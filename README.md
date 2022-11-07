## Description
This is the custom-made plugin for QGIS with the functionality of creating a heatmap from a layer with points.

## How to add plugin to QGIS
To add the plugin to QGIS you need to make this simple n steps:
1. Close QGIS if it is open.
2. Clone the code from this repo to the local folder (preferably named _delta_plugin_).
3. Find the QGIS application plugin folder. In Ubuntu it is usually located in _/home/USER/.local/share/QGIS/QGIS3/profiles/default/python/plugins_, in Windows in _ C:\Users\USER\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins_
4. Move the folder with the code that you created in the first step to the QGIS plugin folder from the second step.
5. Open QGIS.
6. Open QGIS _Plugins menu_ and switch to mode _All_.
7. Type _Delta plugin_ in the search bar.
8. Choose the plugin and put a check in a checkbox near it.

The plugin is ready to be used, congratulations!

## How to use plugin
To use the plugin you have to click on its icon, choose the layer with the points, change values of horizontal and vertical spacing and press _Применить_. The execution may take a while and the progress bar is not always working, so you might need to wait for a while.
