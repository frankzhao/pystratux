pystratux
=========

Python integration with stratux. Connects to stratux and plots seen ADS-B traffic on a map.

![Screenshot of sample traffic](https://github.com/frankzhao/pystratux/raw/master/doc/traffic.png)

Traffic seen is written to a database. This can be replayed without a stratux device.

## Live traffic
Connect to a stratux device and plot love traffic on a map.

Usage:

```bash
python bin/stratux 
```

Optional arguments:
  * -H HOST, --host HOST  Stratux hostname or IP (default 10.1.1.120)
  * -g, --arcgis          Use ArcGIS image
  * -z ZOOM, --zoom ZOOM  Use ArcGIS image

## Replay traffic

Optional arguments:
  * -g, --arcgis          Use ArcGIS image
  * -z ZOOM, --zoom ZOOM  Use ArcGIS image

```bash
python bin/replay --arcgis --zoom 1.2
```
