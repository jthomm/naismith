from os import path
FILE_DIR = path.dirname(path.abspath(__file__))

import sys
PKG_DIR = path.dirname(FILE_DIR)
sys.path.append(PKG_DIR)

from datamanager import DataManager

import simplejson as json
import re


DATA_DIR = path.join(path.dirname(PKG_DIR), 'files', 'si')


class ScheduleManager(DataManager):

    def scrape(self, raw):
        mo = re.search(r'callbackWrapper\((.+?)\);$', raw)
        json_data = raw if mo is None else mo.group(1)
        return json.loads(json_data)

    def url_for(self, date_string):
        url_template = 'http://data.sportsillustrated.cnn.com/jsonp/basketball/nba/scoreboards/{year}/{month}/{day}/scoreboard.json'
        return url_template.format(year=date_string[:4],
                                   month=date_string[4:6],
                                   day=date_string[6:])

    def raw_file_path(self, date_string):
        file_name = '{date_string}.txt.gz'.format(date_string=date_string)
        return path.join(DATA_DIR, 'schedule', 'raw', file_name)

    def scraped_file_path(self, date_string):
        file_name = '{date_string}.json.gz'.format(date_string=date_string)
        return path.join(DATA_DIR, 'schedule', 'scraped', file_name)


class PlayByPlayManager(DataManager):
    
    def scrape(self, raw):
        mo = re.search(r'callbackWrapper\((.+?)\);$', raw)
        json_data = raw if mo is None else mo.group(1)
        return json.loads(json_data)

    def url_for(self, date_string_si_id):
        url_template = 'http://data.sportsillustrated.cnn.com/jsonp/basketball/nba/gameflash/{year}/{month}/{day}/{si_id}_playbyplay.json'
        return url_template.format(year=date_string_si_id[:4],
                                   month=date_string_si_id[4:6],
                                   day=date_string_si_id[6:8],
                                   si_id=date_string_si_id[8:])

    def raw_file_path(self, date_string_si_id):
        file_name = '{date_string_si_id}.txt.gz'.format(date_string_si_id=date_string_si_id)
        return path.join(DATA_DIR, 'playbyplay', 'raw', file_name)

    def scraped_file_path(self, date_string_si_id):
        file_name = '{date_string_si_id}.json.gz'.format(date_string_si_id=date_string_si_id)
        return path.join(DATA_DIR, 'playbyplay', 'scraped', file_name)


class BoxScoreManager(DataManager):
    
    def scrape(self, raw):
        mo = re.search(r'callbackWrapper\((.+?)\);$', raw)
        json_data = raw if mo is None else mo.group(1)
        return json.loads(json_data)

    def url_for(self, date_string_si_id):
        url_template = 'http://data.sportsillustrated.cnn.com/jsonp/basketball/nba/gameflash/{year}/{month}/{day}/{si_id}_boxscore.json'
        return url_template.format(year=date_string_si_id[:4],
                                   month=date_string_si_id[4:6],
                                   day=date_string_si_id[6:8],
                                   si_id=date_string_si_id[8:])

    def raw_file_path(self, date_string_si_id):
        file_name = '{date_string_si_id}.txt.gz'.format(date_string_si_id=date_string_si_id)
        return path.join(DATA_DIR, 'boxscore', 'raw', file_name)

    def scraped_file_path(self, date_string_si_id):
        file_name = '{date_string_si_id}.json.gz'.format(date_string_si_id=date_string_si_id)
        return path.join(DATA_DIR, 'boxscore', 'scraped', file_name)
