from flask import Flask
from data import db_session
from data.ads import Ads

app = Flask(__name__)


def main():
    db_session.global_init("db/ads.db")


if __name__ == '__main__':
    main()
    app.run()
