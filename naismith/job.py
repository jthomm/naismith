from naismith import NBACom
from bs4 import BeautifulSoup as bs
import requests
import datetime
import simplejson as json
from os import path
import sys



def json_default(obj):
    try:
        return obj.isoformat()
    except AttributeError:
        return obj


class GameDate(object):
    """Collects all game data for a given day and saves as json."""
    
    def __init__(self, date):
        self._date = date
        self._scrape_game_urls()
        self._get_game_htmls()

    @property
    def url(self):
        return 'http://www.nba.com/gameline/%s/' % self._date.strftime('%Y%m%d')

    def _scrape_game_urls(self):
        res = requests.get(self.url)
        tag = bs(res.text)
        self._game_urls = ['http://www.nba.com%s' % t.a.attrs['href'] for t in \
                           tag.find_all('div', {'class': 'nbaFnlMnRecapDiv'})]

    def _get_game_htmls(self):
        self._game_htmls = [requests.get(url).text for url in self._game_urls]

    def _extract_game_data(self):
        self._game_data = [NBACom(html) for html in self._game_htmls]

    def save_game_data(self):
        for game in self._game_data:
            game_id = u''.join((game.date.strftime('%Y%m%d'),
                                game.away_abbr, game.home_abbr,))
            print 'Saving %s...' % game_id
            json_str = json.dumps(game.as_dict, default=json_default, indent=2)
            with open(u'%s.json' % game_id, 'wb') as f:
                f.write(json_str.replace('\u00A0', ''))



date = datetime.date(2012, 10, 31)
end_date = datetime.date(2012, 11, 4)

while date < end_date:
    gd = GameDate(date)
    gd.save_game_data()
    date += datetime.timedelta(days=1)
