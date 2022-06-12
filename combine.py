#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import wave
import numpy as np
import pyaudio
import librosa
import soundfile as sf
import scipy.signal as signal
import struct

# ok，音频叠加！我这里4.wav和5.wav都是5s的音频，还没有测试时长不同的音频！
# 参考文档：https://www.cnblogs.com/xingshansi/p/6799994.html
x, _ = librosa.load('D:/4.wav', sr=16000)  # 需要修改的地方：音频1
sf.write('t1.wav', x, 16000)
y, _ = librosa.load('D:/5.wav', sr=16000)  # 需要修改的地方：音频2
sf.write('t2.wav', y, 16000)
f1 = wave.open('t1.wav', 'rb')
f2 = wave.open('t2.wav', 'rb')

# 音频1的数据
params1 = f1.getparams()
nchannels1, sampwidth1, framerate1, nframes1, comptype1, compname1 = params1[:6]
print(nchannels1, sampwidth1, framerate1, nframes1, comptype1, compname1)
f1_str_data = f1.readframes(nframes1)
f1.close()
f1_wave_data = np.frombuffer(f1_str_data, dtype=np.int16)

# 音频2的数据
params2 = f2.getparams()
nchannels2, sampwidth2, framerate2, nframes2, comptype2, compname2 = params2[:6]
print(nchannels2, sampwidth2, framerate2, nframes2, comptype2, compname2)
f2_str_data = f2.readframes(nframes2)
f2.close()
f2_wave_data = np.frombuffer(f2_str_data, dtype=np.int16)

# 对不同长度的音频用数据零对齐补位
if nframes1 < nframes2:
    length = abs(nframes2 - nframes1)
    temp_array = np.zeros(length, dtype=np.int16)
    rf1_wave_data = np.concatenate((f1_wave_data, temp_array))
    rf2_wave_data = f2_wave_data
elif nframes1 > nframes2:
    length = abs(nframes2 - nframes1)
    temp_array = np.zeros(length, dtype=np.int16)
    rf2_wave_data = np.concatenate((f2_wave_data, temp_array))
    rf1_wave_data = f1_wave_data
else:
    rf1_wave_data = f1_wave_data
    rf2_wave_data = f2_wave_data

# ================================
# 合并1和2的数据
new_wave_data = rf1_wave_data + rf2_wave_data
new_wave_data = new_wave_data * 1.0 / (max(abs(new_wave_data)))  # wave幅值归一化
new_wave = new_wave_data.tostring()

p = pyaudio.PyAudio()
CHANNELS = 1
FORMAT = pyaudio.paInt16

# 写文件
framerate = 44100
time = 10

# 产生10秒44.1kHz的100Hz - 1kHz的频率扫描波。没用！
t = np.arange(0, time, 1.0 / framerate)
wave_data = signal.chirp(t, 100, time, 1000, method='linear') * 10000
wave_data = wave_data.astype(np.short)

# 打开WAV文档
f = wave.open(r"D:\6.wav", "wb")  # 需要修改的地方：输出音频

# 配置声道数、量化位数和取样频率
nchannels = 1  # 单通道为例
sampwidth = 2
data_size = len(new_wave_data)
framerate = 16000  # 设置为44100就是1s，设置为8000就是10s，只有16000才是5s是对的。这里还没搞懂！
nframes = data_size
comptype = "NONE"
compname = "not compressed"
f.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
# 将wav_data转换为二进制数据写入文件
# f.writeframes(new_wave)
for v in new_wave_data:
    f.writeframes(struct.pack('h', int(v * 64000 / 2)))
f.close()


# 实现录音,暂时用不到。
def record(re_frames, WAVE_OUTPUT_FILENAME):
    print("开始录音")
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(re_frames)
    wf.close()
    print("关闭录音")