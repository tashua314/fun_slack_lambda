# -*- coding:utf-8 -*-


def lambda_handler(event, _context):
    """ サンプルファイル """
    text = '%s is %s years old.' % (event['name'], event['age'])
    return text
