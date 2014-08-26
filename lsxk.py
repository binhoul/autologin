#!/usr/bin/python

import HTMLParser
import urlparse
import urllib
import urllib2
import cookielib
import string
import re

hosturl = 'http://lsxk.org/wForum/frames.html'
posturl = 'http://lsxk.org/wForum/logon.php'
mailurl = 'http://lsxk.org/wForum/usermailbox.php?boxname=Inbox'


cj = cookielib.CookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)


headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8,text/vnd.wap.wml;q=0.6',
    'Accept-Encoding' : 'gzip, deflate',
    'Accept-Language' : 'en-US,en;q=0.5'
}
postData = {
   'id' : 'saintli86',
   'passwd' : '3569930',
}
postData = urllib.urlencode(postData)
postData = postData + '&post=%B5%C7%C2%BC'
request = urllib2.Request(posturl, postData, headers)
response = opener.open(request)
request = request.add_header('Referer','http://lsxk.org/wForum/usermailbox.php?boxname=inbox')
request = request.add_header('Host','lsxk.org')
request = request.add_header('Connection','keep-alive')
result = opener.open(mailurl)
print result.read().decode('gb2312').encode('utf-8')
