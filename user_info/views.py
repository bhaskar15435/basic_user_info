import json
from django.conf import settings
import redis
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import re

regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

# Connect to our Redis instance
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

@api_view(['GET', 'POST'])
def manage_item(request, *args, **kwargs):
    if request.method == 'GET':
        try:
            key = request.GET.get('email')
            if not key:
                raise Exception('please provide email in api parmas')
            data = redis_instance.get(key)
            if not data:
                raise Exception('no data found')
            response = {
                'email': key,
                'msg': "success",
                'data': json.loads(data)
            }
            return Response(response, status=200)
        except Exception as e:
            response = {
                'error':str(e)
            }
            return Response(response,404)
    elif request.method == 'POST':
        try:
            item = json.loads(request.body)
            validate_body(item)
            email = item['email']
            pre_data = redis_instance.get(email)
            if pre_data is not None:
                raise Exception('email {} already exists'.format(email))
            redis_instance.set(email, request.body)
            response = {
                'msg': f"{email} successfully set to {item}"
            }
            return Response(response, 201)
        except Exception as e:
            response = {
                'msg':f"{str(e)}"
            }
            return Response(response,422)

def validate_body(body):
    if 'name' not in body:
        raise Exception('name key is requierd')

    if 'email' not in body:
        raise Exception('email key is requierd')

    if 'age' not in body:
        raise Exception('age key is requierd')

    if 'occupation' not in body:
        raise Exception('occupation key is required')

    if not body['name']:
        raise Exception('name field should not be empty')

    if not body['occupation']:
        raise Exception('occupation field should not be empty')

    if not check_email(body['email']):
        raise Exception('Invalid Email')

    if type(body['age']) is not int or body['age'] < 0:
        raise Exception('age should be positive integer')

def check_email(email):
    if(re.search(regex, email)):
    	return True
    return False
