#!/usr/bin/env python3
import matplotlib.pyplot as plt

from .extract import extract_args
from .uorb_topics import UorbTopic, DistanceSensor, EstimatorLocalPositionRefAlt, \
    VehicleGpsPosition, VehicleAirDataBaroAltMeter, SensorGps
from .utils import log_name_from_full_path

UORB_TOPICS = {
    "vehicle_local_position_0":     UorbTopic(["z"], True),
    "distance_sensor_0":            DistanceSensor(["current_distance"], True),
    "estimator_local_position_0":   EstimatorLocalPositionRefAlt(["ref_alt"]),
    "vehicle_gps_position_0":       VehicleGpsPosition(["alt"]),
    "vehicle_air_data_0":           VehicleAirDataBaroAltMeter(["baro_alt_meter"], True),
    "sensor_gps_0":                 SensorGps(["alt", "device_id"], True),
    "sensor_gps_1":                 SensorGps(["alt", "device_id"], True),
}


def altitude(log_path, output_path, output_report_path):
    log_name = log_name_from_full_path(log_path)

    # 1. Extract and process data
    for topic, uorb in UORB_TOPICS.items():
        data_args = uorb.args
        tss_and_data = extract_args(log_path=f"{log_path}/{log_name}.ulg",
                                    output_path=output_path,
                                    msg=topic,
                                    msg_fields=("timestamp", *data_args))
        uorb.append_data(tss_and_data)

    # 2. Plot
    plt.cla()
    for topic, uorb in UORB_TOPICS.items():
        if uorb.need_plot is False:
            continue
        tss = uorb.data[0]
        data = uorb.data[1]
        plt.plot(tss, data, label=str(topic + "." + uorb.args[0]))
    plt.legend()
    plt.xlabel("time")
    plt.ylabel("altitude")
    plt.title(log_name)
    plt.grid()
    plt.savefig(f'{output_report_path}/altitude.png')
