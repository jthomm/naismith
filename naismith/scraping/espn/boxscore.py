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
    def player_name(self):
        """Returns the player's abbreviated name."""
        return self._tds[0].text.split(u', ')[0]

    @property
    def position(self):
        """Returns the player's position."""
        return self._tds[0].text.split(u', ')[1]



class BoxScoreTr(BoxScoreTrABC):
    """Box score table row for members of the team that played.
    """

    @property
    def minutes_played(self):
        return self._tds[1].text

    @property
    def field_goals(self):
        return self._tds[2].text

    @property
    def three_pointers(self):
        return self._tds[3].text

    @property
    def free_throws(self):
        return self._tds[4].text

    @property
    def offensive_rebounds(self):
        return int(self._tds[5].text)

    @property
    def defensive_rebounds(self):
        return int(self._tds[6].text)

    @property
    def total_rebounds(self):
        return int(self._tds[7].text)

    @property
    def assists(self):
        return int(self._tds[8].text)

    @property
    def steals(self):
        return int(self._tds[9].text)

    @property
    def blocked_shots(self):
        return int(self._tds[10].text)

    @property
    def turnovers(self):
        return int(self._tds[11].text)

    @property
    def personal_fouls(self):
        return int(self._tds[12].text)

    @property
    def plus_minus(self):
        return int(self._tds[13].text)

    @property
    def points(self):
        return int(self._tds[14].text)

    @property
    def as_dict(self):
        return {attr_name: getattr(self, attr_name) for attr_name in \
                ('player_url',
                 'player_name',
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



class DNPBoxScoreTr(BoxScoreTrABC):
    """Box score table row for players that did not play.  Row will have
    two cells only.  Second cell gives reason for DNP.
    """

    @property
    def dnp_reason(self):
        return self._tds[1].text

    @property
    def as_dict(self):
        return {attr_name: getattr(self, attr_name) for attr_name in \
                ('player_url',
                 'player_name',
                 'position',
                 'dnp_reason',)}



class BoxScoreTbody(tuple):
    """tbody
    """

    def __new__(cls, tag):
        lst = list()
        for tr in tag.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) == 2:
                box_score_tr = DNPBoxScoreTr(tds)
            else:
                box_score_tr = BoxScoreTr(tds)
            lst.append(box_score_tr.as_dict)
        return super(BoxScoreTbody, cls).__new__(cls, lst)



class TeamBoxScore(dict):
    """One of two box score tables
    """

    def __init__(self, starters_tbody, bench_tbody):
        dict.__init__(self)
        self['starters'] = BoxScoreTbody(starters_tbody)
        self['bench'] = BoxScoreTbody(bench_tbody)



class BoxScore(dict):
    """box score
    """

    def __init__(self, tag):
        dict.__init__(self)
        mod_data = tag.find('table', {'class': 'mod-data'})
        tbodies = mod_data.find_all('tbody')
        self['away'] = TeamBoxScore(*tbodies[:2])
        self['home'] = TeamBoxScore(*tbodies[3:5])
