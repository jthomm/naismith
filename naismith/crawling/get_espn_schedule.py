from bs4 import BeautifulSoup as bs
import simplejson as json
from os import path
import datetime
import requests
import sys
from espnschedule import SchedulePage



SCOREBOARD_URL = 'http://scores.espn.go.com/nba/scoreboard?date=%s'

DATA_DIR = path.join(path.dirname(__file__), '../data/espn/')

SCHEDULE_FILE_NAME = path.join(DATA_DIR, 'schedule.json')



def json_datetime_default(obj):
    try:
        return obj.isoformat()
    except AttributeError:
        return obj

def get_schedule_page(date_string):
    """`date_string` must be formatted '%Y%m%d', e.g.:
    >>> some_date = datetime.date.today()
    >>> some_date.strptime('%Y%m%d')
    '20130111'
    """
    url = SCOREBOARD_URL % date_string
    schedule_page_html = requests.get(url).text
    schedule_page_tag = bs(schedule_page_html)
    return SchedulePage(schedule_page_tag)

def append_games_to_schedule(schedule_page):
    old_schedule = json.loads(open(SCHEDULE_FILE_NAME, 'rb').read())
    new_schedule = list(schedule_page)
    for old_game in old_schedule:
        old_nba_id = old_game['nba_id']
        if not any(game['nba_id'] == old_nba_id for game in schedule_page):
            # Only append game if not found in `schedule_page`
            new_schedule.append(old_game)
    schedule_json = json.dumps(new_schedule, default=json_datetime_default,
                               indent=2)
    with open(SCHEDULE_FILE_NAME, 'wb') as f:
        print 'writing to %s' % SCHEDULE_FILE_NAME
        f.write(schedule_json)

def main(argv=None):
    if argv is None:
        date_string = datetime.date.today().strftime('%Y%m%d')
    else:
        date_string = argv[1]
    print 'getting games for %s...' % date_string
    append_games_to_schedule(get_schedule_page(date_string))


if __name__ == '__main__':
    sys.exit(main(sys.argv))
