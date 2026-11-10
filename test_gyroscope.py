
import time

from sensor.mpu6050 import MPU6050


sensor = MPU6050()

try:
    print("Gyroscope reading started.")

    while True:
        gyro_x, gyro_y, gyro_z = sensor.read_gyroscope()

        print(
            f"Gyro X: {gyro_x:8.2f} °/s | "
            f"Gyro Y: {gyro_y:8.2f} °/s | "
            f"Gyro Z: {gyro_z:8.2f} °/s",
            flush=True
        )

        time.sleep(0.3)

except KeyboardInterrupt:
    print("\nGyroscope test stopped.")

finally:
    sensor.close()
