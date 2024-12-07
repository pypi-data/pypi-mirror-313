'''
Created on 30 Apr 2024

@author: jacklok
'''
from functools import wraps
from flask import request
import logging,json
from flask.globals import session
from trexlib.utils.log_util import get_tracelog
from trexlib.utils.string_util import is_not_empty

logger = logging.getLogger('request_wrapper')

def request_json(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request_json = request.get_json()
        
        request_json = json.loads(json.dumps({**request_json}))
            
        return f(*args, request_json, **kwargs)

    return decorated_function

def request_debug(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logger.debug('------------------------------ request debug start --------------------------------------')
        values = {}
        values.update(request.args)
        values.update(request.form)
        try:
            request_json = request.get_json()
            request_json = json.loads(json.dumps({**request_json}))
            
            values.update(request_json)
        except:
            logger.debug('not json request')
        
        headers = request.headers
        headers = json.loads(json.dumps({**headers}))
        headers = dict((k.lower(), v) for k, v in headers.items())
        
        
        #logger.debug('------------------------------ request debug start --------------------------------------')
        logger.debug('request method=%s', request.method)
        logger.debug('request url=%s', request.url)
        logger.debug('request headers=%s', headers)
        logger.debug('request params=%s', values)
        
        logger.debug('------------------------------ request debug end --------------------------------------')
            
        return f(*args, **kwargs)

    return decorated_function

def request_headers(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        headers = request.headers
        logger.debug('headers before=%s', headers)
        headers = json.loads(json.dumps({**headers}))
        headers = dict((k.lower(), v) for k, v in headers.items())    
        logger.debug('headers after=%s', headers)
        return f(*args, headers, **kwargs)

    return decorated_function

def request_args(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        values = {}
        values.update(request.args)
        
        return f(*args, values, **kwargs)

    return decorated_function

def request_form(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, request.form, **kwargs)

    return decorated_function
        

def request_values(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        values = {}
        try:
            content_type = request.content_type
            values.update(request.args)
            
            logger.debug('request_values debug: content_type=%s', content_type)
            if is_not_empty(content_type):
                if 'application/x-www-form-urlencoded' in content_type:
                    values.update(request.form)
                
                if 'application/json' in content_type:
                    request_json = request.get_json()
                    request_json = json.loads(json.dumps({**request_json}))
                    values.update(request_json)
            
            logger.debug('request_values debug: request_values=%s', request_values)
            
            return f(*args, values, **kwargs)
        except:
            logger.error('request_values debug: Failed due to %s', get_tracelog())
            
            return f(*args, values, **kwargs)
        
    return decorated_function

def request_files(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request_files = request.files
        
        logger.debug('request_files=%s', request_files)
        
        return f(*args, request_files, **kwargs)

    return decorated_function

def session_value(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        return f(*args, session, **kwargs)

    return decorated_function
