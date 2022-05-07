# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['SchemaTest::test_get_portfolios 1'] = {
    'data': {
        'users': [
            {
                'email': 'davis@gmail.com',
                'username': 'davisphem'
            }
        ]
    }
}

snapshots['SchemaTest::test_get_portfolios first output'] = {
    'data': {
        'users': [
            {
                'email': 'davis@gmail.com',
                'username': 'davisphem'
            }
        ]
    }
}

snapshots['SchemaTest::test_get_portfolios_resolver 1'] = {
    'data': {
        'users': [
            {
                'email': 'davis@gmail.com',
                'username': 'davisphem'
            }
        ]
    }
}
