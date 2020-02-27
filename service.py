#!usr/bin/python

from flask import Flask, jsonify, request, abort, Response
import flipdot
import time

app = Flask(__name__)
panel = flipdot.flipdot()

@app.route('/flip/api/v1/panel', methods=['POST'])
def write_string():
    if not request.json:
        abort(400)

    if 'type' in request.json:
        transitionType = request.json['transition-type'] if 'transition-type' in request.json else None
        justification = request.json['justification'] if 'justification' in request.json else None
        message = request.json['message'] if 'message' in request.json else None

        if request.json['type'] == 'string':
            pass

        if request.json['type'] == 'time':
            if message is None:
                message = time.strftime("%H:%M %A")
            else:
                message = time.strftime(message)

        panel.write_string(string=message, transitionType=transitionType, justification=justification)

        return Response(status=200)
    else:
        abort(400)

@app.route('/flip/api/v1/panel/clear', methods=['GET'])
def clear_panel():
    panel.clear_panel()
    return Response(status=200)

if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0')
    app.run(host='0.0.0.0')
