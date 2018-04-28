import asyncio

import logging
import json
import websockets
import matplotlib.pyplot as plt
from datetime import datetime
from mpl_toolkits.basemap import Basemap
from stratux.model.traffic import Traffic

logging.getLogger('sqlalchemy').setLevel(logging.WARN)


class Stratux:
    fig = None
    ax = None
    plt_map = None
    scatter = None
    curr_traffic = {}
    curr_points = {}
    annotations = {}
    center_lng, center_lat = 174.7762, -41.2865

    def __init__(self, session, uri='ws://10.1.1.120/traffic'):
        self.logger = logging.getLogger(__name__)
        self.session = session  # type: sqlalchemy.orm.session.Session
        self.stratux_uri = uri

    async def connect(self):
        self.logger.info('Connecting to stratux')
        async with websockets.connect(self.stratux_uri) as websocket:
            self.logger.info('Connected.')
            while True:
                buffer = []
                buffer_age_ms = 0
                buffer_start = datetime.now()
                while len(buffer) < 20 and buffer_age_ms < 1000:
                    packet = await websocket.recv()
                    logging.debug('Received packet: {}'.format(packet))
                    buffer.append(packet)
                    t_delta = (datetime.now() - buffer_start)
                    buffer_age_ms = int((t_delta.seconds * 1000) + (t_delta.microseconds / 1000))

                logging.debug('Collecting buffer n={} took {}ms'.format(len(buffer), buffer_age_ms))
                self.process_buffer(buffer)
                buffer.clear()

    def process_buffer(self, messages):
        for packet in messages:
            entry = json.JSONDecoder().decode(packet)  # type: dict

            entry_lowered = dict((k.lower(), v) for k, v in entry.items())
            traffic = Traffic(**entry_lowered)
            traffic.last_seen = datetime.now()
            self.curr_traffic[traffic.icao_addr] = traffic

            # self.session.add(traffic)
            # self.session.commit()

            self.update_map(traffic, clear=False)
            self.reap_traffic()
            self.fig.canvas.draw()

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

    def launch(self):
        self.create_map()
        asyncio.get_event_loop().run_until_complete(self.connect())

    def create_map(self):
        self.fig, self.ax = plt.subplots()
        m = Basemap(projection='lcc', resolution='f',
                    lat_0=self.center_lat, lon_0=self.center_lng,
                    width=1E5, height=1.5E5,
                    epsg=2113)
        m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels=2000, verbose=True)
        # m.shadedrelief(scale=1)
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
            self.annotations[traffic.icao_addr].xy = (self.plt_map(traffic.lng, traffic.lat))

        if clear and self.scatter:
            self.scatter.remove()
        self.scatter = self.plt_map.scatter(*zip(*self.curr_points.values()), latlon=True, marker='+', c='red')

        # annotate
        for t in self.curr_traffic.values():  # type: Traffic
            if t.icao_addr not in self.annotations:
                ann = self.ax.annotate(self.generate_label(t), self.plt_map(t.lng, t.lat), xytext=(5, 5),
                                       textcoords='offset points', bbox=dict(boxstyle='round', fc='0.8', alpha=0.5))
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
                    "Reaping stale traffic: icao: {}, tail: {} - idle for {}s".format(t.icao_addr, t.tail,
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
