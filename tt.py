from flask import Flask, request

app = Flask(__name__)

@app.route('/start', methods=['POST'])
def handle_start():
    # Handle the /start command here
    # Your logic goes here
    return 'OK'

if __name__ == '__main__':
    app.run()
