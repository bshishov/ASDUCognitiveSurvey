from struct import *
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
        for n in range(N): Fm += fnList[n] * cmath.exp(- 1j * pi2 * m * n / N)
        FmList.append(abs(Fm / N))
    return FmList


def calc_cepstrum(spectrum):
    return dft([cmath.log(amp) for i, amp in enumerate(spectrum)])


filename = files["audio.wav"]
f = open(filename, "rb")
x = 0
raw = []
fund = []
while x != os.path.getsize(filename)//80 - 1:
    #фрагменты по 10мс
    raw_input = read_file(f)[0:80]
    raw.append(raw_input)
    #окно Хемминга
    raw_input = [amp * 1.8 * (0.5 - 0.5 * cmath.cos(2*3.1415*i/len(raw_input))) for i, amp in enumerate(raw_input)]
    spectrum = dft(raw_input)
    cepstrum = calc_cepstrum(spectrum)
    #основные частоты голосов взрослых людей лежат в диапазоне 80..270 Гц
    #тогда диапазон периодов 30..100 (8000/270..8000/80).
    fund_freq = 8000 * len(cepstrum) / (np.argmax(cepstrum[30:100]) + 30.0) / len(cepstrum)
    fund.append(fund_freq)
    x += 1
    f.seek(x*80)
f.close()


f0_avg = np.mean(fund)
print('Average fundamental frequency: ', f0_avg)

f0_std = np.std(fund)
print('Standard deviation: ', f0_std)
