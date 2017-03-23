#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
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
sonarServerAPIUrl = '/api/measures/component?componentKey=%s&metricKeys=%s' % (resource,','.join(metrics.keys()))
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
