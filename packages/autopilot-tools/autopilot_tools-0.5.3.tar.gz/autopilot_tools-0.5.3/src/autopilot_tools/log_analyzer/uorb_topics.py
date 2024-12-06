#!/usr/bin/env python3
from .device_id_parser import parse_device_id


class UorbTopic:
    ref_alt = 0

    def __init__(self, args, need_plot=False) -> None:
        self.args = args
        self.need_plot = need_plot
        self.data = tuple([] for _ in range(len(args)))

    def append_data(self, data):
        self.data = data


class EstimatorLocalPositionRefAlt(UorbTopic):
    def append_data(self, data):
        self.data = data
        UorbTopic.ref_alt = self.data[1][0]


class DistanceSensor(UorbTopic):
    def append_data(self, data):
        self.data = data
        for idx in range(len(self.data[1])):
            if self.data[1][idx] > 70:
                self.data[1][idx] = 0
            self.data[1][idx] *= -1


class VehicleGpsPosition(UorbTopic):
    def append_data(self, data):
        self.data = data
        for idx in range(len(self.data[1])):
            self.data[1][idx] /= 1000
            self.data[1][idx] = UorbTopic.ref_alt - self.data[1][idx]


class VehicleAirDataBaroAltMeter(UorbTopic):
    def append_data(self, data):
        self.data = data
        baro_offset = self.data[1][0]
        for idx in range(len(self.data[1])):
            self.data[1][idx] -= baro_offset
            self.data[1][idx] *= -1


class SensorGps(UorbTopic):
    def append_data(self, data):
        if len(data[2]) == 0:
            return

        self.data = data
        device_id = int(sum(self.data[2]) / len(self.data[2]))
        parse_device_id(device_id, verbose=True)
        for idx in range(len(self.data[1])):
            self.data[1][idx] /= 1000
            self.data[1][idx] = UorbTopic.ref_alt - self.data[1][idx]


class ActuatorOutputs(UorbTopic):
    def __init__(self, args=("timestamp", "output[7]"), need_plot=False) -> None:
        super().__init__(args, need_plot)
        self.msg = "actuator_outputs_0"
        self.values = {}
        for arg in self.args:
            self.values[arg] = []

    def fill_values(self):
        for idx, arg in enumerate(self.args):
            self.values[arg] = self.data[idx]

    def append_data(self, data):
        self.data = data
        for idx in range(len(self.data[1])):
            if self.data[1][idx] == 65535:
                self.data[1][idx] = 0
        self.fill_values()


class EscStatus(UorbTopic):
    def __init__(self, args=("timestamp",
                             "esc[0].esc_rpm",
                             "esc[1].esc_rpm",
                             "esc[2].esc_rpm",
                             "esc[3].esc_rpm",
                             "esc[0].esc_voltage",
                             "esc[1].esc_voltage",
                             "esc[2].esc_voltage",
                             "esc[3].esc_voltage"), need_plot=False) -> None:
        super().__init__(args, need_plot)
        self.msg = "esc_status_0"
        self.values = {}
        for arg in self.args:
            self.values[arg] = []

    def fill_values(self):
        for idx, arg in enumerate(self.args):
            self.values[arg] = self.data[idx]

    def append_data(self, data):
        self.data = data
        for idx in range(len(self.data[1])):
            if self.data[1][idx] == 65535:
                self.data[1][idx] = 0
        self.fill_values()
