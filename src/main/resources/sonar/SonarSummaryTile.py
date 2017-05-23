#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


import json
from xlrelease.HttpRequest import HttpRequest

if not sonarServer:
    raise Exception("Sonar server ID must be provided")
if not username:
    username = sonarServer["username"]
if not password:
    password = sonarServer["password"]

sonarUrl = sonarServer['url']

credentials = CredentialsFallback(sonarServer, username, password).getCredentials()
content = None
RESPONSE_OK_STATUS = 200
print "Sending content %s" % content
sonarServerAPIUrl = '/api/measures/component?componentKey=%s&metricKeys=%s' % (resource, ','.join(metrics.keys()))
http_request = HttpRequest(sonarServer, credentials['username'], credentials['password'])
sonarResponse = http_request.get(sonarServerAPIUrl)
if sonarResponse.status == RESPONSE_OK_STATUS:
    json_data = json.loads(sonarResponse.getResponse())
    data1 = {}
    data1['id'] = json_data['component']['id']
    data1['key'] = json_data['component']['key']
    data1['name'] = json_data['component']['name']
    data1['sonarUrl'] = sonarUrl
    for item in json_data['component']['measures']:
        data1[item['metric']] = item['value']
    data = data1
else:
    error = json.loads(sonarResponse.getResponse())
    if 'Invalid table' in error['error']['message']:
        print "Invalid Table Name"
        data = {"Invalid table name"}
        sonarResponse.errorDump()
    else:
        print "Failed to run query in Sonar"
        sonarResponse.errorDump()
        sys.exit(1)
