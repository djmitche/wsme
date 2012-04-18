# encoding=utf8

import datetime
import unittest

from wsme import WSRoot
from wsme.protocols import getprotocol, CallContext
from wsme.protocols.commons import from_param, from_params

from wsme.types import UserType, Unset


class MyUserType(UserType):
    basetype = str


class TestProtocolsCommons(unittest.TestCase):
    def test_from_param_date(self):
        assert from_param(datetime.date, '2008-02-28') == \
            datetime.date(2008, 02, 28)

    def test_from_param_time(self):
        assert from_param(datetime.time, '12:14:56') == \
            datetime.time(12, 14, 56)

    def test_from_param_datetime(self):
        assert from_param(datetime.datetime, '2009-12-23T12:14:56') == \
            datetime.datetime(2009, 12, 23, 12, 14, 56)

    def test_from_param_usertype(self):
        assert from_param(MyUserType(), 'test') == 'test'

    def test_from_params_empty(self):
        assert from_params(str, {}, '') is Unset
        
    def test_from_params_native_array(self):
        class params(dict):
            def getall(self, path):
                return ['1', '2']
        p = params({'a': []})
        assert from_params([int], p, 'a') == [1, 2]

    def test_from_params_empty_array(self):
        assert from_params([int], {}, 'a') is Unset

    def test_from_params_dict(self):
        assert from_params({int: str}, {
                'a[2]': 'a2', 'a[3]': 'a3'}, 'a') == \
            {2: 'a2', 3: 'a3'}

    def test_from_params_dict_unset(self):
        assert from_params({int: str}, {}, 'a') is Unset