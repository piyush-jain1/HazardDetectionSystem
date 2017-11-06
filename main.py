from flask import Flask, request
import time
import threading

app = Flask(__name__)


@app.route('/Settings', methods=['POST'])
def set_param():
    if (request.form.get('fire', '')):
        fire_detect = 1
    else:
        fire_detect = 0

    if (request.form.get('ear', '')):
        earthquake_detect = 1
    else:
        earthquake_detect = 0

    if (request.form.get('gas', '')):
        gas_detect = 1
    else:
        gas_detect = 0

    print ("OpeningFile")

    with open("./userpref.txt", "w+") as output:
        print ("SettingUserPreferences")
        output.write(str(fire_detect) + " " + str(earthquake_detect) + " " + str(gas_detect))
        print ("PreferenceSet")

    print "updated values : "
    print "set", fire_detect, earthquake_detect, gas_detect
    print "param updated!"
    return 'update successful'


@app.route('/')
def hello_world():
    return "Hello World!"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)


