from espn import PlayByPlay, GameFlow, ShotChart
from bs4 import BeautifulSoup as bs
import requests



class ESPNCom(dict):
    """Top-level API for accessing ESPN.com game data.  Includes data from 
    ESPN.com game page (metadata, play-by-play), as well as shot chart and 
    game flow data.
    """

    PBP_BASE_URL = 'http://scores.espn.go.com/nba/playbyplay?gameId=%s&period=0'
    XML_BASE_URL = 'http://sports.espn.go.com/nba/gamepackage/data/%s?gameId=%s'

    def __init__(self, espn_game_id):
        """Initialize with `espn_game_id`:

        >>> espn_game_id = '400278120'
        >>> game = ESPNCom(espn_game_id)

        `ESPNCom` object will then construct the appropriate URLs and fetch the 
        html/xml data required for each subsidiary object (play-by-play, 
        shot chart, and game flow).
        """
        dict.__init__(self)
        # Get play-by-play data
        pbp_tag = _get_tag(self.PBP_BASE_URL % espn_game_id)
        self.update(PlayByPlay(pbp_tag))
        # Get shot chart data
        shot_chart_tag = _get_tag(self.XML_BASE_URL % ('shot', espn_game_id))
        self['shot_chart'] = ShotChart(shot_chart_tag)
        # Get game flow data
        game_flow_tag = _get_tag(self.XML_BASE_URL % ('gameflow', espn_game_id))
        self['game_flow'] = GameFlow(game_flow_tag)



"""Utils"""

def _get_tag(url):
    return bs(requests.get(url).text)
