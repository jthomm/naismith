class BoxScoreTrABC(object):
    """Object representation of a table row from the game's NBA.com 
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
    def plus_minus(self):
        return int(self._tds[6].text)

    @property
    def offensive_rebounds(self):
        return int(self._tds[7].text)

    @property
    def defensive_rebounds(self):
        return int(self._tds[8].text)

    @property
    def total_rebounds(self):
        return int(self._tds[9].text)

    @property
    def assists(self):
        return int(self._tds[10].text)

    @property
    def personal_fouls(self):
        return int(self._tds[11].text)

    @property
    def steals(self):
        return int(self._tds[12].text)

    @property
    def turnovers(self):
        return int(self._tds[13].text)

    @property
    def blocked_shots(self):
        return int(self._tds[14].text)

    @property
    def points(self):
        return int(self._tds[16].text)

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
                 'player_abbr',
                 'dnp_reason',)}



class TeamBoxScore(tuple):
    """Object representation of a single team's box score table (box 
    score has one table for each team). Tuple contains one row for each
    player on a team's roster.
    """

    def __new__(cls, tag):
        """Must be instantiated with `tag` representing box score table."""
        lst = [box_score_tr.as_dict for box_score_tr in \
               [BoxScoreTr(tds) if len(tds) > 2 else DNPBoxScoreTr(tds) \
                for tds in [tr.find_all('td') \
                            for tr in tag.find_all(_is_player_tr)]]]
        return super(TeamBoxScore, cls).__new__(cls, lst)



class BoxScore(dict):
    """box score
    """

    def __init__(self, tag):
        dict.__init__(self)
        box_tables = tag.find_all(id='nbaGITeamStats')
        self['away'] = TeamBoxScore(box_tables[0])
        self['home'] = TeamBoxScore(box_tables[1])



"""Utils"""

def _is_player_tr(tag):
    return tag.name == 'tr' and \
           'class' in tag.attrs and \
           tag.attrs['class'] in (['odd'], ['even']) and \
           tag.a is not None
