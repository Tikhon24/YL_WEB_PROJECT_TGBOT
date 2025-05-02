from flask import jsonify

import random
import string
from ..ads import Ads


class AdsMaster:
    """Класс для некоторой работы с таблицей ads.
    Позволяет создавать айди объявления, и искать объявление по айди"""

    def __init__(self, db_sess, id=''):
        self.ad_id = id
        self.db_sess = db_sess

    def create_ad_id(self) -> str:
        length = 10
        characters = string.ascii_letters + string.digits
        self.set_ad_id(''.join(random.choice(characters) for _ in range(length)))
        return self.get_ad_id()

    def get_ad_id(self) -> str:
        return self.ad_id

    def set_ad_id(self, id):
        self.ad_id = id

    def get_ad_by_id(self):
        ad = self.db_sess.query(Ads).filter(Ads.ads_id == self.get_ad_id()).first()
        data = {
            'title': ad.title,
            'description': ad.description,
            'price': ad.price,
            'image': ad.image,
            'date': ad.date,
            'user_tag': ad.user_tag,
            'ads_id': ad.ads_id,
            'message_id': ad.message_id
        }
        return jsonify(data)

    def find_ad_id(self) -> bool:
        ad = self.db_sess.query(Ads).filter(Ads.ads_id == self.get_ad_id()).first()
        if ad:
            return True
        return False


class AdsDelete(AdsMaster):
    pass


class AdsPut(AdsMaster):
    pass
