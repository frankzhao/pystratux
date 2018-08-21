import requests

from stratux.model import LoggedObject
from stratux.model.situation import Situation


class Operations(LoggedObject):
  def __init__(self, stratux):
    self.stratux = stratux

  def update_situation(self, timeout=10):
    response = requests.get("http://" + self.stratux.stratux_host + "/getSituation", timeout=timeout)
    if response.status_code != 200:
      self.logger.error("Unable to get current situation: {} - {}",
                        response.status_code, response.text)
      return

    response_json = response.json()
    response_json_lowered = dict((k.lower(), v) for k, v in response_json.items())
    situation = Situation(**response_json_lowered)
    self.stratux.situation = situation
