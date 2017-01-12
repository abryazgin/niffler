#!/usr/bin/env python
import requests

uri = "testdir/2/somefile.txt"
url = "http://office.rc-online.ru:22788/private/" + uri
headers = {"Authorization": "e8738304de22ffdb812fc151c232af3ee5dd12b557f08d1f"}
headers2 = {"Authorization": "0b202c64e4ba86a0023a5b8a8a3e2a2b31578cc313340813"}
group_name = 'admin_client_group'

data = 'some small text'
# create file
print "UPLOADING"
requests.put(url, headers=headers, data=data)
# get file by owner
print "DOWNLOAD BY OWNER"
resp = requests.get(url, headers=headers)
print resp.text
# get file by other
print "DOWNLOAD BY OTHER (ASSERT 403)"
resp = requests.get(url, headers=headers2)
print resp.text
# share file
print "SHARE TO OTHER"
url_patch = url + '?group=' + group_name
resp = requests.patch(url_patch, headers=headers)
# get file by other
print "DOWNLOAD BY OTHER"
resp = requests.get(url, headers=headers2)
print resp.text
# remove file
print "DELETE"
requests.delete(url, headers=headers)
# get file by owner
print "DOWNLOAD BY OWNER (ASSERT 403)"
resp = requests.get(url, headers=headers)
print resp.text
