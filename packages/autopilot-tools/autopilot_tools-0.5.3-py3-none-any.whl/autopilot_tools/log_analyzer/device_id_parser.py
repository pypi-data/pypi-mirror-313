#!/usr/bin/env python3

BUS_TYPE_TO_STRING = {
    0: "unknown",
    1: "i2c",
    2: "spi",
    3: "uavcan",
    4: "sim",
    5: "serial",
    6: "mavlink",
}

DEV_TYPE_TO_STRING = {
    61:  "baro_ms5611",
    129: "baro_uavcan",
    131: "diff_press_uavcan",
    133: "gps_uavcan",
    161: "gps_EMLID"
}


def print_dev_id(device_id, data):
    output_string = f"device_id={device_id}: "

    dev_type_value = data["devtype"]
    dev_type_str = DEV_TYPE_TO_STRING.get(dev_type_value, "Unknown")
    output_string += f"devtype={dev_type_value} ({dev_type_str}), "

    address_value = data["address"]
    output_string += f"address={address_value}, "

    output_string += "bus=?, "

    bus_type_value = data["bus_type"]
    bus_type_name = BUS_TYPE_TO_STRING.get(bus_type_value, "Unknown")
    output_string += f"bus_type={bus_type_value} ({bus_type_name})"

    print(output_string)


def parse_device_id(device_id: int, verbose=False):
    data = {
        "bus_type": device_id % 256,
        "devtype": (device_id >> 16) % 256,
        "address": (device_id >> 8) % 256,
        "bus": (device_id >> 24) % 256,
        "zero_byte": (device_id >> 24) % 256
    }

    if verbose:
        print_dev_id(device_id, data)

    return data


if __name__ == '__main__':
    import sys

    parse_device_id(int(sys.argv[1]), verbose=True)
