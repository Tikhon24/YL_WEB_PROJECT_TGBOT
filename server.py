from flask import Flask
from flask import make_response, jsonify
from data import db_session, ads_api

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


def main():
    db_session.global_init("db/ads.db")
    app.register_blueprint(ads_api.blueprint)


if __name__ == '__main__':
    main()
    app.run()
