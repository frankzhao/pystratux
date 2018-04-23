import asyncio

import websockets


class Stratux:
  stratux_uri = 'ws://10.1.1.120/traffic'

  async def connect(self, uri=stratux_uri):
    async with websockets.connect(uri) as websocket:
      while True:
        packet = await websocket.recv()
        print(packet)

  def launch(self):
    asyncio.get_event_loop().run_until_complete(self.connect())

# {
#   "Icao_addr": 1065986,
#   "Reg": "",
#   "Tail": "",
#   "Emitter_category": 0,
#   "OnGround": true,
#   "Addr_type": 4,
#   "TargetType": 0,
#   "SignalLevel": -43.09803919971486,
#   "Squawk": 0,
#   "Position_valid": true,
#   "Lat": -89.64273,
#   "Lng": 4.265485,
#   "Alt": 35850,
#   "GnssDiffFromBaroAlt": 0,
#   "AltIsGNSS": false,
#   "NIC": 8,
#   "NACp": 0,
#   "Track": 0,
#   "Speed": 357,
#   "Speed_valid": true,
#   "Vvel": 0,
#   "Timestamp": "2016-02-27T22:52:53.910258947Z",
#   "PriorityStatus": 0,
#   "Age": 0,
#   "AgeLastAlt": 0,
#   "Last_seen": "0001-01-01T23:29:11.63Z",
#   "Last_alt": "0001-01-01T23:29:11.63Z",
#   "Last_GnssDiff": "0001-01-01T00:00:00Z",
#   "Last_GnssDiffAlt": 0,
#   "Last_speed": "0001-01-01T23:29:11.63Z",
#   "Last_source": 2,
#   "ExtrapolatedPosition": false,
#   "BearingDist_valid": false,
#   "Bearing": 0,
#   "Distance": 0
# }
