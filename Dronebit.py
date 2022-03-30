from microbit import *
import radio
import music

class DRONE(object):
    #initModule
    master = 0x01
    remote = 0x02

    #Basic_action
    take_off = 0x01
    landing = 0x02

    #Move_action
    Up = 0x10
    Down = 0x11
    Forward = 0x12
    Backward = 0x13
    Left = 0x14
    Right = 0x15

    #Rotation_action
    turn_left = 0x16
    turn_right = 0x17

    #Roll_action
    Roll_forward = 0x20
    Roll_back = 0x21
    Roll_left = 0x22
    Roll_right = 0x23

    heartbeatBuff = bytearray([0xAF,0xFA])

    def __init__(self,radio_channel=7,txPin=pin1,rxPin=pin2):
        uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=txPin, rx=rxPin)
        radio.on()
        radio.config(channel=radio_channel)
        self.__last_time = running_time()


    def heartbeat(self):
        if running_time() - self.__last_time >= 1000:
            uart.write(DRONE.heartbeatBuff)
            self.__last_time = running_time()

    def Drone_sleep(self,time_ms):
        while time_ms > 0:
            self.heartbeat()
            sleep(1)
            time_ms = time_ms - 1

    def __WaitCellback(self):
        self.Drone_sleep(1000)
        rx_buff = bytearray([0x00, 0x00, 0x00])
        uart.readinto(rx_buff)
        self.heartbeat()
        if rx_buff[0] == 0x01 and rx_buff[1] == 0x01:
            radio.send("S")
            return True
        else:
            radio.send("F")
            return False

    def initModule(self,mode):
        self.heartbeat()
        uart.read()
        self.Drone_sleep(1000)
        tx_buff = bytearray([0x00])
        tx_buff[0] = mode
        uart.write(tx_buff)
        self.Drone_sleep(1000)
        rx_buff = bytearray([0x00, 0x00, 0x00])
        uart.readinto(rx_buff)
        self.Drone_sleep(3000)
        while rx_buff[1] == 0x02:
            music.play(music.POWER_DOWN)
            self.Drone_sleep(3000)
        music.play(music.POWER_UP)
        if mode == self.remote:
            for i in range(3):
                display.show(Image(
                "00000:"
                "00000:"
                "00000:"
                "00000:"
                "00900"
                ))
                self.Drone_sleep(300)
                display.show(Image(
                "00000:"
                "00000:"
                "00900:"
                "09090:"
                "00000"
                ))
                self.Drone_sleep(300)
                display.show(Image(
                "09990:"
                "90009:"
                "00000:"
                "00000:"
                "00000"
                ))
                self.Drone_sleep(330)
            display.clear()
        self.heartbeat()

    def UAV_speed(self,power):
        self.heartbeat()
        uart.read()
        tx_buff = bytearray([0xEF, 1, 0x01, 0x03, 0x00])
        tx_buff[4] = power
        uart.write(tx_buff)
        return self.__WaitCellback()

    def Basic_action(self,basicstate):
        self.heartbeat()
        uart.read()
        self.heartbeat()
        if basicstate == DRONE.take_off:
            for i in range(3,-1,-1):
                display.show(i)
                if i == 0:
                    music.play(['g'])
                else:
                    music.set_tempo(ticks=8,bpm=100)
                    music.play(['c4'])
                self.Drone_sleep(1000)
            display.clear()
            tx_buff = bytearray([0xEF, 0, 0x01, 0X01])
            uart.write(tx_buff)
            self.heartbeat()
        elif basicstate == DRONE.landing:
            tx_buff = bytearray([0xEF, 0, 0x01, 0X02])
            uart.write(tx_buff)
        return self.__WaitCellback()

    def Move_action(self,Directionstate,distance):
        self.heartbeat()
        uart.read()
        tx_buff = bytearray([0xEF, 0x00, 0x01, 0x00, 0x00, 0x00])
        tx_buff[3] = Directionstate
        if distance > 255:
            tx_buff[1] = 2
            tx_buff[4] = 255
            tx_buff[5] = distance - 255
        else:
            tx_buff[1] = 1
            tx_buff[4] = distance
            tx_buff[5] = 0
        self.heartbeat()
        uart.write(tx_buff)
        return self.__WaitCellback()

    def Rotation_action(self,rotationstate,angle):
        self.heartbeat()
        uart.read()
        tx_buff = bytearray([0xEF, 0x00, 0x01, 0x00, 0x00, 0x00])
        tx_buff[3] = rotationstate
        if angle > 255:
            tx_buff[1] = 2
            tx_buff[4] = 255
            tx_buff[5] = angle - 255
        else:
            tx_buff[1] = 1
            tx_buff[4] = angle
            tx_buff[5] = 0
        uart.write(tx_buff)
        return self.__WaitCellback()

    def Roll_action(self,rollstate):
        self.heartbeat()
        uart.read()
        tx_buff = bytearray([0xEF, 0, 0x01, 0x00])
        tx_buff[3] = rollstate
        uart.write(tx_buff)
        return self.__WaitCellback()

    def Hovering(self,time):
        self.heartbeat()
        uart.read()
        tx_buff = bytearray([0xEF, 1, 0x01, 0x04, 0x00])
        tx_buff[4] = time
        uart.write(tx_buff)
        self.Drone_sleep(time*1000)
        return self.__WaitCellback()

    def Get_voltage(self):
        self.heartbeat()
        uart.read()
        tx_buff = bytearray([0xEF, 0, 0x02, 0x01])
        uart.write(tx_buff)
        self.Drone_sleep(1000)
        rx_buff = bytearray([0x00, 0x00, 0x00])
        uart.readinto(rx_buff)
        if rx_buff[0] == 0x02:
            return rx_buff[1] + rx_buff[2]
        else:
            return -1

    def Get_height(self):
        self.heartbeat()
        uart.read()
        tx_buff = bytearray([0xEF, 0, 0x02, 0x02])
        uart.write(tx_buff)
        self.Drone_sleep(1000)
        rx_buff = bytearray([0x00, 0x00, 0x00])
        uart.readinto(rx_buff)
        if rx_buff[0] == 0x02:
            return rx_buff[1] + rx_buff[2]
        else:
            return -1

    def Emergency_brake(self):
        self.heartbeat()
        uart.read()
        tx_buff = bytearray([0xEF, 0, 0x01, 0x05])
        uart.write(tx_buff)
        return self.__WaitCellback()


if __name__ == '__main__':
    test = DRONE()
    test.initModule(test.master)
    test.Drone_sleep(1000)
    display.show(Image.HAPPY)
    test.Drone_sleep(1000)

    while(True):
        test.heartbeat()
        if button_a.was_pressed():
            test.Basic_action(test.take_off)
            test.Hovering(3)
            test.Move_action(test.Up,30)
            test.Hovering(2)
            test.Move_action(test.Down,50)
            test.Hovering(2)
            test.Move_action(test.Up,50)
            test.Hovering(2)
            test.Basic_action(test.landing)
            test.Drone_sleep(3000)
        if button_b.was_pressed():
            test.UAV_speed(30)
            test.Basic_action(test.take_off)
            test.Hovering(3)
            test.Rotation_action(test.turn_right,320)
            test.Hovering(2)
            test.Rotation_action(test.turn_left,350)
            test.Hovering(2)
            test.Move_action(test.Down,80)
            test.Hovering(2)
            test.Emergency_brake()
            test.Drone_sleep(2000)
            test.Basic_action(test.landing)
            test.Drone_sleep(3000)
