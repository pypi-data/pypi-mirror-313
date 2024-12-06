#!/usr/bin/env python3
import math
import sys
from bisect import bisect_left
import numpy as np
import matplotlib.pyplot as plt

from .extract import extract_args
from .utils import get_log_names, extract_date_from_date_string, extract_date_from_log_path
from .color_logging import log_info, log_warn


def extract_vehicle_local_position(log_name, output_path):
    extracted_data = extract_args(log_path=log_name,
                                  output_path=output_path,
                                  msg="vehicle_local_position_0",
                                  msg_fields=("x", "y", "z", "xy_valid", "z_valid", "timestamp"))
    pos_x_y_z = (extracted_data[0], extracted_data[1], extracted_data[2])
    xy_valid = extracted_data[3]
    z_valid = extracted_data[4]
    timestamp = extracted_data[5]
    pos_xyz_valid = np.multiply(xy_valid, z_valid)
    flight_time_minutes = (timestamp[-1] - timestamp[0]) / 1000000 / 60
    return pos_x_y_z[0], pos_x_y_z[1], pos_x_y_z[2], pos_xyz_valid, flight_time_minutes


def estimate_distance(pos_x, pos_y, pos_z, pos_xyz_valid):
    total_dist_m = 0
    last_index = -2
    for valid_index in np.argwhere(pos_xyz_valid > 0):
        index = valid_index[0]
        if index == last_index + 1:
            dx = pos_x[index] - pos_x[last_index]
            dy = pos_y[index] - pos_y[last_index]
            dz = pos_z[index] - pos_z[last_index]
            total_dist_m += math.sqrt(dx * dx + dy * dy + dz * dz)
        last_index = index

    return total_dist_m


class BasePlotter:
    def __init__(self) -> None:
        self.x_label_name = ""
        self.y_label_name = ""
        self.title = ""

    def crease_plot_template(self):
        plt.clf()
        plt.grid()
        plt.xlabel(self.x_label_name)
        plt.ylabel(self.y_label_name)
        plt.title(self.title)

    def create(self, total):
        pass


class MonthDistancesPlotter(BasePlotter):
    def __init__(self, output_report_path, dates) -> None:
        super().__init__()
        self.output_report_path = f"{output_report_path}/distance.png"
        self.x_label_name = f"logs from {dates[0]} to {dates[-1]}"
        self.y_label_name = "total distance, km"

        self.month_distances = {}

    def process(self, month_num, dist_km):
        if month_num in self.month_distances:
            self.month_distances[month_num] += dist_km
        else:
            self.month_distances[month_num] = dist_km

    def create(self, total):
        self.title = f"month distance (total {total} km)"
        self.crease_plot_template()

        lists = sorted(self.month_distances.items())
        x, y = zip(*lists)
        plt.bar(x, y)

        plt.savefig(self.output_report_path)


class MonthFlightTimePlotter(BasePlotter):
    def __init__(self, output_report_path, dates) -> None:
        super().__init__()
        self.output_report_path = f'{output_report_path}/month_flight_time.png'
        self.x_label_name = f"logs from {dates[0]} to {dates[-1]}"
        self.y_label_name = "total flight time, hours"

        self.month_flight_time = {}

    def process(self, month_num, flight_time_hours):
        if month_num in self.month_flight_time:
            self.month_flight_time[month_num] += flight_time_hours
        else:
            self.month_flight_time[month_num] = flight_time_hours

    def create(self, total):
        self.title = f"month flight time (total {total} hours)"
        self.crease_plot_template()

        lists = sorted(self.month_flight_time.items())
        x, y = zip(*lists)
        plt.bar(x, y)

        plt.savefig(self.output_report_path)


class CrashDistancePlotter(BasePlotter):
    def __init__(self, output_report_path, dates) -> None:
        super().__init__()
        self.output_report_path = f'{output_report_path}/distance_between_crashes.png'
        self.x_label_name = f"logs from {dates[0]} to {dates[-1]}"
        self.y_label_name = "total distance, km"
        self.title = ""

        self.crash_dates = dates[1:-1]

        self.distance_between_crashes = [0] * (len(self.crash_dates) + 1)
        self.crash_date_nums = []
        for crash_date in self.crash_dates:
            _, crash_day_num = extract_date_from_date_string(crash_date)
            self.crash_date_nums.append(crash_day_num)

    def process(self, day_num, dist_km):
        idx = bisect_left(self.crash_date_nums, day_num)
        self.distance_between_crashes[idx] += dist_km

    def create(self, total):
        self.title = f"distance between crashes (total {int(total)} km)"
        self.crease_plot_template()

        periods = list(self.crash_dates)
        periods.append("now")
        print(len(self.distance_between_crashes))
        plt.bar(periods, self.distance_between_crashes)

        plt.savefig(self.output_report_path)


class FlightStatsEstimator():
    def __init__(self, number_of_logs, output_build_path) -> None:
        self.number_of_logs = number_of_logs
        self.output_path = output_build_path
        self.log_counter = 0
        self.distances = [0]
        self.flight_times = [0]
        self.total_dist_from_all_logs_km = 0
        self.total_flight_time_minutes = 0

    def process_log(self, log_path):
        self.log_counter += 1
        x, y, z, valid, time_minutes = extract_vehicle_local_position(log_path, self.output_path)
        dist_m = estimate_distance(x, y, z, valid)
        dist_km = dist_m * 0.001

        self.total_flight_time_minutes += time_minutes
        self.total_dist_from_all_logs_km += dist_km

        self.print_info(log_path, dist_m)

        self.distances.append(self.total_dist_from_all_logs_km)
        self.flight_times.append(self.total_flight_time_minutes)
        return dist_km, time_minutes

    def print_info(self, log_path, dist_m):
        msg = (
            f"\r{self.log_counter}/{self.number_of_logs}. "
            f"Total {self.total_dist_from_all_logs_km:.1f} km; "
            f"total {round(self.total_flight_time_minutes / 60, 1):3} hours. "
            f"Now: {log_path} has {int(dist_m)} meters"
        )
        sys.stdout.write("\033[K")
        print(msg, end='', flush=True)

    def get_total_distance(self):
        return self.total_dist_from_all_logs_km

    def get_total_flight_time(self):
        return self.total_flight_time_minutes


def flight_distance(input_logs_path, dates, output_build_path, output_report_path):
    log_info(f"The script config:\n- Input {input_logs_path},\n- Output is {output_build_path}.")
    logs_pathes = get_log_names(input_logs_path, verbose=False)

    stats_estimator = FlightStatsEstimator(len(logs_pathes), output_build_path)
    month_distances_plotter = MonthDistancesPlotter(output_report_path, dates)
    month_flight_time_plotter = MonthFlightTimePlotter(output_report_path, dates)
    crash_distance_plotter = CrashDistancePlotter(output_report_path, dates)

    for log_path in logs_pathes:
        month_num, day_num = extract_date_from_log_path(log_path)

        dist_km, flight_time_minutes = stats_estimator.process_log(log_path)
        month_distances_plotter.process(month_num, dist_km)
        month_flight_time_plotter.process(month_num, flight_time_minutes / 60)
        crash_distance_plotter.process(day_num, dist_km)
    print("")  # new line

    total_dist_km = int(stats_estimator.get_total_distance())
    if total_dist_km == 0:
        log_warn("There is no any log or total distance is 0. Skip plot creating.")
        sys.exit()

    month_distances_plotter.create(total_dist_km)
    month_flight_time_plotter.create(int(stats_estimator.get_total_flight_time() / 60))
    crash_distance_plotter.create(total_dist_km)
