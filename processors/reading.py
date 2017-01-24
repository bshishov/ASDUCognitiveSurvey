from struct import *
import wave
import cmath
import numpy as np
import os.path


def read_file(f):
    chunk = f.read(2)
    raw_input = []
    while chunk:
        raw_input.append(unpack('<h', chunk)[0])
        chunk = f.read(2)
    return raw_input


def dft(fnList):
    pi2 = cmath.pi * 2.0
    N = len(fnList)
    FmList = []
    for m in range(N):
        Fm = 0.0
        for n in range(N):
            Fm += fnList[n] * cmath.exp(- 1j * pi2 * m * n / N)
        FmList.append(abs(Fm / N) + 0.0000000000001)
    return FmList


def calc_cepstrum(spectrum):
    return dft([cmath.log(amp) for i, amp in enumerate(spectrum)])


def f0_freq(filename):
    wav = wave.open(filename, mode="r")
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
    print(nchannels, sampwidth, framerate, nframes, comptype, compname)
    f = open(filename, "rb")
    x = 0
    raw = []
    fund = []
    if (framerate // 100) % 2 == 1:
        fr = framerate // 100 + 1
    else:
        fr = framerate // 100
    print(os.path.getsize(filename), fr)
    while (x != (os.path.getsize(filename) // fr) - 1):
        # фрагменты по 2 мс
        raw_input = read_file(f)[0:fr]
        raw.append(raw_input)
        # окно Хемминга
        raw_input = [amp * 1.8 * (0.5 - 0.5 * cmath.cos(2 * 3.1415 * i / len(raw_input))) for i, amp in
                     enumerate(raw_input)]
        spectrum = dft(raw_input)
        cepstrum = calc_cepstrum(spectrum)
        # основные частоты голосов взрослых людей лежат в диапазоне 80..270 Гц
        # тогда диапазон периодов (framerate/270..framerate/80).
        down = framerate // 270
        up = framerate // 80
        d = framerate / 270
        fund_freq = framerate * len(cepstrum) / (np.argmax(cepstrum[down:up]) + d) / len(cepstrum)
        fund.append(fund_freq)
        x += 1
        f.seek(x * fr)
    f.close()
    print("fundamental frequency list: ", fund)
    return fund


filename = files["audio.wav"]
f0_freq = f0_freq(filename)
f0_freq_mean = np.mean(f0_freq)
f0_freq_std = np.mean(f0_std)

print('Average fundamental frequency: ', f0_freq_mean)
print('Standard deviation: ', f0_freq_std)
