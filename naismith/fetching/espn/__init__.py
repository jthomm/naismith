from os import path
FILE_DIR = path.dirname(path.abspath(__file__))

import sys
PKG_DIR = path.dirname(FILE_DIR)
sys.path.append(PKG_DIR)

from datamanager import DataManager

from scraping import espn

import bs4


DATA_DIR = path.join(path.dirname(PKG_DIR), 'files', 'espn')


class ScheduleManager(DataManager):

    def scrape(self, raw):
        tag = bs4.BeautifulSoup(raw)
        return espn.SchedulePage(tag)

    def url_for(self, date_string):
        url_template = 'http://espn.go.com/nba/scoreboard?date={date_string}'
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
        return espn.PlayByPlay(tag)

    def url_for(self, espn_id):
        url_template = 'http://espn.go.com/nba/playbyplay?gameId={gid}&period=0'
        return url_template.format(gid=espn_id)

    def raw_file_path(self, espn_id):
        file_name = '{espn_id}.html.gz'.format(espn_id=espn_id)
        return path.join(DATA_DIR, 'playbyplay', 'raw', file_name)

    def scraped_file_path(self, espn_id):
        file_name = '{espn_id}.json.gz'.format(espn_id=espn_id)
        return path.join(DATA_DIR, 'playbyplay', 'scraped', file_name)


class BoxScoreManager(DataManager):
    
    def scrape(self, raw):
        tag = bs4.BeautifulSoup(raw)
        return espn.BoxScore(tag)

    def url_for(self, espn_id):
        url_template = 'http://espn.go.com/nba/boxscore?gameId={espn_id}'
        return url_template.format(espn_id=espn_id)

    def raw_file_path(self, espn_id):
        file_name = '{espn_id}.html.gz'.format(espn_id=espn_id)
        return path.join(DATA_DIR, 'boxscore', 'raw', file_name)

    def scraped_file_path(self, espn_id):
        file_name = '{espn_id}.json.gz'.format(espn_id=espn_id)
        return path.join(DATA_DIR, 'boxscore', 'scraped', file_name)


class GameMetaManager(DataManager):

    def scrape(self, raw):
        tag = bs4.BeautifulSoup(raw)
        return espn.GameMeta(tag)

    def url_for(self, espn_id):
        url_template = 'http://espn.go.com/nba/boxscore?gameId={espn_id}'
        return url_template.format(espn_id=espn_id)

    def raw_file_path(self, espn_id):
        file_name = '{espn_id}.html.gz'.format(espn_id=espn_id)
        return path.join(DATA_DIR, 'boxscore', 'raw', file_name)

    def scraped_file_path(self, espn_id):
        file_name = '{espn_id}.json.gz'.format(espn_id=espn_id)
        return path.join(DATA_DIR, 'meta', 'scraped', file_name)


class ShotChartManager(DataManager):
    
    def scrape(self, raw):
        tag = bs4.BeautifulSoup(raw)
        return espn.ShotChart(tag)

    def url_for(self, espn_id):
        url_template = 'http://sports.espn.go.com/nba/gamepackage/data/shot?gameId={espn_id}'
        return url_template.format(espn_id=espn_id)

    def raw_file_path(self, espn_id):
        file_name = '{espn_id}.xml.gz'.format(espn_id=espn_id)
        return path.join(DATA_DIR, 'shotchart', 'raw', file_name)

    def scraped_file_path(self, espn_id):
        file_name = '{espn_id}.json.gz'.format(espn_id=espn_id)
        return path.join(DATA_DIR, 'shotchart', 'scraped', file_name)


class GameFlowManager(DataManager):
    
    def scrape(self, raw):
        tag = bs4.BeautifulSoup(raw)
        return espn.GameFlow(tag)

    def url_for(self, espn_id):
        url_template = 'http://sports.espn.go.com/nba/gamepackage/data/gameflow?gameId={espn_id}'
        return url_template.format(espn_id=espn_id)

    def raw_file_path(self, espn_id):
        file_name = '{espn_id}.xml.gz'.format(espn_id=espn_id)
        return path.join(DATA_DIR, 'gameflow', 'raw', file_name)

    def scraped_file_path(self, espn_id):
        file_name = '{espn_id}.json.gz'.format(espn_id=espn_id)
        return path.join(DATA_DIR, 'gameflow', 'scraped', file_name)
