from datetime import datetime

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

from stratux.model import LoggedObject
from stratux.operations import Operations


class Renderer(LoggedObject):
  def __init__(self, stratux):
    self.stratux = stratux
    self.operations = Operations(stratux)

  def create_map(self):
    self.operations.update_situation()
    self.fig, self.ax = plt.subplots()
    m = Basemap(projection='lcc', resolution='f',
                lat_0=self.stratux.situation.gpsLatitude,
                lon_0=self.stratux.situation.gpsLongitude,
                width=1E5, height=1.5E5,
                # epsg=2113)
                )
    # m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels=2000, verbose=True)
    m.shadedrelief(scale=1)
    m.drawcoastlines(color='gray')
    m.drawcounties(color='gray')
    m.drawstates(color='gray')

    self.plt_map = m
    plt.show(block=False)
    self.fig.canvas.draw()
    plt.pause(0.1)

  def update_map(self, traffic, clear=False):
    lat = traffic.lat
    lng = traffic.lng
    if lat == 0 and lng == 0:
      return

    self.curr_points[traffic.icao_addr] = (lng, lat)

    # update annotations
    if traffic.icao_addr in self.annotations:
      self.annotations[traffic.icao_addr].xy = (
        self.plt_map(traffic.lng, traffic.lat))

    if clear and self.scatter:
      self.scatter.remove()
    self.scatter = self.plt_map.scatter(*zip(*self.curr_points.values()),
                                        latlon=True, marker='+', c='red')

    # annotate
    for t in self.curr_traffic.values():  # type: Traffic
      if t.icao_addr not in self.annotations:
        ann = self.ax.annotate(self.generate_label(t),
                               self.plt_map(t.lng, t.lat), xytext=(5, 5),
                               textcoords='offset points',
                               bbox=dict(boxstyle='round', fc='0.8', alpha=0.5))
        self.annotations[t.icao_addr] = ann
      else:
        self.annotations[t.icao_addr].xy = self.plt_map(t.lng, t.lat)
        self.annotations[t.icao_addr].set_text(self.generate_label(t))

  def reap_traffic(self):
    # remove stale traffic
    curr_traffic = dict(self.curr_traffic)
    curr_annotations = dict(self.annotations)
    curr_points = dict(self.curr_points)
    for k, t in curr_traffic.copy().items():  # type: Traffic
      time_idle = datetime.now() - t.last_seen
      seconds_idle = time_idle.total_seconds()
      if seconds_idle > 60:
        self.logger.info(
            "Reaping stale traffic: icao: {}, tail: {} - idle for {}s".format(
                t.icao_addr, t.tail,
                seconds_idle))
        curr_traffic.pop(k, None)
        curr_points.pop(k, None)
        ann = curr_annotations.pop(k, None)
        if ann:
          ann.xy = (0, 0)
          ann.remove()
    self.curr_traffic = curr_traffic
    self.annotations = curr_annotations
    self.curr_points = curr_points

  @staticmethod
  def generate_label(traffic):
    label = '{} {}\n{} {}@{}'.format(
        traffic.squawk if traffic.squawk else traffic.icao_addr,
        str(round(traffic.age, 1)) + 's',
        traffic.tail if traffic.tail else traffic.reg,
        str(traffic.track) if traffic.track else '?',
        str(traffic.speed if traffic.speed else '?') + "kts"
    )

    return label

  def process_buffer(self, buffer):
    for traffic in buffer.values():
      traffic.last_seen = datetime.now()
      self.curr_traffic[traffic.icao_addr] = traffic

      self.stratux.session.add(traffic)
      self.stratux.session.commit()

      self.update_map(traffic, clear=False)
      self.reap_traffic()
      self.fig.canvas.draw()
