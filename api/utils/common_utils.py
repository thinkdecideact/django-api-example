from datetime import time, date, datetime
import json
from decimal import Decimal
import math


def api_success(m='Successful operation', d='', c=0):
    return tdar_jsonify({'code': c, 'msg': m, 'data': d})


def api_failure(m='Errors occurred', d=None, c=1):
    return tdar_jsonify({'code': c, 'msg': m, 'data': d})


def tdar_jsonify(response_data):
    from django.http import HttpResponse
    if isinstance(response_data, dict) or isinstance(response_data, list):
        response_data = json.dumps(response_data, cls=TdarCustomEncoder)
    return HttpResponse(response_data, content_type='application/json')


class TdarCustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, time):
            return obj.strftime('%H:%M:%S')
        elif isinstance(obj, Decimal):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def get_page_count(row_count, row_count_per_page):
    if (row_count % row_count_per_page) == 0:
        return row_count / row_count_per_page
    else:
        return math.ceil(row_count / row_count_per_page)


def get_token(request):
    return request.META.get("HTTP_X_TOKEN", '')


def create_md5_hash(input_str):
    import hashlib
    md5 = hashlib.md5()
    md5.update(input_str.encode("utf-8"))
    return md5.hexdigest()

