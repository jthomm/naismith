from os import path
MODULE_DIR = path.dirname(path.abspath(__file__))

import sys
PKG_DIR = path.dirname(MODULE_DIR)
sys.path.append(PKG_DIR)

from resourceabc import ResourceABC

from scraping import espn

import bs4


FILE_DIR = path.join(path.dirname(MODULE_DIR), 'files', 'espn')


class SchedulePage(ResourceABC):

    def scrape(self, raw):
        tag = bs4.BeautifulSoup(raw)
        return espn.SchedulePage(tag)

    @property
    def url(self):
        url_tmpl = 'http://espn.go.com/nba/scoreboard?date={date_string}'
        return url_tmpl.format(date_string=self.resource_id)

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
        return espn.PlayByPlay(tag)

    @property
    def url(self):
        url_tmpl = 'http://espn.go.com/nba/playbyplay?gameId={gid}&period=0'
        return url_tmpl.format(gid=self.resource_id)

    @property
    def raw_file_path(self):
        file_name = '{espn_id}.html.gz'.format(espn_id=self.resource_id)
        return path.join(FILE_DIR, 'playbyplay', 'raw', file_name)

    @property
    def scraped_file_path(self):
        file_name = '{espn_id}.json.gz'.format(espn_id=self.resource_id)
        return path.join(FILE_DIR, 'playbyplay', 'scraped', file_name)


class BoxScore(ResourceABC):

    def scrape(self, raw):
        tag = bs4.BeautifulSoup(raw)
        return espn.BoxScore(tag)

    @property
    def url(self):
        url_tmpl = 'http://espn.go.com/nba/boxscore?gameId={espn_id}'
        return url_tmpl.format(espn_id=self.resource_id)

    @property
    def raw_file_path(self):
        file_name = '{espn_id}.html.gz'.format(espn_id=self.resource_id)
        return path.join(FILE_DIR, 'boxscore', 'raw', file_name)

    @property
    def scraped_file_path(self):
        file_name = '{espn_id}.json.gz'.format(espn_id=self.resource_id)
        return path.join(FILE_DIR, 'boxscore', 'scraped', file_name)


class GameMeta(ResourceABC):

    def scrape(self, raw):
        tag = bs4.BeautifulSoup(raw)
        return espn.GameMeta(tag)

    @property
    def url(self):
        url_tmpl = 'http://espn.go.com/nba/boxscore?gameId={espn_id}'
        return url_tmpl.format(espn_id=self.resource_id)

    @property
    def raw_file_path(self):
        file_name = '{espn_id}.html.gz'.format(espn_id=self.resource_id)
        return path.join(FILE_DIR, 'boxscore', 'raw', file_name)

    @property
    def scraped_file_path(self):
        file_name = '{espn_id}.json.gz'.format(espn_id=self.resource_id)
        return path.join(FILE_DIR, 'meta', 'scraped', file_name)


class ShotChart(ResourceABC):

    def scrape(self, raw):
        tag = bs4.BeautifulSoup(raw)
        return espn.ShotChart(tag)

    @property
    def url(self):
        url_tmpl = 'http://sports.espn.go.com/nba/gamepackage/data/shot?gameId={espn_id}'
        return url_tmpl.format(espn_id=self.resource_id)

    @property
    def raw_file_path(self):
        file_name = '{espn_id}.xml.gz'.format(espn_id=self.resource_id)
        return path.join(FILE_DIR, 'shotchart', 'raw', file_name)

    @property
    def scraped_file_path(self):
        file_name = '{espn_id}.json.gz'.format(espn_id=self.resource_id)
        return path.join(FILE_DIR, 'shotchart', 'scraped', file_name)


class GameFlow(ResourceABC):

    def scrape(self, raw):
        tag = bs4.BeautifulSoup(raw)
        return espn.GameFlow(tag)

    @property
    def url(self):
        url_tmpl = 'http://sports.espn.go.com/nba/gamepackage/data/gameflow?gameId={espn_id}'
        return url_tmpl.format(espn_id=self.resource_id)

    @property
    def raw_file_path(self):
        file_name = '{espn_id}.xml.gz'.format(espn_id=self.resource_id)
        return path.join(FILE_DIR, 'gameflow', 'raw', file_name)

    @property
    def scraped_file_path(self):
        file_name = '{espn_id}.json.gz'.format(espn_id=self.resource_id)
        return path.join(FILE_DIR, 'gameflow', 'scraped', file_name)
