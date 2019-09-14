#
# Copyright 2019 XEBIALABS
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

sonar_server_api_url = '/api/measures/component?componentKey=%s&metricKeys=complexity,line_coverage,duplicated_lines_density,violations' % resource
http_request = HttpRequest(sonarServer, username, password)
sonar_response = http_request.get(sonar_server_api_url)
if not sonar_response.isSuccessful():
    raise Exception("Failed to get Sonar Measures. Server return [%s], with content [%s]" % (sonar_response.status, sonar_response.response))
json_data = json.loads(sonar_response.getResponse())
data = {}
for item in json_data['component']['measures']:
    data[item['metric']] = item['value']

error_message = ""
if lineCoverage > -1 and 'line_coverage' in data and lineCoverage > float(data["line_coverage"]):
    error_message += "+ Did not meet line coverage requirement. Received %s\n" % data["line_coverage"]
if lineCoverage > -1 and 'line_coverage' not in data:
    error_message += "+ Did not meet line coverage requirement. Received no coverage data\n"

if complexity > -1 and 'complexity' in data and complexity < int(data["complexity"]):
    error_message += "+ Did not meet complexity requirement. Received %s\n" % data["complexity"]
if complexity > -1 and 'complexity' not in data:
    error_message += "+ Did not meet complexity requirement. Received no complexity data\n"

if duplicatedLinesDensity > -1 and 'duplicated_lines_density' in data and duplicatedLinesDensity < float(data["duplicated_lines_density"]):
    error_message += "+ Did not meet duplicated lines density requirement. Received %s\n" % data["duplicated_lines_density"]
if duplicatedLinesDensity > -1 and 'duplicated_lines_density' not in data:
    error_message += "+ Did not meet duplicated lines density requirement. Received no duplicated lines density data\n"

if violations > -1 and 'violations' in data and violations < int(data["violations"]):
    error_message += "+ Did not meet violations requirement. Received %s\n" % data["violations"]
if violations > -1 and 'violations' not in data:
    error_message += "+ Did not meet violations requirement. Received no violations data\n"

if error_message:
    raise Exception("Failed quality verifications:\n%s" % error_message)
print "Code qualification verified"
