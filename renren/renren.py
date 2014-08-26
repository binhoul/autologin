#!/usr/bin/python
#-*- coding: utf-8 -*-

import urllib
import urllib2
import cookielib
import re
import zlib
import json


class Renren(object):
    def __init__(self):
        self.operate = ''
#        self.icode = ''
#        self.loginurl = ''
        self.is_login = False

        #header
        self.header = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:23.0) Gecko/20100101 Firefox/23.0',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
        }
        #cookies
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        #requestToken, _rtk, ruid
        self.hostid = ''
        self.requestToken = self._rtk = self.ruid = ''
        self.requestToken_pattern = re.compile(r"get_check:'([-0-9]*)'")
        self._rtk_pattern = re.compile(r"get_check_x:'([a-zA-Z0-9]+)'")
        self.ruid_pattern = re.compile(r"'ruid':'(\d+)'")

    def login(self, email='', password='', origURL=''):
        loginURL = 'http://www.renren.com/PLogin.do'
        postdata = {
            'email': email,
            'password': password,
            'origURL': origURL,
        }
        print 'start login...'
        while not self.is_login:
            self.operate = self._get_response(loginURL, postdata)
            cur_url = self.operate.geturl()
            headers = self.operate.info()
            content_encode = self.operate.headers.get('Content-Encoding')
            if content_encode == 'gzip':
                web_content = zlib.decompress(self.operate.read(), 16+zlib.MAX_WBITS)
            else:
                web_content = self.operate.read()
            self._get_token(web_content)
            if self.ruid:
                self.is_login = True
                print "用户 {0} 登陆成功！".format(self.ruid)


    def publish(self, content):
        loginURL = 'http://shell.renren.com/{0}/status'.format(self.ruid)
        postdata = {
            'content': content,
            'withInfo': '{"wpath":[]}',
            'hostid': self.ruid,
            'privacyParams': '{"sourceControl": 99}',
            'requestToken': self.requestToken,
            '_rtk': self._rtk,
            'channel': 'renren'
        }
        print "start posting..."
        self.operate = self._get_response(loginURL, postdata)
        cur_url = self.operate.geturl()
        content_encode = self.operate.headers.get('Content-Encoding')
        if content_encode == 'gzip':
            web_content = zlib.decompress(self.operate.read(),16+zlib.MAX_WBITS)
        else:
            web_content = self.operate.read()
        json_response = json.loads(web_content)
        if json_response['code'] == 0:
            print '发贴成功了！'
        else:
            print '发贴失败，错误码：{0}'.format(json_response['code']) 

    def _get_response(self, url, data = None):
        if data is not None:
            req = urllib2.Request(url, urllib.urlencode(data), self.header)
        else:
            req = urllib2.Request(url)
        response = self.opener.open(req)
        return response
            
    def _get_token(self, data):
        self.requestToken = self.requestToken_pattern.search(data).group(1)
        self._rtk = self._rtk_pattern.search(data).group(1)
        self.ruid = self.ruid_pattern.search(data).group(1)



