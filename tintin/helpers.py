from bencode import bencode
from hashlib import md5
from datetime import datetime, timedelta
from decimal import Decimal
from functools import wraps

from tintin.errors import GenericError


def cached_property(method):
    @wraps(method)
    def wrapper(self):
        name = method.__name__
        if name in self.__dict__:
            return self.__dict__[name]
        self.__dict__[name] = result = method(self)
        return result
    return property(wrapper)


def daterange(start_date, end_date):
    """
    Returns datetime objects iterator for requested range
    :param start_date: %d.%m.%Y (for ex. 01.12.2014)
    :param end_date: %d.%m.%Y (for ex. 09.12.2014)
    """
    if not isinstance(start_date, datetime) and not isinstance(end_date, datetime):
        start_date = datetime.strptime(start_date, '%d.%m.%Y')
        end_date = datetime.strptime(end_date, '%d.%m.%Y')
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


def list_to_dict(objects_list, object_key):
    """
    Convert list to dict with selected key. It's useful for many-requests object construction.
    :param objects_list: list of objects
    :param object_key: object unique value
    :return: :rtype: dict with objects
    """
    if not isinstance(objects_list, list):
        try:
            objects_list = list(objects_list)
        except:
            raise BaseException('not a listable object')
    return dict((el.__getattribute__(object_key), el) for el in objects_list)


def query_objects(objects, **kwargs):
    conditions = []
    for k,v in kwargs.iteritems():
        if '__' in k:
            attr, op = k.split('__')
            if op == 'gt':
                conditions.append('Decimal(obj.{0})>Decimal({1})'.format(str(attr), str(v)))
            elif op == 'gte':
                conditions.append('Decimal(obj.{0})>=Decimal({1})'.format(str(attr), str(v)))
            elif op == 'lt':
                conditions.append('Decimal(obj.{0})<Decimal({1})'.format(str(attr), str(v)))
            elif op == 'lte':
                conditions.append('Decimal(obj.{0})<=Decimal({1})'.format(str(attr), str(v)))
            elif op == 'eq':
                conditions.append('obj.{0}=="{1}"'.format(str(attr), str(v)))
            elif op == 'in':
                if isinstance(v, list):
                    conditions.append('set({0}).issubset(obj.{1})'.format(str(v), str(attr)))
        else:
            raise GenericError('condition missing')
    results = []
    query = 'if '+ ' and '.join([c for c in conditions]) +':\n\tresults.append(obj)'
    for obj in objects:
        try:
            exec(query)
        except AttributeError as e:
            raise GenericError(e.message)
    return results


def intersect(*lists):
    result = set(lists[0])
    for x in xrange(1,len(lists)):
        result = result & set(lists[x])
    return list(result)

def object_hash(obj):
    return md5(bencode(str(obj))).hexdigest()
