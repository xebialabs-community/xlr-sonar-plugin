#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import com.xhaus.jyson.JysonCodec as json

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
metrics = ['blocking_violations', 'major_violations', 'sqale_index'] 

sonarServerAPIUrl = sonarUrl + '/api/resources?resource=%s&metrics=%s' % (resource,','.join(metrics))
print sonarServerAPIUrl

sonarResponse = XLRequest(sonarServerAPIUrl, 'GET', content, credentials['username'], credentials['password'], 'application/json').send()
if sonarResponse.status != RESPONSE_OK_STATUS:
    error = json.loads(sonarResponse.read())
    if 'Invalid table' in error['error']['message']:
        print "Invalid Table Name"
        data = {"Invalid table name"}
        sonarResponse.errorDump()
    else:
        print "Failed to run query in Sonar"
        sonarResponse.errorDump()
    
    sys.exit(1)

json_data = json.loads(sonarResponse.read())

metrics_data = {}
for item in json_data[0]['msr']:
    metrics_data[item['key']] = item['val']

blocking_violations = int(metrics_data.get('blocking_violations', 0))
major_violations = int(metrics_data.get('major_violations', 0))
sqale_index = int(metrics_data.get('sqale_index', 0))

print "Metrics: blocking_violations=%s major_violations=%s sqale_index=%s" % (blocking_violations, major_violations, sqale_index)

#
# blocking_violations 0
# major_violations 0
# sqale_index < 3000
#
if blocking_violations == 0 and major_violations < 351 and sqale_index < 5000:
    print "pass"
else:
    print "fail"
    sys.exit(1)