from os import path
FILE_DIR = path.dirname(path.abspath(__file__))

import sys
PKG_DIR = path.dirname(FILE_DIR)
sys.path.append(PKG_DIR)

from datamanager import DataManager

from scraping import nba

import bs4


DATA_DIR = path.join(path.dirname(PKG_DIR), 'files', 'nba')


class ScheduleManager(DataManager):

    def scrape(self, raw):
        tag = bs4.BeautifulSoup(raw)
        return nba.SchedulePage(tag)

    def url_for(self, date_string):
        url_template = 'http://www.nba.com/gameline/{date_string}'
        return url_template.format(date_string=date_string)

    def raw_file_path(self, date_string):
        file_name = '{date_string}.html.gz'.format(date_string=date_string)
        return path.join(DATA_DIR, 'schedule', 'raw', file_name)

    def scraped_file_path(self, date_string):
        file_name = '{date_string}.json.gz'.format(date_string=date_string)
        return path.join(DATA_DIR, 'schedule', 'scraped', file_name)


class PlayByPlayManager(DataManager):
    
    def scrape(self, raw):
        tag = bs4.BeautifulSoup(raw)
        return nba.PlayByPlay(tag)

    def url_for(self, nba_id):
        url_template = 'http://www.nba.com/games/{date_string}/{away_abbr}{home_abbr}/gameinfo.html'
        return url_template.format(date_string=nba_id[:8],
                                   away_abbr=nba_id[8:11],
                                   home_abbr=nba_id[11:])

    def raw_file_path(self, nba_id):
        file_name = '{nba_id}.html.gz'.format(nba_id=nba_id)
        return path.join(DATA_DIR, 'playbyplay', 'raw', file_name)

    def scraped_file_path(self, nba_id):
        file_name = '{nba_id}.json.gz'.format(nba_id=nba_id)
        return path.join(DATA_DIR, 'playbyplay', 'scraped', file_name)


class BoxScoreManager(DataManager):
    
    def scrape(self, raw):
        tag = bs4.BeautifulSoup(raw)
        return nba.BoxScore(tag)

    def url_for(self, nba_id):
        url_template = 'http://www.nba.com/games/{date_string}/{away_abbr}{home_abbr}/gameinfo.html'
        return url_template.format(date_string=nba_id[:8],
                                   away_abbr=nba_id[8:11],
                                   home_abbr=nba_id[11:])

    def raw_file_path(self, nba_id):
        file_name = '{nba_id}.html.gz'.format(nba_id=nba_id)
        return path.join(DATA_DIR, 'playbyplay', 'raw', file_name)

    def scraped_file_path(self, nba_id):
        file_name = '{nba_id}.json.gz'.format(nba_id=nba_id)
        return path.join(DATA_DIR, 'boxscore', 'scraped', file_name)


class GameMetaManager(DataManager):

    def scrape(self, raw):
        tag = bs4.BeautifulSoup(raw)
        return nba.GameMeta(tag).as_dict

    def url_for(self, nba_id):
        url_template = 'http://www.nba.com/games/{date_string}/{away_abbr}{home_abbr}/gameinfo.html'
        return url_template.format(date_string=nba_id[:8],
                                   away_abbr=nba_id[8:11],
                                   home_abbr=nba_id[11:])

    def raw_file_path(self, nba_id):
        file_name = '{nba_id}.html.gz'.format(nba_id=nba_id)
        return path.join(DATA_DIR, 'playbyplay', 'raw', file_name)

    def scraped_file_path(self, nba_id):
        file_name = '{nba_id}.json.gz'.format(nba_id=nba_id)
        return path.join(DATA_DIR, 'meta', 'scraped', file_name)
