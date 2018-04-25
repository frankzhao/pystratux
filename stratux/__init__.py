import asyncio

import websockets
import json
import logging
from stratux.model.traffic import Traffic

logging.basicConfig(level=logging.INFO)


class Stratux:

    def __init__(self, session, uri='ws://10.1.1.73/traffic'):
        self.logger = logging.getLogger(__name__)
        self.session = session  # type: sqlalchemy.orm.session.Session
        self.stratux_uri = uri

    async def connect(self):
        self.logger.info("Connecting to stratux")
        async with websockets.connect(self.stratux_uri) as websocket:
            self.logger.info("Connected.")
            while True:
                packet = await websocket.recv()
                logging.info('Received packet: {}'.format(packet))

                entry = json.JSONDecoder().decode(packet)  # type: dict
                entry_lowered = dict((k.lower(), v) for k, v in entry.items())
                traffic = Traffic(**entry_lowered)
                self.session.add(traffic)
                self.session.commit()

    def launch(self):
        asyncio.get_event_loop().run_until_complete(self.connect())
