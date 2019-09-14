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

sonar_server_api_url = '/api/project_analyses/search?project=%s&p=1&ps=1' % resource
http_request = HttpRequest(sonarServer, username, password)
sonar_response = http_request.get(sonar_server_api_url)
if not sonar_response.isSuccessful():
    raise Exception("Failed to get Sonarqube data. Server return [%s], with content [%s]" % (sonar_response.status, sonar_response.response))
json_data = json.loads(sonar_response.getResponse())
event_key = None
analysis_key = json_data["analyses"][0]["key"]
for event in json_data["analyses"][0]["events"]:
    if event["category"] == "VERSION":
        event_key = event["key"]

if event_key is not None:
    sonar_server_api_url = '/api/project_analyses/update_event?event=%s&name=%s' % (event_key, version)
    http_request = HttpRequest(sonarServer, username, password)
    sonar_response = http_request.post(sonar_server_api_url, body="")
    if not sonar_response.isSuccessful():
        raise Exception("Failed to get Sonarqube data. Server return [%s], with content [%s]" % (sonar_response.status, sonar_response.response))
else:
    sonar_server_api_url = '/api/project_analyses/create_event?analysis=%s&category=VERSION&name=%s' % (analysis_key, version)
    http_request = HttpRequest(sonarServer, username, password)
    sonar_response = http_request.post(sonar_server_api_url, body="")
    if not sonar_response.isSuccessful():
        raise Exception("Failed to get Sonarqube data. Server return [%s], with content [%s]" % (sonar_response.status, sonar_response.response))