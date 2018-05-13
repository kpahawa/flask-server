from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from json import dumps
import os
import RPi.GPIO as GPIO
from time import sleep
from services.motor_runner import MotorRunner

app = Flask(__name__)
json_obj = None
list_of_drinks = ['rum', 'coke', 'sprite', 'vodka', 'water']

## All back row with the 5V ones.
_PIN1 = 21  # pin 29
_PIN2 = 19  # pin 24
_PIN3 = 12  # pin 26
_PIN4 = 13

_PIN_LIST = [_PIN1, _PIN2, _PIN3]

drink_hash = {
    "rum": _PIN1,
    "coke": _PIN2,
    "vodka": _PIN3,
    "sprite": _PIN4
}


def _setup():
    GPIO.setmode(GPIO.BCM)
    # Set relay pins as output
    GPIO.setup(_PIN1, GPIO.OUT)
    GPIO.setup(_PIN2, GPIO.OUT)
    GPIO.setup(_PIN3, GPIO.OUT)
    #GPIO.setup(_PIN4, GPIO.OUT)


@app.route('/test_server', methods=['GET'])
def test_server():
    while True:
        # Turn all relays ON
        print("Entered true")
        GPIO.output(26, 1)
        print("set to high")
        # Sleep for 5 seconds
        sleep(5)
        # Turn all relays OFF
        GPIO.output(26, GPIO.LOW)
        print("set to low")
        # Sleep for 5 seconds
        sleep(5)
        break

    return dumps("Ran the server command")

@app.route('/make_drink', methods=['GET', 'POST'])
def make_drink():
    _setup()
    msg_body = request.form['Body']
    print("entered make drink with body {}".format(msg_body))
    drinks_found = []
    valid_order = False
    for drink in list_of_drinks:
        if drink in msg_body.lower():
            valid_order = True
            drinks_found.append(drink)
    resp = MessagingResponse()
    a = ''
    drinks_to_make = []
    if len(drinks_found) > 0:
        for drink_idx in range(len(drinks_found)):
            drink = drinks_found[drink_idx]
            drinks_to_make.append(drink_hash.get(drink.lower()))

            if drink_idx != len(drinks_found) - 1:
                a += drink + ' with '
        a += drinks_found[-1]

    if valid_order:
        resp.message("you requested a {}".format(a))
        print("valid order is {}".format(valid_order))

        MotorRunner.run_motor(drinks_to_make)
    else:
        resp.message("Your order is not a valid order")
    GPIO.cleanup()
    return str(resp)


@app.route('/twilio', methods=['POST'])
def sms():
    global json_obj
    message_body = request.form['Body']
    resp = MessagingResponse()
    keyWord = message_body
    commands = ["stop", "st", "pause", "p", "stp", "pa", "stop video", "pause video", "play", "resume"]
    if keyWord.lower().strip() in commands:
        json_obj = dumps({"isUrl": "false", "keyword": keyWord.lower().strip()})
    elif keyWord[:4] == "http":
        json_obj = dumps({"isUrl": "true", "url": keyWord})
    else:
        a_list = keyWord.split(" ")
        searchedVideo = ""
        for word in a_list[1:]:
            searchedVideo += word + " "
        listOfWords = [a_list[0], searchedVideo]
        if listOfWords[1][0:4] == "http":
            json_obj = dumps({"isUrl": "true", "url": listOfWords[1].strip()})
        else:
            json_obj = dumps({"isUrl": "false", "keyword": listOfWords[1].strip()})
    print(json_obj)
    return str(resp)


@app.route('/messageBody', methods=['GET'])
def returnKeyWords():
    global json_obj
    if json_obj is None:
        # print((dumps(None) is 'null'))
        return dumps(None)
    returned_obj = json_obj
    json_obj = None
    return returned_obj


@app.route('/', methods=['GET'])
def welcome():
    return 'Welcome!'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
