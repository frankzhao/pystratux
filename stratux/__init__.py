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

    def __init__(self, session, uri='ws://10.1.1.120/traffic'):
        self.logger = logging.getLogger(__name__)
        self.session = session  # type: sqlalchemy.orm.session.Session
        self.stratux_uri = uri

    async def connect(self):
        self.logger.info('Connecting to stratux')
        async with websockets.connect(self.stratux_uri) as websocket:
            self.logger.info('Connected.')
            while True:
                packet = await websocket.recv()
                logging.debug('Received packet: {}'.format(packet))

                entry = json.JSONDecoder().decode(packet)  # type: dict
                entry_lowered = dict((k.lower(), v) for k, v in entry.items())
                self.logger.info("timestamp: {}".format(entry_lowered['timestamp']))
                try:
                    entry_lowered['timestamp'] = datetime.strptime(entry_lowered['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
                except ValueError:
                    entry_lowered['timestamp'] = datetime.strptime(entry_lowered['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
                traffic = Traffic(**entry_lowered)
                self.curr_traffic[traffic.icao_addr] = traffic

                self.session.add(traffic)
                self.session.commit()

                self.update_map(traffic, clear=False)

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
        self.fig = plt.figure(figsize=(8, 8))
        m = Basemap(projection='lcc', resolution='f', lat_0=-41.2865, lon_0=174.7762, width=8E4, height=1E5,
                    epsg=2113)
        m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels=2000, verbose=True)
        # m.shadedrelief(scale=1)
        m.drawcoastlines(color='gray')
        m.drawcounties(color='gray')
        m.drawstates(color='gray')

        self.plt_map = m
        plt.show(block=False)
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
            plt.draw()

        self.reap_traffic()
        if clear and self.scatter:
            self.scatter.remove()
            plt.draw()
        self.scatter = self.plt_map.scatter(*zip(*self.curr_points.values()), latlon=True, marker='+', c='red')

        # annotate
        for t in self.curr_traffic.values():    # type: Traffic
            if t.icao_addr not in self.annotations:
                ann = plt.annotate(self.generate_label(t), self.plt_map(t.lng, t.lat), xytext=(5, 5),
                                   textcoords='offset points', bbox=dict(boxstyle='round', fc='0.8', alpha=0.5))
                self.annotations[t.icao_addr] = ann
            else:
                self.annotations[t.icao_addr].xy = self.plt_map(t.lng, t.lat)
            plt.draw()

        plt.pause(0.1)

    def reap_traffic(self):
        # remove stale traffic
        for k, t in self.curr_traffic.copy().items():    # type: Traffic
            time_idle = datetime.utcfromtimestamp(datetime.now().timestamp()) - t.timestamp
            seconds_idle = time_idle.total_seconds()
            if seconds_idle > 60:
                self.logger.info("Reaping stale traffic: icao: {}, tail: {}".format(t.icao_addr, t.tail))
                del self.curr_traffic[k]
                if k in self.annotations:
                    ann = self.annotations.get(k)
                    ann.xy = (0, 0)
                    ann.remove()
                    del self.annotations[k]
                if k in self.curr_points:
                    del self.curr_points[k]
                plt.draw()
        plt.pause(0.1)

