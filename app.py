from flask import Flask, request
from twilio import twiml
from json import dumps
app = Flask(__name__)
json_obj = None
@app.route('/twilio', methods=['POST'])
def sms():
    global json_obj
    message_body = request.form['Body']
    resp = twiml.Response()
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
    return('Welcome!')
if __name__ == '__main__':
    app.run()