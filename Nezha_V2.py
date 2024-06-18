from microbit import *
from time import *

NEZHA_V2_ADDR = 0x10

class motor():  
    A = 1  
    B = 2  
    C = 3  
    D = 4  

class direction():  
    clockwise = 1  
    counterclockwise = 2  

class MotorFunction():  
    turns = 1  
    degrees = 2  
    seconds =3

class modePostion():  
    clockwise = 1  
    counterclockwise = 2  
    shortestpath =3

class NEZHA_V2(object):  
    def __init__(self):  
        i2c.init()  
    def Motorspeed(self, motor, direction, speed, MotorFunction):  
        """  
        设置指定电机的参数和功能。  
        motor:A,B,C,D  
        direction: clockwise(正转),counterclockwise(反转)
        speed: turns(none), degrees(none),seconds(none)
        MotorFunction:  turns,degrees,seconds
        """  
        speed_H = (speed >> 8) & 0xFF  # 高位字节  
        speed_L = speed & 0xFF          # 低位字节  
        i2c.write(NEZHA_V2_ADDR, bytearray([0xFF, 0xF9, motor, direction, 0x70, speed_H, MotorFunction, speed_L]))  
  
    def goToAbsolutePosition(self, motor, modePostion, target_angle):  
        """  
        将指定电机移动到绝对位置。  
        motor:A,B,C,D    
        modePostion: clockwise(正转),counterclockwise(反转),shortestpath(最短路径) 
        target_angle: 目标角度值(0-360)
        """  
        while (target_angle < 0):  
            target_angle += 360  
        target_angle %= 360  
        target_H = (target_angle >> 8) & 0xFF  
        target_L = target_angle & 0xFF  
        i2c.write(NEZHA_V2_ADDR, bytearray([0xFF, 0xF9, motor, 0x00, 0x5D, target_H, modePostion, target_L]))  
  
    def nezha2MotorStart(self, motor, direction):  
        """  
        启动指定电机并设置转动方向。  
        motor:A,B,C,D     
        direction: clockwise(正转),counterclockwise(反转)        
        """  
        i2c.write(NEZHA_V2_ADDR, bytearray([0xFF, 0xF9, motor, direction, 0x5E, 0x00, 0xF5, 0x00]))  
  
    def nezha2MotorStop(self, motor):  
        """  
        停止指定电机。  
        motor:A,B,C,D      
        """  
        i2c.write(NEZHA_V2_ADDR, bytearray([0xFF, 0xF9, motor, 0x00, 0x5F, 0x00, 0xF5, 0x00]))  
  
    def nezha2MotorSpeedCtrolExport(self, motor, speed):  
        """  
        设置指定电机的速度  
        motor:A,B,C,D       
        speed: 电机速度值（-100-100）。  
        """  
        if speed > 0:  
            direction = 1  # 假设1表示向前  
        else:  
            direction = 2  # 假设2表示向后  
        i2c.write(NEZHA_V2_ADDR, bytearray([0xFF, 0xF9, motor, direction, 0x60, abs(speed), 0xF5, 0x00]))
    def servoPostionReset(self, motor):
        """  
        重置指定伺服电机的位置到初始状态。  
        motor:A,B,C,D       
        """  
        i2c.write(NEZHA_V2_ADDR, bytearray([0xFF, 0xF9, motor, 0x00,0x1D,0x00,0xF5,0x00]))
    def readServoAbsolutePostion(self, motor):
        """  
        读取指定伺服电机的绝对位置。  
        motor:A,B,C,D       
        """  
        i2c.write(NEZHA_V2_ADDR, bytearray([0xFF, 0xF9, motor, 0x00,0x46,0x00,0xF5,0x00]))
        sleep_ms(4)
        arr = i2c.read(NEZHA_V2_ADDR, 4)
        position = (arr[3] << 24) | (arr[2] << 16) | (arr[1] << 8) | (arr[0])
        while (position < 0) :
            position += 3600
        return (position % 3600) * 0.1
    def readServoAbsoluteSpeed(self, motor):
        """  
        读取指定伺服电机的速度。  
        motor:A,B,C,D  
        """  
        i2c.write(NEZHA_V2_ADDR, bytearray([0xFF, 0xF9, motor, 0x00,0x47,0x00,0xF5,0x00]))
        sleep_ms(3)
        ServoSpeed1Arr= i2c.read(NEZHA_V2_ADDR, 2)
        Servo1Speed = (ServoSpeed1Arr[1] << 8) | (ServoSpeed1Arr[0])
        return (Servo1Speed * 0.0926)

if __name__ == '__main__':
    nezha = NEZHA_V2()

# from microbit import *
# from Nezha_V2 import *

# aaa = NEZHA_V2()

# while True:
#     if button_a.was_pressed():
#         aaa.Motorspeed(motor.A,direction.clockwise,100,MotorFunction.degrees)   
#     if button_b.was_pressed():
#         aaa.Motorspeed(motor.A,direction.counterclockwise,100,MotorFunction.degrees)   

# while True:
#     if button_a.was_pressed():
#         aaa.goToAbsolutePosition(motor.A,modePostion.clockwise,100)   
#     if button_b.was_pressed():
#         aaa.goToAbsolutePosition(motor.A,modePostion.clockwise,-100)   

# while True:
#     if button_a.was_pressed():
#         aaa.nezha2MotorStart(motor.A,direction.clockwise)   
#     if button_b.was_pressed():
#         aaa.nezha2MotorStart(motor.A,direction.counterclockwise)   
#     if pin_logo.is_touched():
#         aaa.nezha2MotorStop(motor.A)   

# while True:
#     if button_a.was_pressed():
#         aaa.nezha2MotorSpeedCtrolExport(motor.A,100)   
#     if button_b.was_pressed():
#         aaa.nezha2MotorSpeedCtrolExport(motor.A,-100)   
#     if pin_logo.is_touched():
#         aaa.nezha2MotorStop(motor.A)   

# while True:
#     if button_a.was_pressed():
#         aaa.Motorspeed(motor.A,direction.clockwise,100,MotorFunction.degrees)   
#     if button_b.was_pressed():
#         aaa.Motorspeed(motor.A,direction.counterclockwise,100,MotorFunction.degrees)   
#     if pin_logo.is_touched():
#         display.show(aaa.readServoAbsolutePostion(motor.A)  )

# while True:
#     if button_a.was_pressed():
#         aaa.nezha2MotorSpeedCtrolExport(motor.A,100)   
#     if button_b.was_pressed():
#         aaa.nezha2MotorSpeedCtrolExport(motor.A,-100)   
#     if pin_logo.is_touched():
#         display.show(aaa.readServoAbsoluteSpeed(motor.A)  )

# while True:
#     if button_a.was_pressed():
#         aaa.Motorspeed(motor.A,direction.clockwise,100,MotorFunction.degrees)   
#     if button_b.was_pressed():
#         aaa.Motorspeed(motor.A,direction.counterclockwise,100,MotorFunction.degrees)   
#     if pin_logo.is_touched():
#         aaa.servoPostionReset(motor.A) 

         

