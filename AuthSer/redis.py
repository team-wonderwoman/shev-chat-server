# -*- coding: utf-8 -*-
from django.core.cache import cache
from common.const import const_value

# 레디스 get, set, delete, expire

def redis_exists(key):
    if key in cache:
        return True
    else:
        return False

def redis_get(key):
    value = cache.get(key)
    return value

def redis_set(key, value):
    cache.set(key, value)
    return

def redis_delete(key):
    cache.delete(key)
    return

def redis_expire(key):
    cache.expire(key, const_value['TTL'])
    return