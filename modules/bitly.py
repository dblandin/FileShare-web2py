#!/usr/bin/env python
# coding: utf8
from gluon import *
#!/usr/bin/python
# use bit.ly's URL shortener
# requires urllib, urllib2, re, simplejson
 
try:
  from re import match
  from urllib2 import urlopen, Request, HTTPError
  from urllib import urlencode
  from simplejson import loads
except ImportError, e:
  raise Exception('Required module missing: %s' % e.args[0])
 
user = "dblandin"
apikey  = "R_58a1f017ea8e85f5dbe4108feb1eac5d"
 
def expand(url):
  try:
    params = urlencode({'shortUrl': url, 'login': user, 'apiKey': apikey, 'format': 'json'})
    req = Request("http://api.bit.ly/v3/expand?%s" % params)
    response = urlopen(req)
    j = loads(response.read())
    if j['status_code'] == 200:
      return j['data']['expand'][0]['long_url']
    raise Exception('%s'%j['status_txt'])
  except HTTPError, e:
    raise('HTTP Error%s'%e.read())
 
def shorten(url):
  try:
    params = urlencode({'longUrl': url, 'login': user, 'apiKey': apikey, 'format': 'json'})
    req = Request("http://api.bit.ly/v3/shorten?%s" % params)
    response = urlopen(req)
    j = loads(response.read())
    if j['status_code'] == 200:
      return j['data']['url']
    raise Exception('%s'%j['status_txt'])
  except HTTPError, e:
    raise('HTTP error%s'%e.read())
 
if __name__ == '__main__':
  from sys import argv
  if not match('http://',argv[1]):
    raise Exception('URL must start with "http://"')
  print shorten(argv[1])
