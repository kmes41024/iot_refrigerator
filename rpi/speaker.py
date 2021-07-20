from flask import Flask, request
import RPi.GPIO as GPIO
from gtts import gTTS
import os

app = Flask(__name__)

@app.route('/check', methods=['GET'])
def ledcmd():
    if request.method == 'GET':
        cmd = request.args.get('isMax')
        person = request.args.get('name')
        if cmd == '1' :
            tts = gTTS(text=str(person)+'嗓，恭喜你成為本月零食王啦', lang='zh-TW')
            tts.save('snack_tw.mp3')
            os.system('omxplayer -o local -p snack_tw.mp3 > /dev/null 2>&1')
       #print(cmd)
        return "cmd"


if __name__ == '__main__':
    try:
        app.run(host ='0.0.0.0', port = 8000)
    except KeyboardInterrupt:
        print("Exception: KeyboardInterrupt")
    finally:
        print("cleanup")
        GPIO.cleanup()

