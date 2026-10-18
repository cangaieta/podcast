#!/usr/bin/env python3
"""
Genera els jingles d'entrada i sortida del podcast (assets/audio/jingle-*.wav).

Rumbeta en re major: rasgueig de guitarra de niló amb calaix, i a sobre el
motiu de quatre notes "Can Gai-e-tà" (re mi fa# LA, l'accent a la darrera
síl·laba com quan es diu el nom). La sortida fa el motiu baixant i resol en un
acord de re amb el baix greu.

La guitarra és síntesi Karplus-Strong (una corda que vibra simulada), no
mostres. Si algun dia es vol un so més real, les notes són aquestes: es poden
passar a GarageBand.

Per què no MusicGen: es va provar (2026-10) i fa música en bucle, sense principi
ni final; retallada a 2-3 s sona tallada.

El generador és determinista (llavor fixa): tornar-lo a executar reprodueix
exactament els fitxers de assets/audio/. Si en canvies una nota, escolta el
resultat abans de substituir-los.

Ús:
    python scripts/generate_jingles.py                 # escriu a assets/audio/
    python scripts/generate_jingles.py --output-dir /tmp/proves
"""

import argparse
import os

import numpy as np
import soundfile as sf
from scipy.signal import butter, fftconvolve, sosfilt

SR = 44100
rng = np.random.default_rng(11)


def hz(n):
    return 440.0 * 2 ** ((n - 69) / 12)  # MIDI -> Hz


def place(b, s, t):
    i = int(t * SR)
    j = min(len(b), i + len(s))
    b[i:j] += s[:j - i]


def lp(x, fc):
    return sosfilt(butter(2, fc / (SR / 2), "low", output="sos"), x)


def pluck(n, dur, vol=0.3, bright=0.5):
    """Karplus-Strong: corda de niló."""
    N = int(dur * SR)
    p = int(SR / hz(n))
    ring = lp(rng.uniform(-1, 1, p), 2000 + 6000 * bright)
    out = np.zeros(N)
    for i in range(N):
        out[i] = ring[i % p]
        ring[i % p] = 0.996 * 0.5 * (ring[i % p] + ring[(i + 1) % p])
    return out * vol


def strum(b, notes, t, dur=1.5, gap=0.018, vol=0.22, down=True):
    for k, n in enumerate(notes if down else notes[::-1]):
        place(b, pluck(n, dur, vol), t + k * gap)


def cajon(vol=0.35):
    N = int(0.25 * SR)
    t = np.arange(N) / SR
    cop = np.sin(2 * np.pi * (90 * np.exp(-t * 8) + 60) * t) * np.exp(-t * 18)
    return (cop + 0.3 * lp(rng.standard_normal(N), 1500) * np.exp(-t * 30)) * vol


def reverb(x, dur=1.4, decay=0.35, mix=0.25):
    t = np.arange(int(dur * SR)) / SR
    ir = rng.standard_normal(len(t)) * np.exp(-t / decay)
    ir /= np.sqrt(np.sum(ir ** 2))
    y = np.concatenate([x, np.zeros(len(ir))])
    return y + mix * fftconvolve(y, ir)[:len(y)]


def finish(b, path):
    y = reverb(b)
    y = y[:int(np.max(np.nonzero(np.abs(y) > 2e-3)) + 1)]
    f = int(0.06 * SR)
    y[-f:] *= np.linspace(1, 0, f)
    sf.write(path, y / np.max(np.abs(y)) * 0.9, SR)
    print(f"✅ {path} ({len(y) / SR:.1f}s)")


D = [50, 57, 62, 66, 69]  # acord de Re (guitarra)
A = [45, 52, 57, 61, 64]  # La
G = [43, 50, 55, 59, 62]  # Sol
MOTIU_PUJA = [74, 76, 78, 81]  # "Can Gai-e-tà": re mi fa# LA
MOTIU_BAIXA = [81, 78, 76, 74]


def entrada(path):
    b = np.zeros(int(4 * SR))
    beat = 0.16
    for k, (ch, avall) in enumerate([(D, True), (D, False), (A, True), (A, False)]):
        strum(b, ch, k * beat * 2, 0.5, 0.012, 0.16, avall)
        place(b, cajon(), k * beat * 2)
    for i, n in enumerate(MOTIU_PUJA):
        place(b, pluck(n, 0.9, 0.3, 0.8), 0.05 + i * beat * 2)
    strum(b, D + [74], 1.3, 2.0, 0.025, 0.22)
    place(b, cajon(0.45), 1.3)
    finish(b, path)


def sortida(path):
    b = np.zeros(int(4 * SR))
    beat = 0.18
    for k, (ch, avall) in enumerate([(D, True), (G, False), (A, True)]):
        strum(b, ch, k * beat * 2, 0.5, 0.012, 0.15, avall)
        place(b, cajon(0.3), k * beat * 2)
    for i, n in enumerate(MOTIU_BAIXA):
        place(b, pluck(n, 0.9, 0.3, 0.8), 0.05 + i * beat * 1.5)
    strum(b, [38] + D, 1.15, 2.2, 0.04, 0.2)
    finish(b, path)


def main():
    parser = argparse.ArgumentParser(description="Genera els jingles d'entrada i sortida")
    parser.add_argument("--output-dir", default="assets/audio")
    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    entrada(os.path.join(args.output_dir, "jingle-entrada.wav"))
    sortida(os.path.join(args.output_dir, "jingle-sortida.wav"))


if __name__ == "__main__":
    main()
