from django.http import JsonResponse


class APIResult(JsonResponse):
    def __init__(self, data, message=''):
        assert isinstance(data, (list, dict))

        result = {
            'result': True,
            'code': 200,
            'data': data,
            'message': message
        }

        super(APIResult, self).__init__(result)


class APIServerError(JsonResponse):
    def __init__(self, message=''):
        result = {
            'code': 500,
            'message': message
        }

        super(APIServerError, self).__init__(result)