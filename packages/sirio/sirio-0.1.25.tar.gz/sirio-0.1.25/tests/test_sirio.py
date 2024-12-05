#!/usr/bin/env python

"""Tests for `sirio` package."""


import unittest
import io

from sirio import event

from   sirio.business_object import BusinessObject, Object

from sirio.service import SirioService

ss = SirioService(host_sirio_ep='https://sirio-engine-backend.srv-test.eu-central-1.aws.cervedgroup.com')
bo = ss.retrieveBo('67063d15abcaec5dc6e87bb9','','')
bo.setOutputTask('miaVal','valoreMiaVal')
ss.completeTask(bo,'ir4','task_id')

ibk = bo.internalBusinessKey
ow = bo.owner


obj = Object('TEST-PASK','pask', extension='json')
stream = io.BytesIO(b"Questo il contenuto del file.")
obj.createByStream(stream)

url_sirio_get_business_object = 'https://sirio-engine-backend.srv-test.eu-central-1.aws.cervedgroup.com/sirio/enginebackend/businessobjects/{businessKey}'
url_sirio_complete = 'https://sirio-engine-backend.srv-test.eu-central-1.aws.cervedgroup.com/sirio/enginebackend/processes/domains/{domain}/tasks/{taskId}'
bo = BusinessObject('67063d15abcaec5dc6e87bb9',url_sirio_get_business_object, url_sirio_complete)
testJson = {'a':'paskA','b':'paskB'}
obj = Object('TEST-PASK','pask', extension='json')
stream = io.BytesIO(b"Questo il contenuto del file.")
obj.createByStream(stream)
bo.uploadObject(obj)
bo.complete('ir4','6316d202-ba63-4785-84ac-a0415e44177e')

class TestSirio(unittest.TestCase):
    """Tests for `sirio` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""
