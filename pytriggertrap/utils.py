# encoding: utf-8
import math
from typing import List, Union, Callable


class ChunkIterator(object):
    """
    This iterator cuts down an iterator into several chunks. By example, you can iterate over
    a very long list and do chunk creates every 1000 entry using this.
    """

    def __init__(self, iterable):
        self.iterator = iter(iterable)
        self.iterating = True
        self._next = None
        self.iterated = 0

        self.next()

    def next(self):
        nxt = self._next

        try:
            self._next = next(self.iterator)
        except StopIteration:
            self.iterating = False

        return nxt

    def chunks(self, size):
        """
        Call this method to return the chunks iterator

        :param size: int, size of a chunk
        :return:
        """

        def iter_chunk():
            for i in range(0, size):
                yield self.next()
                self.iterated += 1

                if not self.iterating:
                    break

        while self.iterating:
            yield iter_chunk()


def sine_wave(f: float,
              length: float,
              rate: int = 44100,
              amplitude: Union[float, Callable] = 1.0) \
        -> List[float]:
    """
    Generates a successive values of a sine wave points.

    :param f: frequency in Hz 
    :param length: duration in s
    :param rate: frame/sample rate in Hz
    :param amplitude: amplitude in an arbitrary unit
    """

    b = 2 * math.pi * f
    p = 1.0 / float(rate)

    if callable(amplitude):
        a = amplitude
    else:
        def constant_amplitude(_):
            return 1.0
        a = constant_amplitude

    def y(i):
        t = i * p
        return a(t) * math.sin(b * t)

    return list(map(y, range(0, int(math.floor(length / p)))))


def progress(it):
    from progressbar import ProgressBar
    bar = ProgressBar()

    for done, total in it:
        bar.max_value = total
        bar.update(done)

    bar.update(bar.max_value, force=True)
    print('')
