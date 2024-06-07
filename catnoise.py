from playsound import playsound
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/hissing', methods=['GET'])
def cat_noise():
    playsound('hissing.mp3')
    return "STRING"

if __name__ == '__main__':
    app.run(debug=True, port=8080)
