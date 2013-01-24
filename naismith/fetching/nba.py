from os import path
MODULE_DIR = path.dirname(path.abspath(__file__))

import sys
PKG_DIR = path.dirname(MODULE_DIR)
sys.path.append(PKG_DIR)

from resourceabc import ResourceABC

from scraping import nba

import bs4


FILE_DIR = path.join(path.dirname(MODULE_DIR), 'files', 'nba')


class SchedulePage(ResourceABC):
    
    def scrape(self, raw):
        tag = bs4.BeautifulSoup(raw)
        return nba.SchedulePage(tag)

    @property
    def url(self):
        tmpl = 'http://www.nba.com/gameline/{date_string}'
        return tmpl.format(date_string=self.resource_id)

    @property
    def raw_file_path(self):
        file_name = '{date_string}.html.gz'.format(date_string=self.resource_id)
        return path.join(FILE_DIR, 'schedule', 'raw', file_name)

    @property
    def scraped_file_path(self):
        file_name = '{date_string}.json.gz'.format(date_string=self.resource_id)
        return path.join(FILE_DIR, 'schedule', 'scraped', file_name)


class PlayByPlay(ResourceABC):

    def scrape(self, raw):
        tag = bs4.BeautifulSoup(raw)
        return nba.PlayByPlay(tag)

    @property
    def url(self):
        tmpl = 'http://www.nba.com/games/{date_string}/{away_abbr}{home_abbr}/gameinfo.html'
        return tmpl.format(**{'date_string': self.resource_id[:8],
                              'away_abbr': self.resource_id[8:11],
                              'home_abbr': self.resource_id[11:],})

    @property
    def raw_file_path(self):
        file_name = '{nba_id}.html.gz'.format(nba_id=self.resource_id)
        return path.join(FILE_DIR, 'playbyplay', 'raw', file_name)

    @property
    def scraped_file_path(self):
        file_name = '{nba_id}.json.gz'.format(nba_id=self.resource_id)
        return path.join(FILE_DIR, 'playbyplay', 'scraped', file_name)


class BoxScore(ResourceABC):

    def scrape(self, raw):
        tag = bs4.BeautifulSoup(raw)
        return nba.BoxScore(tag)

    @property
    def url(self):
        tmpl = 'http://www.nba.com/games/{date_string}/{away_abbr}{home_abbr}/gameinfo.html'
        return tmpl.format(**{'date_string': self.resource_id[:8],
                              'away_abbr': self.resource_id[8:11],
                              'home_abbr': self.resource_id[11:],})

    @property
    def raw_file_path(self):
        file_name = '{nba_id}.html.gz'.format(nba_id=self.resource_id)
        return path.join(FILE_DIR, 'playbyplay', 'raw', file_name)

    @property
    def scraped_file_path(self):
        file_name = '{nba_id}.json.gz'.format(nba_id=self.resource_id)
        return path.join(FILE_DIR, 'boxscore', 'scraped', file_name)


class GameMeta(ResourceABC):

    def scrape(self, raw):
        tag = bs4.BeautifulSoup(raw)
        return nba.GameMeta(tag).as_dict

    @property
    def url(self):
        tmpl = 'http://www.nba.com/games/{date_string}/{away_abbr}{home_abbr}/gameinfo.html'
        return tmpl.format(**{'date_string': self.resource_id[:8],
                              'away_abbr': self.resource_id[8:11],
                              'home_abbr': self.resource_id[11:],})

    @property
    def raw_file_path(self):
        file_name = '{nba_id}.html.gz'.format(nba_id=self.resource_id)
        return path.join(FILE_DIR, 'playbyplay', 'raw', file_name)

    @property
    def scraped_file_path(self):
        file_name = '{nba_id}.json.gz'.format(nba_id=self.resource_id)
        return path.join(FILE_DIR, 'meta', 'scraped', file_name)
