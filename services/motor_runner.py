import threading
import RPi.GPIO as GPIO
from time import sleep


class MotorRunner:
    _POUR_TIME = 5  # seconds

    @staticmethod
    def run_motor(pin_nums: "list[int]"):
        print("pin nums: {}".format(pin_nums))
        threaded_pumps = []

        for pin_num in pin_nums:
            thread = threading.Thread(target=MotorRunner.pour, args=(pin_num,))  # args MUST be a tuple
            threaded_pumps.append(thread)

        for thread in threaded_pumps:
            print("Started threading {}".format(thread.getName()))
            thread.start()

        for thread in threaded_pumps:
            thread.join()

        print("done with threading")

    @staticmethod
    def pour(pin_num: "int"):
        GPIO.output(pin_num, 0)
        sleep(MotorRunner._POUR_TIME)
        GPIO.output(pin_num, 1)

    def test_pour(self):
        print("using GPIO output")

    @staticmethod
    def cleanup():
        GPIO.cleanup()
