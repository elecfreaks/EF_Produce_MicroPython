from microbit import *


class IOT(object):

    def __init__(self, TX_pin=pin8, RX_pin=pin12):
        self.mqttRecv=""
        uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=TX_pin, rx=RX_pin)
        self.__sendAT("AT+RESTORE", 1000)
        self.__sendAT("AT+RST", 1000)
        self.__sendAT("AT+CWMODE=1", 500)
        self.__sendAT("AT+SYSTIMESTAMP=1634953609130", 100)
        self.__sendAT("AT+CIPSNTPCFG=1,8,'ntp1.aliyun.com','0.pool.ntp.org','time.google.com'", 100)
        self.__userToken = ""
        self.__topic = ""
        self.__iftttkey = ""
        self.__iftttevent = ""
        while uart.any():
            uart.read()

    def __sendAT(self, command: str, wait: int = 0):
        uart.write(command + "\u000D\u000A")
        sleep(wait)

    def __waitResponse(self):
        uart_str = ""
        timeOut = running_time()
        while True:
            if uart.any():
                uart_str = str(uart.read(), 'UTF-8') + uart_str
                if "WIFI GOT IP" in uart_str:
                    return True
                elif "OK" in uart_str:
                    return True
                elif "FAIL" in uart_str:
                    return False
                elif "CONNECT" in uart_str:
                    return True
                elif len(uart_str) > 60:
                    uart_str = " "
            elif running_time() - timeOut > 8000:
                return False

    def __ConfirmResponse(self,receiveData,times=3000):
        uart_str = ""
        timeOut = running_time()
        while True:
            if uart.any():
                sleep(100)
                uart_str = str(uart.read(), 'UTF-8') + uart_str
                if receiveData in uart_str:
                    return True
                elif len(uart_str) > 60:
                    uart_str = " "
            elif running_time() - timeOut > times:
                return False

    def connectWIFI(self, ssid: str, pw: str):
        self.__sendAT("AT+CWJAP=\"" + ssid + "\",\"" + pw + "\"", 500)
        return self.__waitResponse()

    def connectThingSpeak(self):
        text = "AT+CIPSTART=\"TCP\",\"api.thingspeak.com\",80"
        self.__sendAT(text, 500)
        return self.__waitResponse()

    def uploadThingSpeak(self, write_api_key: str, n1: int = 0, n2: int = 0, n3: int = 0, n4: int = 0, n5: int = 0, n6: int = 0, n7: int = 0, n8: int = 0):
        toSendStr = "GET /update?api_key=" + write_api_key + "&field1=" + str(n1) + "&field2=" + str(n2) + "&field3=" + str(
            n3) + "&field4=" + str(n4) + "&field5=" + str(n5) + "&field6=" + str(n6) + "&field7=" + str(n7) + "&field8=" + str(n8)
        self.__sendAT("AT+CIPSEND="+str(len(toSendStr)+2), 500)
        self.__sendAT(toSendStr, 100)
        return self.__waitResponse()

    def connectKidsiot(self, userToken:str, topic:str):
        self.__userToken = userToken
        self.__topic = topic
        self.__sendAT("AT+CIPSTART=\"TCP\",\"139.159.161.57\",5555", 5000)
        toSendStr = "{\"topic\":\"" + self.__topic + "\",\"userToken\":\"" + self.__userToken + "\",\"op\":\"init\"}"
        self.__sendAT("AT+CIPSEND="+str(len(toSendStr)+2), 500)
        self.__sendAT(toSendStr, 100)
        return self.__waitResponse()

    def uploadKidsiot(self,data:str):
        toSendStr = "{\"topic\":\"" + self.__topic + "\",\"userToken\":\"" + self.__userToken + "\",\"op\":\"up\",\"data\":\"" + data + "\"}"
        self.__sendAT("AT+CIPSEND="+str(len(toSendStr)+2), 500)
        self.__sendAT(toSendStr, 100)

    def disconnectKidsiot(self):
        toSendStr = "{\"topic\":\"" + self.__topic + "\",\"userToken\":\"" + self.__userToken + "\",\"op\":\"close\"}"
        self.__sendAT("AT+CIPSEND="+str(len(toSendStr)+2), 500)
        self.__sendAT(toSendStr, 100)

    def kidsiotSwitchOn(self):
        uart_str = ""
        timeOut = running_time()
        while True:
            if uart.any():
                uart_str = str(uart.read(), 'UTF-8') + uart_str
                if "switchon" in uart_str:
                    return True
            elif running_time() - timeOut > 3000:
                return False

    def kidsiotSwitchOff(self):
        uart_str = ""
        timeOut = running_time()
        while True:
            if uart.any():
                uart_str = str(uart.read(), 'UTF-8') + uart_str
                if "switchoff" in uart_str:
                    return True
            elif running_time() - timeOut > 3000:
                return False

    def setMQTT(self,scheme:str,clientID:str,username:str,password:str,path=""):
        self.__sendAT("AT+MQTTUSERCFG=0,"+scheme+",\""+clientID+"\",\""+username+"\",\""+password+"\",0,0,\""+path+"\"")
        return self.__waitResponse()

    def connectMQTT(self,host:str,port:str,reconnect="0"):
        self.__sendAT("AT+MQTTCONN=0,\""+host+"\","+port+","+reconnect)
        return self.__waitResponse()

    def subscriptionMQTT(self,Topic:str,Qos:str):
        self.__sendAT("AT+MQTTSUB=0,\""+Topic+"\","+Qos)
        self.__sendAT("AT+MQTTSUB=0,\""+Topic+"\","+Qos)
        return self.__waitResponse()

    def publishMqttMessage(self,msg:str,topic:str,Qos:str):
        self.__sendAT("AT+MQTTPUB=0,\""+topic+"\",\""+msg+"\","+Qos+",0")
        return self.__waitResponse()

    def receiveMqttMessage(self):
        uart_str = ""
        timeOut = running_time()
        while True:
            if uart.any():
                sleep(100)
                uart_str = str(uart.read(), 'UTF-8') + uart_str
                if "+MQTTSUBRECV" in uart_str:
                    #self.mqttRecv = uart_str[uart_str.rfind(","):]
                    #self.mqttRecv = uart_str
                    self.mqttRecv = uart_str[uart_str.rfind(",")+1:-2]
                    return True
            elif running_time() - timeOut > 1000:
                return False

    def setIFTTT(self,key:str,event:str):
        self.__iftttkey = key
        self.__iftttevent = event

    def postIFTTT(self,value1:str,value2:str,value3:str):
        sendST1 = "AT+HTTPCLIENT=3,1,\"http://maker.ifttt.com/trigger/"+__iftttevent+"/with/key/"+__iftttkey+"\",,,2,"
        sendST2 = "\"{\\\"value1\\\":\\\"" + value1 + "\\\"\\\,\\\"value2\\\":\\\"" + value2 + "\\\"\\\,\\\"value3\\\":\\\"" + value3 + "\\\"}\""
        sendST = sendST1 + sendST2
        self.__sendAT(sendST,1000)
        return self.__waitResponse()


if __name__ == '__main__':
    iot = IOT()
    if iot.connectWIFI("ELECFREAKS_2.4G","elecfreaks2019"):
        display.show(Image.YES)
        sleep(2000)
        if iot.setMQTT("2","clientId-erMh5AVlhO","abccd","123456789abcA"):
            display.show("1")
            sleep(1000)
            if iot.connectMQTT("91ff93d955334349a85fc784d8b98eda.s2.eu.hivemq.cloud","8883"):
                display.show("2")
                sleep(1000)
                if iot.subscriptionMQTT("testtopic/1","1"):
                    iot.subscriptionMQTT("testtopic/1","1")
                    display.show("3")
                    sleep(1000)
                    while True:
                        if iot.receiveMqttMessage():
                            display.scroll(iot.mqttRecv)
                            uart.write(iot.mqttRecv + "\u000D\u000A")
                            sleep(1000)
                            display.show(Image.HEART)
                        else:
                            display.show("w")
                else:
                    display.show("error3")
                    sleep(1000)
            else:
                display.show("error2")
            sleep(1000)
        else:
            display.show("error1")
            sleep(1000)
        display.show(Image.COW)
    else:
        display.show(Image.NO)

