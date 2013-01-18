import requests
import bs4

import datetime
import simplejson as json

from os import path
import sys

import logging

sys.path.append(path.join(path.dirname(__file__), '../'))
from scraping.espn import SchedulePage


SCOREBOARD_URL = 'http://scores.espn.go.com/nba/scoreboard?date=%s'

DATA_DIR = path.join(path.dirname(__file__), '../data/espn/schedule/')


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def get_schedule_page(date_string):
    """`date_string` must be formatted '%Y%m%d', e.g.:
    >>> some_date = datetime.date.today()
    >>> some_date.strptime('%Y%m%d')
    '20130111'
    """
    url = SCOREBOARD_URL % date_string
    logger.info('requesting %s' % url)
    schedule_page_html = requests.get(url).text
    logger.info('parsing html')
    schedule_page_tag = bs4.BeautifulSoup(schedule_page_html)
    logger.info('loading `SchedulePage`')
    return SchedulePage(schedule_page_tag)


def json_datetime_default(obj):
    try:
        return obj.isoformat()
    except AttributeError:
        return obj


def save_schedule_page(schedule_page, date_string):
    logger.info('encoding json')
    schedule_page_json = json.dumps(schedule_page, indent=2,
                                    default=json_datetime_default)
    file_path = path.join(DATA_DIR, '%s.json' % date_string)
    with open(file_path, 'wb') as f:
        logger.info('writing to %s' % file_path)
        f.write(schedule_page_json)


def main(argv):
    try:
        date_string = argv[1]
    except IndexError:
        date_string = datetime.date.today().strftime('%Y%m%d')
    logger.info('getting schedule for %s' % date_string)
    schedule_page = get_schedule_page(date_string)
    save_schedule_page(schedule_page, date_string)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
