import wave
import struct
from scipy.io import wavfile
import numpy as np

def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def frombits(bits):
    chars = []
    for b in range(len(bits) // 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

waveFile = wave.open('fengyu.cai@epfl.ch.wav', 'rb')
datapre = []
length = waveFile.getnframes()
for i in range(0,length):
    waveData = waveFile.readframes(1)
#     print(waveData)
    data = struct.unpack("<hh", waveData)
    datapre.append(data[0] % 2)
    datapre.append(data[1] % 2)

text = frombits(datapre)
import re
pattern = 'COM402\{(\S+)\}'
print(re.search(pattern, text).group(1))

