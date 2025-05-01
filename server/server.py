from flask import Flask
from data import db_session, ads_api
from data.ads import Ads

app = Flask(__name__)


def main():
    db_session.global_init("db/ads.db")
    app.register_blueprint(ads_api.blueprint)


if __name__ == '__main__':
    main()
    app.run()
