import config
from app.helpers.imagesource import login
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from flask_restful import Api
from app.resources import images_blueprint
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(import_name='Qute')
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

limiter = Limiter(app, key_func=get_remote_address)

def main():
    login()

    app.register_blueprint(images_blueprint, url_prefix="/api/v1/images")
    app.run(host="0.0.0.0", port=config.port)

@app.errorhandler(429)
def ratelimit_handler(e):
    return make_response(
        jsonify(code=429, error="API ratelimit exceeded %s" % e.description)
        , 429
    )

if __name__ == '__main__':
    main()
