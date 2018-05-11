import threading
import RPi.GPIO as GPIO
from time import sleep


class MotorRunner:
    _POUR_TIME = 5

    @staticmethod
    def run_motor(pin_nums: "list[int]"):
        threaded_pumps = []

        for pin_num in pin_nums:
            pump_t = threading.Thread(target=MotorRunner.pour, args=(pin_num))
            threaded_pumps.append(pump_t)

        for pump_t in threaded_pumps:
            pump_t.start()

    @staticmethod
    def pour(pin_num: "int"):
        GPIO.output(pin_num, 1)
        sleep(MotorRunner._POUR_TIME)
        GPIO.output(pin_num, GPIO.LOW)
