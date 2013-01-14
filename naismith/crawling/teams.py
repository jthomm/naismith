team_identifiers = (
    {'nickname': u'Hawks', 'abbr': u'ATL', 'location': u'Atlanta'},
    {'nickname': u'Nets', 'abbr': u'BKN', 'location': u'Brooklyn'},
    {'nickname': u'Celtics', 'abbr': u'BOS', 'location': u'Boston'},
    {'nickname': u'Bobcats', 'abbr': u'CHA', 'location': u'Charlotte'},
    {'nickname': u'Bulls', 'abbr': u'CHI', 'location': u'Chicago'},
    {'nickname': u'Cavaliers', 'abbr': u'CLE', 'location': u'Cleveland'},
    {'nickname': u'Mavericks', 'abbr': u'DAL', 'location': u'Dallas'},
    {'nickname': u'Nuggets', 'abbr': u'DEN', 'location': u'Denver'},
    {'nickname': u'Pistons', 'abbr': u'DET', 'location': u'Detroit'},
    {'nickname': u'Warriors', 'abbr': u'GSW', 'location': u'Golden State'},
    {'nickname': u'Rockets', 'abbr': u'HOU', 'location': u'Houston'},
    {'nickname': u'Pacers', 'abbr': u'IND', 'location': u'Indiana'},
    {'nickname': u'Clippers', 'abbr': u'LAC', 'location': u'Los Angeles'},
    {'nickname': u'Lakers', 'abbr': u'LAL', 'location': u'Los Angeles'},
    {'nickname': u'Grizzlies', 'abbr': u'MEM', 'location': u'Memphis'},
    {'nickname': u'Heat', 'abbr': u'MIA', 'location': u'Miami'},
    {'nickname': u'Bucks', 'abbr': u'MIL', 'location': u'Milwaukee'},
    {'nickname': u'Timberwolves', 'abbr': u'MIN', 'location': u'Minnesota'},
    {'nickname': u'Hornets', 'abbr': u'NOH', 'location': u'New Orleans'},
    {'nickname': u'Knicks', 'abbr': u'NYK', 'location': u'New York'},
    {'nickname': u'Thunder', 'abbr': u'OKC', 'location': u'Oklahoma'},
    {'nickname': u'Magic', 'abbr': u'ORL', 'location': u'Orlando'},
    {'nickname': u'76ers', 'abbr': u'PHI', 'location': u'Philadelphia'},
    {'nickname': u'Suns', 'abbr': u'PHX', 'location': u'Phoenix'},
    {'nickname': u'Trail Blazers', 'abbr': u'POR', 'location': u'Portland'},
    {'nickname': u'Kings', 'abbr': u'SAC', 'location': u'Sacramento'},
    {'nickname': u'Spurs', 'abbr': u'SAS', 'location': u'San Antonio'},
    {'nickname': u'Raptors', 'abbr': u'TOR', 'location': u'Toronto'},
    {'nickname': u'Jazz', 'abbr': u'UTA', 'location': u'Utah'},
    {'nickname': u'Wizards', 'abbr': u'WAS', 'location': u'Washington'},
)

def _keyvals_match(x, y):
    for k, v in x.iteritems():
        if k not in y or y[k] != v:
            return False
    else:
        return True

def find_team(**kwargs):
    for team in team_identifiers:
        if _keyvals_match(kwargs, team):
            return team
