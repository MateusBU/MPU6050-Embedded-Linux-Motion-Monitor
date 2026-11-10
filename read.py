

import time
from datetime import datetime

from sensor.mpu6050 import MPU6050
from database.influxdb_client import (
    create_client,
    create_write_api,
    write_orientation
)

# Sampling interval in seconds
SAMPLE_INTERVAL = 0.3


def main():

    sensor = None
    client = None
    write_api = None

    try:
        sensor = MPU6050()

        client = create_client()
        write_api = create_write_api(client)

        print("MPU6050 data acquisition started.")
        
        while True:

            roll, pitch = sensor.read_orientation()

            write_orientation(
                write_api,
                roll,
                pitch
            )

            current_time = datetime.now().strftime("%H:%M:%S")

            print(
                f"[{current_time}] Sent to InfluxDB -> Roll: {roll:.2f}° | Pitch: {pitch:.2f}°",
                flush=True,
            )

            time.sleep(SAMPLE_INTERVAL)

    except KeyboardInterrupt:
        print("\nData acquisition stopped.")


    finally:
        if write_api:
            write_api.close()

        if client:
            client.close()

        if sensor:
            sensor.close()


if __name__ == "__main__":
    main()
