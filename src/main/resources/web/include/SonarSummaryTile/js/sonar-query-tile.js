/*
 * Copyright 2019 XEBIALABS
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

'use strict';

(function () {

    var SonarQueryTileViewController = function ($scope, SonarQueryService, XlrTileHelper) {
        var vm = this;

        vm.tileConfigurationIsPopulated = tileConfigurationIsPopulated;

        var tile;

        var predefinedColors = [];
        predefinedColors['Open'] = '#7E827A';
        predefinedColors['Reopened'] = '#4AA0C8';
        predefinedColors['To Do'] = '#7E827A';
        predefinedColors['In Progress'] = '#7FB2F0';
        predefinedColors['Resolved'] = '#45BF55';
        predefinedColors['Done'] = '#45BF55';
        predefinedColors['Closed'] = '#468966';
        predefinedColors['Testing'] = '#FFA500';


        if ($scope.xlrDashboard) {
            // summary page
            vm.release = $scope.xlrDashboard.release;
            vm.tile = $scope.xlrTile.tile;
            if (vm.tile.properties == null) {
                vm.config = vm.tile.configurationProperties;
            } else {
                // new style since 7.0
                vm.config = vm.tile.properties;
            }
        }

        function tileConfigurationIsPopulated() {
            return !_.isEmpty(vm.config.sonarServer);
        }

        function load(config) {
            if (tileConfigurationIsPopulated()) {
                vm.loading = true;
                SonarQueryService.executeQuery(vm.tile.id, config).then(
                    function (response) {
                        var sonardata = response.data.data;
                        var result = new Object();
                        for (var metric = 0 ; metric < Object.getOwnPropertyNames(sonardata).length ; metric++)
                        {
                            var keyName = Object.getOwnPropertyNames(sonardata)[metric];
                            var finalKeyName = vm.config.metrics.value[keyName];
                            switch(keyName){
                                case 'key' : result[keyName] = { key : 'Project Key', value : sonardata[keyName], url : sonardata['sonarUrl'] + '/overview?id=' + sonardata['key']}; break;
                                case 'version' : result[keyName] = { key : 'Arfifact Version', value : sonardata[keyName]}; break;
                                case 'name' : break;
                                case 'id' : break;
                                case 'sonarUrl' : break;
                                default : result[keyName] = { key : finalKeyName, value : sonardata[keyName], url : sonardata['sonarUrl'] + '/component_measures/metric/' + keyName + '/list?id=' + sonardata['key']};

                            }
                            
                        }
                        vm.result = result;
                        $scope.xlrTile.title = tile.title + " : " + sonardata['name'];
                    }
                ).finally(function () {
                    vm.loading = false;

                });
            }
        }


        function refresh() {
            load({params: {refresh: true}});
        }

        load();

        vm.refresh = refresh;
    };

    SonarQueryTileViewController.$inject = ['$scope', 'xlrelease.sonar.SonarQueryService', 'XlrTileHelper'];

    var SonarQueryService = function (Backend) {

        function executeQuery(tileId, config) {
            return Backend.get("tiles/" + tileId + "/data", config);
        }

        return {
            executeQuery: executeQuery
        };
    };

    SonarQueryService.$inject = ['Backend'];

    angular.module('xlrelease.sonar.tile', []);
    angular.module('xlrelease.sonar.tile').service('xlrelease.sonar.SonarQueryService', SonarQueryService);
    angular.module('xlrelease.sonar.tile').controller('sonar.SonarQueryTileViewController', SonarQueryTileViewController);

})();

