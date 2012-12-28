import datetime
import re



class PlayByPlay(tuple):
    """Tuple of dictionaries containing information about each play. 
    Table headers and rows denoting quarter summary (one cell) are ommitted.
    """

    def __new__(cls, tag):
        """Must be instantiated with `tag` representing play-by-play table:
               
        >>> tag = entire_page.find('table', {'class': 'mod-data'})
        >>> plays = PlayByPlay(tag)
        """
        lst = list()
        for tr in tag.find_all('tr'):
            data = [_tag_text_stripped(td) for td in tr.find_all('td')]
            if len(data) == 2:
                # Timeout or end of quarter
                lst.append({'desc': data[1],
                            'clock': data[0],
                            'team': None,
                            'score': None,})
            elif len(data) == 4:
                # Home team plays on the right, away plays are on the left
                if data[1] == u'':
                    team = u'home'
                    desc = data[3]
                else:
                    team = u'away'
                    desc = data[1]
                lst.append({'desc': desc,
                            'clock': data[0],
                            'team': team,
                            'score': data[2],})
        return super(PlayByPlay, cls).__new__(cls, lst)



class TeamData(dict):
    """Dict with team nickname, final score, and record at the time of game
    """

    def __init__(self, tag):
        """Must be initialized with `tag` representing team div:
               
        >>> tag = entire_page.find('div', {'class': 'team away'})
        >>> away_team_data = TeamData(tag)
        """
        dict.__init__(self)
        self['team_nickname'] = tag.h3.a.text
        self['final_score'] = int(tag.h3.span.text)
        self['record'] = tag.p.text



class GameVitals(dict):
    """Game channel, time, arena, and city
    """

    def __init__(self, tag):
        """Must be initialized with `tag` representing game "vitals":
               
        >>> tag = entire_page.find('div', {'class': 'game-vitals'})
        >>> game_vitals = GameVitals(tag)
        """
        dict.__init__(self)
        self['channel'] = tag.p.strong and tag.p.strong.text
        _dt_string, location = map(_tag_text_stripped, tag.div.find_all('p'))
        self['datetime'] = \
            datetime.datetime.strptime(_dt_string, '%I:%M %p ET, %B %d, %Y')
        arena, city = location.split(', ', 1)
        self['arena'] = arena
        self['city'] = city



class ESPNCom(dict):
    """Top-level API for accessing ESPN.com play-by-play page data.
    """

    def __init__(self, tag):
        """Initialize with `tag` representing entire ESPN.com play-by-play page:

        >>> import requests
        >>> import bs4
        >>> 
        >>> html = requests.get(pbp_page_url).text
        >>> tag = bs4.BeautifulSoup(html)
        >>> game = ESPNCom(tag)
        """
        dict.__init__(self)
        self['away'] = TeamData(tag.find('div', {'class': 'team away'}))
        self['home'] = TeamData(tag.find('div', {'class': 'team home'}))
        vitals = GameVitals(tag.find('div', {'class': 'game-vitals'}))
        self.update(vitals)
        self['plays'] = PlayByPlay(tag.find('table', {'class': 'mod-data'}))



"""Utils"""

def _tag_text_stripped(td):
    return re.sub(r'[\n\s]+', u' ', td.text).strip()
