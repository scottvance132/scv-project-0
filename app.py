from controller.customer_controller import cc
from flask import Flask

if __name__ == '__main__':
    app = Flask(__name__)

    app.register_blueprint(cc)

    app.run(port=8080)
