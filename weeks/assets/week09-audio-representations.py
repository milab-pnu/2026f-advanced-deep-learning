# 09b-audio.mdx 의 "같은 발화의 네 가지 표현" 그림을 만든다.
#
# 입력 음성: Wikimedia Commons, "LL-Q1860 (eng)-Foobarista2-this is a test sentence.wav" (CC0)
#   https://commons.wikimedia.org/wiki/File:LL-Q1860_(eng)-Foobarista2-this_is_a_test_sentence.wav
# 사용: python3 week09-audio-representations.py <입력.wav> <출력.png>
# 필요: numpy, matplotlib

import sys
import wave

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

SR = 16000  # 목표 sampling rate
WIN = 400  # 25 ms window
HOP = 160  # 10 ms hop
N_MEL = 80
N_MFCC = 13


def load_mono(path):
    with wave.open(path, "rb") as w:
        sr, n, ch, width = w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(n)
    assert width == 2, "16-bit PCM만 지원"
    x = np.frombuffer(raw, dtype="<i2").astype(np.float64) / 32768.0
    if ch > 1:
        x = x.reshape(-1, ch).mean(axis=1)
    return x, sr


def resample_integer(x, sr, target):
    """정수 배 decimation. 먼저 windowed-sinc 저역 통과 필터로 aliasing을 막는다."""
    factor = sr // target
    assert sr == target * factor, "정수 배 관계만 지원"
    if factor == 1:
        return x
    taps = 255
    n = np.arange(taps) - (taps - 1) / 2
    cutoff = 0.45 / factor  # 정규화 주파수 (cycles/sample)
    h = 2 * cutoff * np.sinc(2 * cutoff * n) * np.hamming(taps)
    h /= h.sum()
    return np.convolve(x, h, mode="same")[::factor]


def stft_power(x):
    pad = WIN // 2
    x = np.pad(x, (pad, pad), mode="reflect")
    n_frames = 1 + (len(x) - WIN) // HOP
    idx = np.arange(WIN)[None, :] + HOP * np.arange(n_frames)[:, None]
    frames = x[idx] * np.hanning(WIN)[None, :]
    return np.abs(np.fft.rfft(frames, n=WIN, axis=1)) ** 2  # (frames, 201)


def hz_to_mel(f):
    return 2595.0 * np.log10(1.0 + f / 700.0)


def mel_to_hz(m):
    return 700.0 * (10.0 ** (m / 2595.0) - 1.0)


def mel_filterbank(n_bins):
    freqs = np.linspace(0, SR / 2, n_bins)
    edges = mel_to_hz(np.linspace(hz_to_mel(0.0), hz_to_mel(SR / 2), N_MEL + 2))
    fb = np.zeros((N_MEL, n_bins))
    for m in range(N_MEL):
        lo, mid, hi = edges[m], edges[m + 1], edges[m + 2]
        up = (freqs - lo) / (mid - lo)
        down = (hi - freqs) / (hi - mid)
        fb[m] = np.clip(np.minimum(up, down), 0, None)
    return fb


def dct2_ortho(x):
    """마지막 축에 대한 orthonormal DCT-II."""
    n = x.shape[-1]
    k = np.arange(n)[:, None]
    basis = np.cos(np.pi * (np.arange(n)[None, :] + 0.5) * k / n) * np.sqrt(2.0 / n)
    basis[0] /= np.sqrt(2.0)
    return x @ basis.T


def main(src, dst):
    x, sr = load_mono(src)
    x = resample_integer(x, sr, SR)
    x = x / np.max(np.abs(x))

    power = stft_power(x)
    mel = power @ mel_filterbank(power.shape[1]).T
    log_spec = 10 * np.log10(power + 1e-10)
    log_mel = 10 * np.log10(mel + 1e-10)
    mfcc = dct2_ortho(np.log(mel + 1e-10))[:, :N_MFCC]

    dur = len(x) / SR
    n_frames = power.shape[0]
    top = log_spec.max()

    plt.rcParams.update({"font.size": 11, "axes.titlesize": 12, "axes.titleweight": "bold"})
    fig, ax = plt.subplots(4, 1, figsize=(9, 9.2), sharex=True, gridspec_kw={"height_ratios": [1, 1.5, 1.5, 1]})

    ax[0].plot(np.arange(len(x)) / SR, x, color="#2a78d6", linewidth=0.5)
    ax[0].set_title("Waveform: %s samples at 16 kHz" % format(len(x), ","), loc="left")
    ax[0].set_ylabel("amplitude")
    ax[0].set_ylim(-1.05, 1.05)

    ax[1].imshow(log_spec.T, origin="lower", aspect="auto", cmap="magma", vmin=top - 80, vmax=top,
                 extent=[0, dur, 0, SR / 2000])
    ax[1].set_title("Spectrogram: %d frames x %d frequency bins" % (n_frames, power.shape[1]), loc="left")
    ax[1].set_ylabel("frequency (kHz)")

    ax[2].imshow(log_mel.T, origin="lower", aspect="auto", cmap="magma", vmin=log_mel.max() - 80,
                 vmax=log_mel.max(), extent=[0, dur, 0, N_MEL])
    ax[2].set_title("Log-Mel spectrogram: %d frames x %d Mel bins" % (n_frames, N_MEL), loc="left")
    ax[2].set_ylabel("Mel bin")

    lim = np.percentile(np.abs(mfcc[:, 1:]), 99)
    ax[3].imshow(mfcc[:, 1:].T, origin="lower", aspect="auto", cmap="RdBu_r", vmin=-lim, vmax=lim,
                 extent=[0, dur, 1, N_MFCC])
    ax[3].set_title("MFCC: %d frames x %d coefficients (c1-c%d shown)" % (n_frames, N_MFCC, N_MFCC - 1), loc="left")
    ax[3].set_ylabel("coefficient")
    ax[3].set_xlabel("time (s)")
    ax[3].set_xlim(0, dur)

    fig.tight_layout()
    fig.savefig(dst, dpi=130, facecolor="white")
    print("samples", len(x), "duration", round(dur, 3), "frames", n_frames, "bins", power.shape[1])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
