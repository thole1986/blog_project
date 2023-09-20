from flask import jsonify
from apps.constant.common import SUCCESS_CODE
from apps.controllers.common import common
from apps.models import Province, District
from apps.utils.location import cached_provinces


@common.route('/zone/province/', methods=['GET'])
def province_list():
    return jsonify({
        'status_code': SUCCESS_CODE,
        'data': [{'id': str(province.id), 'text': province.name}
                 for province in cached_provinces],
    })


@common.route('/zone/district/<province_id>/', methods=['GET'])
def district_list(province_id):
    try:
        province = Province.objects.get(id=province_id)
    except Exception:
        return jsonify({
            'status_code': SUCCESS_CODE,
            'data': []
        })
    else:
        return jsonify({
            'data': [{'id': str(district.id), 'text': district.name}
                     for district in province.districts],
            'status_code': SUCCESS_CODE,
        })


@common.route('/zone/ward/<district_id>/', methods=['GET'])
def ward_list(district_id):
    try:
        district = District.objects.get(id=district_id)
    except Exception:
        return jsonify({
            'status_code': SUCCESS_CODE,
            'data': []
        })
    else:
        return jsonify({
            'data': [{'id': str(ward.id), 'text': ward.name}
                     for ward in district.wards],
            'status_code': SUCCESS_CODE,
        })
