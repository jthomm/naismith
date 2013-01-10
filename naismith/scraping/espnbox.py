

class BoxScoreTrABC(object):
    """Object representation of a table row from the game's ESPN.com 
    box score. This is only valid for rows which correspond to player 
    stats (i.e. not for subtotals of table headers).
    """

    def __init__(self, tds):
        self._tds = tds

    @property
    def player_url(self):
        """Returns the player's NBA.com url."""
        return unicode(self._tds[0].a.attrs['href'])

    @property
    def player_abbr(self):
        """Returns the player's abbreviated name."""
        return self._tds[0].text



class BoxScoreTr(BoxScoreTrABC):
    """Box score table row for members of the team that played.
    """

    @property
    def position(self):
        return self._tds[1].text

    @property
    def minutes_played(self):
        return self._tds[2].text

    @property
    def field_goals(self):
        return self._tds[3].text

    @property
    def three_pointers(self):
        return self._tds[4].text

    @property
    def free_throws(self):
        return self._tds[5].text

    @property
    def offensive_rebounds(self):
        return int(self._tds[6].text)

    @property
    def defensive_rebounds(self):
        return int(self._tds[7].text)

    @property
    def total_rebounds(self):
        return int(self._tds[8].text)

    @property
    def assists(self):
        return int(self._tds[9].text)

    @property
    def steals(self):
        return int(self._tds[10].text)

    @property
    def blocked_shots(self):
        return int(self._tds[11].text)

    @property
    def turnovers(self):
        return int(self._tds[12].text)

    @property
    def personal_fouls(self):
        return int(self._tds[13].text)

    @property
    def plus_minus(self):
        return int(self._tds[14].text)

    @property
    def points(self):
        return int(self._tds[15].text)

    @property
    def as_dict(self):
        return {attr_name: getattr(self, attr_name) for attr_name in \
                ('player_url',
                 'player_abbr',
                 'position',
                 'minutes_played',
                 'field_goals',
                 'three_pointers',
                 'free_throws',
                 'plus_minus',
                 'offensive_rebounds',
                 'defensive_rebounds',
                 'total_rebounds',
                 'assists',
                 'personal_fouls',
                 'steals',
                 'turnovers',
                 'blocked_shots',
                 'points',)}




class TeamBoxScore(object):
    """One of two box score tables:
    
    >>> 
    >>> len(tag.find_all('table', {'id': 'nbaGITeamStats'}))
    2
    >>> 
    >>> 
    """

    def __init__(self, tag):
        for player_tr in tag.find_all(_is_player_tr):
            f


"""Utils"""

def _tag_text_stripped(td):
    return re.sub(r'[\n\s]+', u' ', td.text).strip()

def _is_player_tr(tag):
    return tag.name == 'tr' and \
           tag.a is not None and \
           tag.a.attrs.get('href', '')[:11] == '/playerfile'
