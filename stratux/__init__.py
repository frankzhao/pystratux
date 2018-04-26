import asyncio

import logging
import json
import websockets
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from stratux.model.traffic import Traffic

logging.getLogger('sqlalchemy').setLevel(logging.WARN)


class Stratux:
    fig = None
    ax = None
    plt_map = None
    scatter = None
    curr_points = []
    annotations = []

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
                traffic = Traffic(**entry_lowered)
                self.session.add(traffic)
                self.session.commit()

                lat = entry_lowered.get('lat')
                lng = entry_lowered.get('lng')
                self.update_map(lng, lat, self.generate_label(traffic), clear=True)

    @staticmethod
    def generate_label(traffic):
        label = '{} {}\n{}'.format(
            traffic.squawk if traffic.squawk else traffic.icao_addr,
            str(round(traffic.age, 1)) + 's',
            traffic.tail if traffic.tail else '?')
        return label

    def launch(self):
        self.create_map()
        asyncio.get_event_loop().run_until_complete(self.connect())

    def create_map(self):
        self.fig = plt.figure(figsize=(8, 8))
        m = Basemap(projection='lcc', resolution='f', lat_0=-41.2865, lon_0=174.7762, width=1E5, height=1.2E5,
                    epsg=2113)
        # m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels=2000, verbose=True)
        m.shadedrelief(scale=1)
        m.drawcoastlines(color='gray')
        m.drawcounties(color='gray')
        m.drawstates(color='gray')

        self.plt_map = m
        plt.show(block=False)
        plt.pause(0.1)

    def update_map(self, lng, lat, label, clear=False):
        if lat == 0 and lng == 0:
            return

        if (lng, lat) in self.curr_points:
            self.curr_points.remove((lng, lat))
        if clear and self.scatter:
            # Clear plot if existing
            self.scatter.remove()
        self.curr_points.append((lng, lat))
        self.scatter = self.plt_map.scatter(*zip(*self.curr_points), latlon=True, alpha=0.5, marker='+')

        # clear annotations
        for ann in self.annotations:
            ann.remove()
        self.annotations = []

        # annotate
        for pt in self.curr_points:
            self.annotations.append(
                plt.gca().annotate(str(label), self.plt_map(pt[0], pt[1]), xytext=(5, 5),
                                   textcoords='offset points'))

        plt.pause(0.1)
        self.logger.info('Showing {} points'.format(len(self.curr_points)))
