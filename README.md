# XL Release Sonar Plugin
Sonar Tile for XL Release


# Installation #

You can copy the pre build jar file from under the releases section under git repo

OR 

Build the project:
```
gradle build
```

Copy the extension to the plugins folder of your XLD installation:
```
cp ./build/libs/xlr-ui-permissions.jar $XLRelease_HOME/plugins
```


#Usage#

1. Go to the Settings > Configuration and define a Sonarqube Server Reference
2. Then go to a release template and go to the release summary view
3. Add the Sonar Tile from the drop down list
4. Specify what all metrics you want to show in summary ( Keys are the key used as Sonar metrics URI params, Value part is a Nice to Show Header for that metric)
![Configuration] (/images/snapshot1.png)

5. On saving, you'll get the Preview. You can even click on the Data items represented as hyperlinks that take you back to the Sonar Dashboard in a separate browser. 
![Preview] (/images/snapshot2.png)
