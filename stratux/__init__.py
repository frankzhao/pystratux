import asyncio
import json
import logging
from datetime import datetime

import matplotlib.pyplot as plt
import websockets

from stratux.model.situation import Situation
from stratux.model.traffic import Traffic
from stratux.operations import Operations
from stratux.render import Renderer

logging.getLogger('sqlalchemy').setLevel(logging.WARN)


class Stratux:
  ax = None
  plt_map = None
  scatter = None
  situation = None
  renderer = None
  # center_lng, center_lat = 174.7762, -41.2865  # WLG
  center_lng, center_lat = 149.1934, -35.3052  # CBR
  # default uri = 'ws://10.1.1.120/traffic'
  stratux_host = '10.1.1.120'  # 192.168.10.1

  def __init__(self, session, host='10.1.1.120'):
    self.logger = logging.getLogger(__name__)
    self.session = session  # type: sqlalchemy.orm.session.Session
    self.stratux_host = host
    self.renderer = Renderer(self)

  async def connect(self):
    self.logger.info('Connecting to stratux')
    traffic_uri = "ws://" + self.stratux_host + "/traffic"
    async with websockets.connect(traffic_uri) as websocket:
      self.logger.info('Connected.')
      while True:
        buffer = {}
        buffer_age_ms = 0
        buffer_start = datetime.now()
        while len(buffer.keys()) < 10 and buffer_age_ms < 1000:
          packet = await websocket.recv()
          logging.debug('Received packet: {}'.format(packet))

          entry = json.JSONDecoder().decode(packet)  # type: dict
          entry_lowered = dict((k.lower(), v) for k, v in entry.items())
          traffic = Traffic(**entry_lowered)

          # only store latest seen value of unique traffic
          # in buffer for performance
          buffer[traffic.icao_addr] = traffic
          t_delta = (datetime.now() - buffer_start)
          buffer_age_ms = int(
              (t_delta.seconds * 1000) + (t_delta.microseconds / 1000))

        logging.debug(
            'Collecting buffer n={} took {}ms'.format(len(buffer),
                                                      buffer_age_ms))
        self.renderer.process_buffer(buffer)
        buffer.clear()

  def launch(self, gis=False, zoom=1):
    self.renderer.create_map(gis=gis, zoom=zoom)
    while True:
      try:
        asyncio.get_event_loop().run_until_complete(self.connect())
      except OSError:
        self.logger.error(
            "Could not connect to stratux, retrying in {}s".format(10))
      except KeyboardInterrupt:
        return

  def launch_replay(self, gis=False, zoom=1):
    self.situation = Situation()
    self.situation.gpsLongitude = self.center_lng
    self.situation.gpsLatitude = self.center_lat
    self.renderer.create_map(update_situation=False, gis=gis, zoom=zoom)
    try:
      self.replay()
    except KeyboardInterrupt:
      return

  # Replay from database
  def replay(self, buffer_size=25):
    traffic = self.session.query(Traffic).filter(
        Traffic.position_valid,
        Traffic.speed_valid,
        Traffic.bearingdist_valid,
        Traffic.tail is not None,
        Traffic.tail != ''
    ).order_by(Traffic.last_seen.asc()).all()
    self.logger.info("Found {} traffic entries.".format(len(traffic)))

    i = 0
    buffer = {}
    for t in traffic:
      self.logger.debug("Plotting: {}".format(t.tail))
      buffer[t.icao_addr] = t
      i = i + 1
      if i == buffer_size:
        self.renderer.process_buffer(buffer, save=False)
        buffer.clear()
        i = 0

    # Keep map open
    try:
      plt.show(block=True)
    except KeyboardInterrupt:
      return
