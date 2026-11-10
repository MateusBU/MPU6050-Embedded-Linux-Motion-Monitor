
import time

from sensor.mpu6050 import MPU6050


SAMPLES = 500
SAMPLE_INTERVAL = 0.01


sensor = MPU6050()

gyro_x_sum = 0.0
gyro_y_sum = 0.0
gyro_z_sum = 0.0

try:
    print("Keep the sensor completely still...")
    time.sleep(2)

    for _ in range(SAMPLES):
        gyro_x, gyro_y, gyro_z = sensor.read_gyroscope()

        gyro_x_sum += gyro_x
        gyro_y_sum += gyro_y
        gyro_z_sum += gyro_z

        time.sleep(SAMPLE_INTERVAL)

    print("\nGyroscope bias:")

    print(f"X: {gyro_x_sum / SAMPLES:.4f} °/s")
    print(f"Y: {gyro_y_sum / SAMPLES:.4f} °/s")
    print(f"Z: {gyro_z_sum / SAMPLES:.4f} °/s")

finally:
    sensor.close()
