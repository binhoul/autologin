#!/usr/bin/python                                                                                                                                                                             
#-*- coding: utf-8 -*-

import renren
import time
import sys
import os

if len(sys.argv) != 3:
    print '请输入用户名和密码'
    print '格式： python {0} username password'.format(sys.argv[0])
    os._exit(5)
else:
    username = sys.argv[1]
    password = sys.argv[2]

if __name__ == '__main__':
    my_account = renren.Renren()
    my_account.login(username, password)
    my_account.publish('ceshi')
