from microbit import *
import utime 
  
# 定义引脚枚举  
class JoystickBitPin:  
    P12 = 12  
    P13 = 13  
    P14 = 14  
    P15 = 15  
  
# 定义摇杆方向类型枚举  
class RockerType:  
    X = 1  
    Y = 2  
  
# 假设ButtonType的High和Low对应于引脚上的高电平和低电平  
ButtonType = {  
    'down': 0,  # 低电平表示按下  
    'up': 1     # 高电平表示释放  
}  

class JOYSTICKBIT(object):
      """基本描述

      joystick游戏手柄按键功能

      """ 
      def init_joystick_bit(self):  
            """初始化摇杆位 
            P0设置为低电平(假设这是用于其他目的,如初始化LED或其他功能)
            四个按键初始化为上拉输入模式
            震动马达控制引脚输出高电平，默认关闭状态
            """ 
            pin0.write_digital(0)
            
            # 设置P12, P13, P14, P15为输入并启用上拉电阻  
            pin12.set_pull(pin12.PULL_UP) 
            pin13.set_pull(pin13.PULL_UP) 
            pin14.set_pull(pin14.PULL_UP)   
            pin15.set_pull(pin15.PULL_UP)  
            
            # P16设置为高电平（可能是振动马达的控制引脚）  
            pin16.write_digital(1) 
      
      def get_button(self,button):  
            """ 
            button:传入按键编号(P12,P13,P14,P15)
            检测对应编号按键有没有按下
            按下则返回状态True,否则返回状态False
            """ 
            pin = 1
            if button == JoystickBitPin.P12:
                pin12.set_pull(pin12.PULL_UP)
                pin = pin12.read_digital()
            elif button == JoystickBitPin.P13:
                pin13.set_pull(pin13.PULL_UP)
                pin = pin13.read_digital()
            elif button == JoystickBitPin.P14:
                pin14.set_pull(pin14.PULL_UP)
                pin = pin14.read_digital()
            elif button == JoystickBitPin.P15:
                pin15.set_pull(pin15.PULL_UP)
                pin = pin15.read_digital()
            return not pin  # 返回True如果按钮被按下（低电平），否则返回False  
                
      def on_button_event(self,button, event_type, handler):  
            """ 
            button:传入按键编号(P12,P13,P14,P15)
            event_type:按键状态
            handler:条件执行函数
            检测对应编号按键此时的状态,若达到判断标准则执行handler
            """  
            if JOYSTICKBIT.get_button(self,button) == (event_type == ButtonType['down']):  
                  handler()  
         
      def get_rocker_value(self,rocker):  
            """ 
            rocker:传入遥感方向
            检测当前遥感对应X轴Y轴上的模拟战,即使用模拟战表示遥感在处在哪个方位
            """   
            if rocker == RockerType.X:   # P1是摇杆X的模拟输入   # 设置ADC分辨率  
                  return pin1.read_analog()   # 读取模拟值  
            elif rocker == RockerType.Y:   # P2是摇杆Y的模拟输入  # 设置ADC分辨率  
                  return pin2.read_analog()  # 读取模拟值  
            else:  
                  return 0  
       
      def vibration_motor(self,time_ms): 
            """ 
            time_ms:时间量,单位为毫秒
            控制震动马达震动time_ms毫秒
            """   
            pin16.write_digital(0) # 启动振动马达  
            utime.sleep_ms(time_ms)  # 等待指定的毫秒数  
            pin16.write_digital(1)  # 停止振动马达  
            
            # 示例用法：  
            # init_joystick_bit()  
            # print(get_button(JoystickBitPin.P12))  
            # on_button_event(JoystickBitPin.P13, ButtonType['down'], lambda: display.show(Image.YES)))  
            # print(get_rocker_value(RockerType.X))  
            # vibration_motor(500)  # 振动500毫秒

joystickbit = JOYSTICKBIT()


if __name__ == '__main__':
     
      joystickbit.init_joystick_bit()
      # JOYSTICKBIT.get_button(JoystickBitPin.P12)
      # JOYSTICKBIT.on_button_event(JoystickBitPin.P12,ButtonType['down'],lambda: display.show(Image.YES))
      # JOYSTICKBIT.get_rocker_value(RockerType.X)
      # JOYSTICKBIT.vibration_motor(100)
