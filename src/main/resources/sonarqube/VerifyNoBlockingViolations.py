#
# Copyright 2021 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
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

sonar_server_api_url = sonarUrl + '/api/resources?resource=%s&metrics=%s' % (resource, ','.join(metrics))

if branch is not None and len(branch) > 0:
    sonar_server_api_url = sonar_server_api_url+'&branch='+branch

if pullRequest is not None and len(pullRequest) > 0:
    sonar_server_api_url = sonar_server_api_url+'&pullRequest='+pullRequest

print (sonar_server_api_url)

sonarResponse = XLRequest(sonar_server_api_url, 'GET', content, credentials['username'], credentials['password'],
                          'application/json').send()
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

print "Metrics: blocking_violations=%s major_violations=%s sqale_index=%s\n" % (
blocking_violations, major_violations, sqale_index)

#
# blocking_violations 0
# major_violations 0
# sqale_index < 3000
#
if blocking_violations == 0 and major_violations < 351 and sqale_index < 9000:
    print "pass\n"
else:
    print "fail\n"
    sys.exit(1)
