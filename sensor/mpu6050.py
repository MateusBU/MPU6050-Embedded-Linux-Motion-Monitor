import math

from smbus2 import SMBus

I2C_BUS = 1
MPU6050_ADDRESS = 0x68

PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0X3B

GYRO_XOUT_H = 0x43
GYRO_SCALE = 131.0

class MPU6050:
    def __init__(self, bus_number=I2C_BUS):
        self.bus = SMBus(bus_number)

        self.gyro_bias = {
            "x": -4.7684,
            "y": 0.8473,
            "z": -0.6468
        }
        
        # Wake up the MPU6050
        self.bus.write_byte_data(
            MPU6050_ADDRESS,
            PWR_MGMT_1,
            0x00
        )
    
    @staticmethod
    def convert_to_signed(value):
        """Convert a 16-bit unsigned value to a signed intereger"""
        if value >= 32768:
            value -= 65536

        return value
    
    def read_accelerometer(self):
        """Read accelerometer values and convert them to g."""

        #The accelerometer data (X, Y, and Z axes) takes up 6 consecutive bytes, starting at register 0x3B (2 bytes for each axis).
        data = self.bus.read_i2c_block_data(
            MPU6050_ADDRESS,
            ACCEL_XOUT_H,
            6
        )

        accel_x = self.convert_to_signed(
            data[0] << 8 | data[1]
        )

        accel_y = self.convert_to_signed(
            data[2] << 8 | data[3]
        )

        accel_z = self.convert_to_signed(
            data[4] << 8 | data[5]
        )

        #16384.0 +- 2g
        return(
            accel_x / 16384.0,
            accel_y / 16384.0,
            accel_z / 16384.0,
        )

    @staticmethod
    def calculate_angles(accel_x, accel_y, accel_z):
        """Calculate Roll and Pitch angles in degrees"""

        roll = math.degrees(
            math.atan2(accel_y, accel_z)
        )

        pitch = math.degrees(
            math.atan2(
                -accel_x,
                math.sqrt(accel_y ** 2 + accel_z ** 2)
            )
        )

        return roll, pitch

    def read_orientation(self):
        """Read accelerometer and return Roll and Pitch"""

        accel_x, accel_y, accel_z = self.read_accelerometer()

        return self.calculate_angles(
            accel_x,
            accel_y,
            accel_z
        )


    def read_gyroscope(self):
        """Read gyroscope values and compensate for sensor bias."""

        data = self.bus.read_i2c_block_data(
            MPU6050_ADDRESS,
            GYRO_XOUT_H,
            6
        )

        gyro_x = self.convert_to_signed(
            (data[0] << 8) | data[1]
        ) / GYRO_SCALE

        gyro_y = self.convert_to_signed(
            (data[2] << 8) | data[3]
        ) / GYRO_SCALE

        gyro_z = self.convert_to_signed(
            (data[4] << 8) | data[5]
        ) / GYRO_SCALE

        # Compensate gyroscope bias
        gyro_x -= self.gyro_bias["x"]
        gyro_y -= self.gyro_bias["y"]
        gyro_z -= self.gyro_bias["z"]

        return gyro_x, gyro_y, gyro_z

    def close(self):
        self.bus.close()