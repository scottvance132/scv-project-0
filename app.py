from controller.customer_controller import cc
from controller.acc_controller import ac
from flask import Flask

if __name__ == '__main__':
    app = Flask(__name__)

    app.register_blueprint(cc)
    app.register_blueprint(ac)

    app.run(port=8080, debug=True)
