from os import path
MODULE_DIR = path.dirname(path.abspath(__file__))

import sys
PKG_DIR = path.dirname(MODULE_DIR)
sys.path.append(PKG_DIR)

from resourceabc import ResourceABC

import simplejson as json
import re
from scraping import si

FILE_DIR = path.join(path.dirname(MODULE_DIR), 'files', 'si')


class SchedulePage(ResourceABC):

    def scrape(self, raw):
        mo = re.search(r'callbackWrapper\((.+?)\);$', raw)
        json_data = raw if mo is None else mo.group(1)
        return json.loads(json_data)

    @property
    def url(self):
        url_template = 'http://data.sportsillustrated.cnn.com/jsonp/basketball/nba/scoreboards/{year}/{month}/{day}/scoreboard.json'
        return url_template.format(**{'year': self.resource_id[:4],
                                      'month': self.resource_id[4:6],
                                      'day': self.resource_id[6:],})

    @property
    def raw_file_path(self):
        file_name = '{date_string}.txt.gz'.format(date_string=self.resource_id)
        return path.join(FILE_DIR, 'schedule', 'raw', file_name)

    @property
    def scraped_file_path(self):
        file_name = '{date_string}.json.gz'.format(date_string=self.resource_id)
        return path.join(FILE_DIR, 'schedule', 'scraped', file_name)


class PlayByPlay(ResourceABC):
    
    def scrape(self, raw):
        return si.PlayByPlay(raw).as_dict
        #mo = re.search(r'callbackWrapper\((.+?)\);$', raw)
        #json_data = raw if mo is None else mo.group(1)
        #return json.loads(json_data)

    @property
    def url(self):
        url_template = 'http://data.sportsillustrated.cnn.com/jsonp/basketball/nba/gameflash/{year}/{month}/{day}/{si_id}_playbyplay.json'
        return url_template.format(**{'year': self.resource_id[:4],
                                      'month': self.resource_id[4:6],
                                      'day': self.resource_id[6:8],
                                      'si_id': self.resource_id[8:],})

    @property
    def raw_file_path(self):
        file_name = '{rid}.txt.gz'.format(rid=self.resource_id)
        return path.join(FILE_DIR, 'playbyplay', 'raw', file_name)

    @property
    def scraped_file_path(self):
        file_name = '{rid}.json.gz'.format(rid=self.resource_id)
        return path.join(FILE_DIR, 'playbyplay', 'scraped', file_name)


class BoxScore(ResourceABC):
    
    def scrape(self, raw):
        mo = re.search(r'callbackWrapper\((.+?)\);$', raw)
        json_data = raw if mo is None else mo.group(1)
        return json.loads(json_data)

    @property
    def url(self):
        url_template = 'http://data.sportsillustrated.cnn.com/jsonp/basketball/nba/gameflash/{year}/{month}/{day}/{si_id}_boxscore.json'
        return url_template.format(**{'year': self.resource_id[:4],
                                      'month': self.resource_id[4:6],
                                      'day': self.resource_id[6:8],
                                      'si_id': self.resource_id[8:],})

    @property
    def raw_file_path(self):
        file_name = '{rid}.txt.gz'.format(rid=self.resource_id)
        return path.join(FILE_DIR, 'boxscore', 'raw', file_name)

    @property
    def scraped_file_path(self):
        file_name = '{rid}.json.gz'.format(rid=self.resource_id)
        return path.join(FILE_DIR, 'boxscore', 'scraped', file_name)
