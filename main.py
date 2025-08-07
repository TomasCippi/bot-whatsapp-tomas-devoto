from flask import Flask, request
from functions.verify_webhook import verify_webhook
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/webhook', methods=['GET'])
def webhook():
    return verify_webhook()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
