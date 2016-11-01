#!/usr/bin/env python3
from tools.html_chart_helper import *
from dsp.config     import ONE, SAMPLE_RATE, SAMPLE_dT, FIX_FP_REST_SIZE
from dsp.dds        import DDS

class Simulator(DDS):
    def __init__(self, magnitude, frequency):
        super().__init__()
        self.current_time = 0.0
        self.output = []
        self.magnitude = magnitude
        self.frequency = frequency

    @property
    def magnitude(self):
        return self._magnitude / ONE
    @magnitude.setter
    def magnitude(self, magnitude):
        self._magnitude = int(magnitude * ONE)

    @property
    def frequency(self):
        return self._frequency
    @frequency.setter
    def frequency(self, frequency):
        if frequency > SAMPLE_RATE / 2: print("frequency is too high")
        self._frequency = frequency

    def run(self, interval):
        end_timestamp = self.current_time + interval
        while self.current_time < end_timestamp:
            self.current_time += 1 / SAMPLE_RATE
            sample = self.get_next_sample(SAMPLE_dT)

            item = (int(self.current_time * 1000000),  sample / (ONE >> FIX_FP_REST_SIZE))
            self.output.append(item)

if __name__ == "__main__":
    s1 = Simulator(magnitude = 1.0, frequency = 110)
    s1.run(0.003)
    s1.frequency = 500
    s1.run(0.003)
    s1.frequency = 20
    s1.run(0.003)

    put_html_to_file('dds_output', 
        make_html_chart(s1.output, 'time_us', 'value'))


    s2 = Simulator(1 / 2**14, 110)
    s2.run(0.003)
    s2.frequency = 500
    s2.run(0.003)
    s2.frequency = 20
    s2.run(0.003)

    put_html_to_file('dds_output_low_magnitude', 
        make_html_chart(s2.output, 'time_us', 'value'))