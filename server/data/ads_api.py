import flask
from flask import request, make_response, jsonify

from data import db_session
from data.ads import Ads

import random
import string

blueprint = flask.Blueprint(
    'ads_api',
    __name__
)


class AdsMaster():
    def __init__(self, id=''):
        self.ad_id = id
        self.db_sess = db_session.create_session()

    def create_ad_id(self) -> str:
        length = 10
        characters = string.ascii_letters + string.digits
        self.set_ad_id(''.join(random.choice(characters) for _ in range(length)))
        return self.get_ad_id()

    def get_ad_id(self) -> str:
        return self.ad_id

    def set_ad_id(self, id):
        self.ad_id = id

    def find_ad_id(self) -> bool:
        if self.db_sess.query(Ads).filter(Ads.ads_id == self.get_ad_id()).first():
            return True
        return False


@blueprint.route('/add_ad', methods=['POST'])
def add_ad():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    db_sess = db_session.create_session()


@blueprint.route('/get_ad_id', methods=['GET'])
def get_ad_id():
    master = AdsMaster()
    ad_id = master.create_ad_id()
    while master.find_ad_id():
        ad_id = master.create_ad_id()
    return jsonify({'ad_id': ad_id})


if __name__ == '__main__':
    db_session.global_init("db/ads.db")
    master = AdsMaster()
    ad_id = master.create_ad_id()
    print(ad_id)
