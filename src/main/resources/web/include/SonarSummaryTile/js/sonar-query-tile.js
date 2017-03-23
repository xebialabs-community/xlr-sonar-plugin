/*
 * THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
 * FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
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


        if ($scope.xlrTile) {
            // summary mode
            tile = $scope.xlrTile.tile;
        }

        function tileConfigurationIsPopulated() {
            var config = tile.configurationProperties;
            return !_.isEmpty(config.sonarServer);
        }

        function load(config) {
            if (tileConfigurationIsPopulated()) {
                vm.loading = true;
                SonarQueryService.executeQuery(tile.id, config).then(
                    function (response) {
                        console.log()
                        var sonardata = response.data.data;
                        var result = new Object();
                        for (var metric = 0 ; metric < Object.getOwnPropertyNames(sonardata).length ; metric++)
                        {
                            var keyName = Object.getOwnPropertyNames(sonardata)[metric];
                            var finalKeyName = tile.configurationProperties.metrics.value[keyName];
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
                        console.log(result);
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

