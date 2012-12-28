class TeamRow(object):
    """Represents one of two rows from `GameBox` instance
    """

    def __init__(self, tag):
        self._tag = tag

    @property
    def _team_links(self):
        return self._tag.ul.find_all('li')

    @property
    def _score_lis(self):
        return self._tag.find('ul', {'class': 'score'}).find_all('li')

    @property
    def location(self):
        return unicode(self._tag.attrs['class'][1])

    @property
    def url(self):
        return unicode(self._tag.p.span.a.attrs['href'])

    @property
    def nickname(self):
        return self._tag.p.span.text

    @property
    def roster_url(self):
        return unicode(self._team_links[0].a.attrs['href'])

    @property
    def stats_url(self):
        return unicode(self._team_links[1].a.attrs['href'])

    @property
    def scores(self):
        scores = list()
        for li in self._score_lis:
            try:
                scores.append(int(li.text))
            except ValueError:
                pass
        return scores

    @property
    def as_dict(self):
        return {attr_name: getattr(self, attr_name) for attr_name in \
                ('location',
                 'url',
                 'nickname',
                 'roster_url',
                 'stats_url',
                 'scores',)}



class GameBox(dict):
    """All metadata about a game
    """

    def __init__(self, tag):
        dict.__init__(self)
        self['espn_id'] = unicode(tag.attrs['id'][:9])
        _team_rows = map(TeamRow, tag.find_all(_is_team_row_tag))
        self['away'] = _team_rows[0].as_dict
        self['home'] = _team_rows[1].as_dict



class SchedulePage(tuple):
    """Tuple of gameboxes
    """

    def __new__(cls, tag):
        lst = list()
        for game_box_tag in tag.find_all(_is_game_box_tag):
            game_status_tag = game_box_tag.find(**{'class': 'game-status'})
            if game_status_tag.p.text != u'Postponed':
                lst.append(GameBox(game_box_tag))
        return super(SchedulePage, cls).__new__(cls, lst)



def _is_game_box_tag(tag):
    return tag.attrs.get('id', '').endswith('-gamebox')

def _is_team_row_tag(tag):
    return tag.attrs.get('class', None) in (['team', 'away'], ['team', 'home'],)
