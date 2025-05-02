import flask
from flask import request, make_response, jsonify

if __name__ != '__main__':
    # импорты для запуска файла извне
    from data import db_session
    from data.ads import Ads
    from data.api.ads_tools import AdsMaster, AdsDelete, AdsPut

blueprint = flask.Blueprint(
    'ads_api',
    __name__
)


@blueprint.route('/add_ad', methods=['POST'])
def add_ad():
    """Добавляем объявление в бд"""
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    db_sess = db_session.create_session()
    try:
        ad = Ads(
            title=request.json['title'],
            description=request.json['description'],
            price=int(request.json['price']),
            image=request.json['image'],
            user_tag=request.json['user_tag'],
            ads_id=request.json['ads_id'],
            message_id=request.json['message_id']
        )
        db_sess.add(ad)
        db_sess.commit()
        return jsonify({'status': 'OK'})
    except Exception as ex:
        print(ex)
        return jsonify({'status': 'ERROR'})


@blueprint.route('/get_ad_id', methods=['GET'])
def get_ad_id():
    """Создает айди объявлению"""
    db_sess = db_session.create_session()
    master = AdsMaster(db_sess)
    ad_id = master.create_ad_id()
    while master.find_ad_id():
        ad_id = master.create_ad_id()
    return jsonify({'ad_id': ad_id})
