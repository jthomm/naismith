import datetime
import re



class TeamData(dict):
    """Includes team nickname, final points total, and record as a result of
    the game.
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
    """Game channel, time, arena, and city.
    """

    def __init__(self, tag):
        """Must be initialized with `tag` representing game "vitals":
               
        >>> tag = entire_page.find('div', {'class': 'game-vitals'})
        >>> game_vitals = GameVitals(tag)
        """
        dict.__init__(self)
        self['channel'] = tag.p.strong and tag.p.strong.text
        _dt_string, _location = map(_tag_text_stripped, tag.div.find_all('p'))
        self['datetime'] = \
            datetime.datetime.strptime(_dt_string, '%I:%M %p ET, %B %d, %Y')
        venue, city = _location.split(', ', 1)
        self['venue'] = venue
        self['city'] = city



class MoreInfo(dict):
    """Game officials and attendance.
    """

    def __init__(self, tag):
        """Must be initialized with `tag` representing the second 
        'mod-content' div:
        
        >>> mod_content_divs = entire_page.find_all(**{'class': 'mod-content'})
        >>> tag = mod_content_divs[1]
        >>> more_info = MoreInfo(tag)
        """
        dict.__init__(self)
        contents = tag.contents
        self['attendance'] = int(re.sub(u',', u'', contents[-6].strip()))
        self['officials'] = contents[-9].strip().split(u', ')



class GameMeta(dict):
    """Game metadata, including team info and game time/venue.
    """

    def __init__(self, tag):
        """Initialize with `tag` representing entire ESPN.com box score page:

        >>> import requests
        >>> import bs4
        >>> 
        >>> html = requests.get(box_score_page_url).text
        >>> tag = bs4.BeautifulSoup(html)
        >>> game_meta = GameMeta(tag)
        """
        dict.__init__(self)
        self['away'] = TeamData(tag.find('div', {'class': 'team away'}))
        self['home'] = TeamData(tag.find('div', {'class': 'team home'}))
        vitals = GameVitals(tag.find('div', {'class': 'game-vitals'}))
        self.update(vitals)
        more_info = MoreInfo(tag.find_all(**{'class': 'mod-content'})[1])
        self.update(more_info)



"""Utils"""

def _tag_text_stripped(td):
    return re.sub(r'[\n\s]+', u' ', td.text).strip()
