
import os
import math
import time

from smbus2 import SMBus
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


# MPU6050 configuration
I2C_BUS = 1
MPU6050_ADDRESS = 0x68

PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B

# InfluxDB configuration
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUXDB_ORG = "packt"
INFLUXDB_BUCKET = "ch12"

# Sampling interval in seconds
SAMPLE_INTERVAL = 0.1


def convert_to_signed(value):
    """Convert a 16-bit unsigned value to a signed integer."""
    if value >= 32768:
        value -= 65536
    return value


def read_accelerometer(bus):
    """Read and convert accelerometer values from the MPU6050."""

    data = bus.read_i2c_block_data(
        MPU6050_ADDRESS,
        ACCEL_XOUT_H,
        6
    )

    accel_x = convert_to_signed((data[0] << 8) | data[1])
    accel_y = convert_to_signed((data[2] << 8) | data[3])
    accel_z = convert_to_signed((data[4] << 8) | data[5])

    # Convert raw values to g (assuming the +/- 2g range)
    accel_x_g = accel_x / 16384.0
    accel_y_g = accel_y / 16384.0
    accel_z_g = accel_z / 16384.0

    return accel_x_g, accel_y_g, accel_z_g


def calculate_angles(accel_x, accel_y, accel_z):
    """Calculate Roll and Pitch angles in degrees."""

    roll = math.degrees(math.atan2(accel_y, accel_z))

    pitch = math.degrees(
        math.atan2(
            -accel_x,
            math.sqrt(accel_y ** 2 + accel_z ** 2)
        )
    )

    return roll, pitch


def main():

    if not INFLUXDB_TOKEN:
        raise RuntimeError("INFLUXDB_TOKEN environment variable is not set.")

    # Initialize I2C communication
    bus = SMBus(I2C_BUS)

    # Wake up the MPU6050
    bus.write_byte_data(
        MPU6050_ADDRESS,
        PWR_MGMT_1,
        0x00
    )

    # Initialize InfluxDB client
    client = InfluxDBClient(
        url=INFLUXDB_URL,
        token=INFLUXDB_TOKEN,
        org=INFLUXDB_ORG
    )

    write_api = client.write_api(
        write_options=SYNCHRONOUS
    )

    print("MPU6050 data acquisition started.")

    try:
        while True:

            # Read accelerometer data
            accel_x, accel_y, accel_z = read_accelerometer(bus)

            # Calculate orientation angles
            roll, pitch = calculate_angles(
                accel_x,
                accel_y,
                accel_z
            )

            # Create an InfluxDB data point
            point = (
                Point("mpu6050_orientation")
                .tag("location", "raspberry-pi")
                .field("roll", roll)
                .field("pitch", pitch)
            )

            # Write data to InfluxDB
            write_api.write(
                bucket=INFLUXDB_BUCKET,
                record=point
            )

            print(
                f"Roll: {roll:.2f}° | "
                f"Pitch: {pitch:.2f}°"
            )

            time.sleep(SAMPLE_INTERVAL)

    except KeyboardInterrupt:
        print("\nData acquisition stopped.")

    finally:
        write_api.close()
        client.close()
        bus.close()


if __name__ == "__main__":
    main()
