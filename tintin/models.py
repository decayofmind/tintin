from decimal import Decimal
from pprint import pprint

from bookinganalytics.errors import GenericError
from bookinganalytics.helpers import cached_property


class BaseDTO(object):
    def __init__(self, d):
        self.__dict__ = d

    @property
    def data(self):
        return  self.__dict__

    def to_dict(self):
        return self.data

    def dump(self):
        pprint(self.data)


class BaseCollection(list):
    def __init__(self, *args):
        super(BaseCollection, self).__init__(args)

    def query(self, **kwargs):
        conditions = []
        for k,v in kwargs.iteritems():
            if '__' in k:
                if v != None:
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
        results = BaseCollection()
        if not conditions:
            return self
        query = 'if '+ ' and '.join([c for c in conditions]) +':\n\tresults.append(obj)'
        for obj in self:
            try:
                exec(query)
            except AttributeError as e:
                raise GenericError(e.message)
        return results

    @cached_property
    def first(self):
        return self[0]
