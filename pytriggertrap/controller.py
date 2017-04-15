# encoding: utf-8
import math
import wave
import struct
import os
from typing import List, Tuple, Iterable
from subprocess import Popen, PIPE

from .utils import sine_wave, ChunkIterator


class TTController(object):
    RATE = 44100
    FREQ = 17000
    DURATION = 0.05
    PAUSE = 0.001
    CHANNEL_WIDTH = 2
    FFMPEG_BIN = 'ffmpeg'

    def __init__(self):
        def left_pulse_amplitude(t):
            if t < self.PAUSE:
                return 0.0
            else:
                return 1.0

        self.right_pulse = sine_wave(self.FREQ, self.DURATION, self.RATE)
        self.left_pulse = sine_wave(self.FREQ, self.DURATION, self.RATE, left_pulse_amplitude)

    def make_pulse(self, n: int=3) -> Tuple[List[float], List[float]]:
        """
        Generates the waveform for the specified number of pulses. Each pulse lasts 50ms. The
        default value is "3" which matches TriggerTrap's own default value of 150ms.

        :param n: Number of pulses to send
        :return: a tuple with the left wave and the right wave
        """
        return self.left_pulse * n, self.right_pulse * n

    def make_timelapse_waveform(self, frames, period, pulses=3) \
            -> Tuple[int, Iterable[Tuple[float, float]]]:
        """
        Generate the waveforms to make a timelapse. 
        
        :param frames: how many frames do you want to capture ?
        :param period: the time between each frame
        :param pulses: number of pulses to send
        :return: an iterable of the left and the right signal
        """

        p = 1.0 / float(self.RATE)
        l, r = self.make_pulse(pulses)

        total = int(math.floor(period / p))
        pulse_length = len(l)

        def make():
            for _ in range(0, frames):
                for i in range(0, total):
                    if i < pulse_length:
                        yield l[i], r[i]
                    else:
                        yield 0.0, 0.0

        return int(total * frames), make()

    def write_timelapse_waveform_wav(self, output_file, frames, period, pulses=3):
        with wave.open(output_file, 'wb') as w:  # type: wave.Wave_write
            n_frames, frames_it = self.make_timelapse_waveform(frames, period, pulses)
            it = ChunkIterator(frames_it)

            w.setnchannels(2)
            w.setsampwidth(self.CHANNEL_WIDTH)
            w.setframerate(self.RATE)
            w.setnframes(n_frames)

            amp = (2 ** (self.CHANNEL_WIDTH * 8 - 1)) - 1

            for data in it.chunks(10000):
                out = b''.join(struct.pack('h', int(amp * y)) for x in data for y in x)
                w.writeframesraw(out)

                yield it.iterated, n_frames

    def write_timelapse_waveform_mp3(self, file_name, frames, period, pulses=3):
        if os.path.exists(file_name):
            os.unlink(file_name)

        p = Popen([
            self.FFMPEG_BIN,
            '-i',
            'pipe:0',
            '-codec:a',
            'libmp3lame',
            '-q:a',
            '0',
            '-f',
            'mp3',
            file_name,
        ], stdout=PIPE, stdin=PIPE, stderr=PIPE)

        for x in self.write_timelapse_waveform_wav(p.stdin, frames, period, pulses):
            yield x

        p.terminate()
        p.wait()

    def calc_timelapse_args(self, input_duration, output_duration, output_fps, pulses):
        d_i = float(input_duration)
        f_o = float(output_fps)
        d_o = float(output_duration)

        p_i = d_i / (f_o * d_o)

        return {
            'frames': int(math.floor(output_duration * output_fps)),
            'period': p_i,
            'pulses': pulses,
        }
