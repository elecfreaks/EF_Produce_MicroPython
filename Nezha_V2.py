from microbit import *
from time import *

NEZHA_V2_ADDR = 0x10


class NEZHA_V2(object):
    def __init__(self):
        i2c.init()
    def Motorspeed(self, motor, direction,speed,MotorFunction):
        speed_H  =(speed >> 8) & 0XFF
        speed_L = (speed >> 0) & 0XFF
        i2c.write(NEZHA_V2_ADDR, bytearray([0xFF, 0xF9, motor, direction,0x70,speed_H,MotorFunction,speed_L]))
    def goToAbsolutePosition(self, motor, modePostion,target_angle):
        while (target_angle < 0) :
            target_angle += 360
        target_angle %= 360
        target_H = (target_angle >> 8) & 0XFF
        target_L = (target_angle >> 0) & 0XFF
        i2c.write(NEZHA_V2_ADDR, bytearray([0xFF, 0xF9, motor, 0x00,0x5D,target_H,modePostion,target_L]))
    def nezha2MotorStart(self, motor, direction):
        i2c.write(NEZHA_V2_ADDR, bytearray([0xFF, 0xF9, motor, direction,0x5E,0x00,0xF5,0x00]))
    def nezha2MotorStop(self, motor):
        i2c.write(NEZHA_V2_ADDR, bytearray([0xFF, 0xF9, motor, 0x00,0x5F,0x00,0xF5,0x00]))
    def nezha2MotorSpeedCtrolExport(self, motor,speed):
        if (speed > 0) :
            direction=1
        else:
           direction=2
        i2c.write(NEZHA_V2_ADDR, bytearray([0xFF, 0xF9, motor, direction,0x60,abs(speed),0xF5,0x00]))
    def servoPostionReset(self, motor):
        i2c.write(NEZHA_V2_ADDR, bytearray([0xFF, 0xF9, motor, 0x00,0x1D,0x00,0xF5,0x00]))
    def readServoAbsolutePostion(self, motor):
        i2c.write(NEZHA_V2_ADDR, bytearray([0xFF, 0xF9, motor, 0x00,0x46,0x00,0xF5,0x00]))
        sleep_ms(4)
        arr = i2c.read(NEZHA_V2_ADDR, 4)
        position = (arr[3] << 24) | (arr[2] << 16) | (arr[1] << 8) | (arr[0])
        while (position < 0) :
            position += 3600
        return (position % 3600) * 0.1
    def readServoAbsoluteSpeed(self, motor):
        i2c.write(NEZHA_V2_ADDR, bytearray([0xFF, 0xF9, motor, 0x00,0x47,0x00,0xF5,0x00]))
        sleep_ms(3)
        ServoSpeed1Arr= i2c.read(NEZHA_V2_ADDR, 2)
        Servo1Speed = (ServoSpeed1Arr[1] << 8) | (ServoSpeed1Arr[0])
        return Math.floor(Servo1Speed * 0.0926)

    #     let ServoSpeed1Arr = pins.i2cReadBuffer(i2cAddr, 2);
    #     let Servo1Speed = (ServoSpeed1Arr[1] << 8) | (ServoSpeed1Arr[0]);
    #     return Math.floor(Servo1Speed * 0.0926);
    # }


if __name__ == '__main__':
    nezha = NEZHA_V2()

# while True:
#     if button_a.was_pressed():
#         nezha.Motorspeed(1,1, 100,1)
#     if button_b.was_pressed():
#         nezha.Motorspeed(1,1, 0,1)
    
# while True:
#     if button_a.was_pressed():
#         nezha.readServoAbsolutePostion(1)
#     if button_b.was_pressed():
#         nezha.goToAbsolutePosition(1,1, 0)
