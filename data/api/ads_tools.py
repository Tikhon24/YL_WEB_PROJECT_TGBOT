import random
import string
from ..ads import Ads


class EmptyRequest(Exception):
    pass


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

    def get_ad_by_id(self) -> dict:
        ad = self.db_sess.query(Ads).filter(Ads.ads_id == self.get_ad_id()).first()
        data = {
            'title': ad.title,
            'description': ad.description,
            'price': ad.price,
            'image': ad.image,
            'date': ad.date,
            'user_tag': ad.user_tag,
            'user_id': ad.user_id,
            'ads_id': ad.ads_id,
            'message_id': ad.message_id
        }
        return data

    def find_ad_id(self) -> bool:
        ad = self.db_sess.query(Ads).filter(Ads.ads_id == self.get_ad_id()).first()
        if ad:
            return True
        return False


class AdsDelete(AdsMaster):
    """Операции удаления в бд"""

    def delete_ad(self):
        """Удаление определенного объявления по айди товара"""
        try:
            if not self.db_sess.query(Ads).filter(Ads.ads_id == self.get_ad_id()).first():
                return False
            self.db_sess.query(Ads).filter(Ads.ads_id == self.get_ad_id()).delete()
            self.db_sess.commit()
            return True
        except Exception as ex:
            print(ex)
            return False


class AdsPut(AdsMaster):
    pass


class AdsGet(AdsMaster):
    """Операции по возврату объявлений из бд"""

    def get_by_title(self, title):
        """Возвращает все объявления с указанным названием"""
        try:
            ads = self.db_sess.query(Ads).filter(Ads.title == title).all()
            result = [item.to_dict() for item in ads]
            if not result:
                raise EmptyRequest('EMPTY')
            return {
                'ads': result,
                'status': 'OK'
            }
        except EmptyRequest as er:
            print('Error:', er)
            return {'status': er, 'ads': []}
        except Exception as ex:
            print('Error:', ex)
            return {'status': 'ERROR', 'ads': []}

    def get_by_price(self, price):
        """Возвращает все объявления с указанной ценой"""
        try:
            ads = self.db_sess.query(Ads).filter(Ads.price == price).all()
            result = [item.to_dict() for item in ads]
            if not result:
                raise EmptyRequest('EMPTY')
            return {
                'ads': result,
                'status': 'OK'
            }
        except EmptyRequest as er:
            print('Error:', er)
            return {'status': er, 'ads': []}
        except Exception as ex:
            print('Error:', ex)
            return {'status': 'ERROR', 'ads': []}

    def get_by_user_id(self, user_id):
        """Возвращает все объявления по айди пользователя"""
        try:
            ads = self.db_sess.query(Ads).filter(Ads.user_id == user_id).all()
            result = [item.to_dict() for item in ads]
            if not result:
                raise EmptyRequest('EMPTY')
            return {
                'ads': result,
                'status': 'OK'
            }
        except EmptyRequest as er:
            print('Error:', er)
            return {'status': er, 'ads': []}
        except Exception as ex:
            print('Error:', ex)
            return {'status': 'ERROR', 'ads': []}
