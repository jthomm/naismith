

regexes = ({'name': 'ft',
            'pattern': r'(?P<shooter>.+?) (?P<result>makes|misses) free throw (?P<number>\d) of (?P<of>\d)'},
           {'name': 'tech_ft',
            'pattern': r'(?P<shooter>.+?) (?P<result>makes|misses) technical free throw'},
           {'name': 'make',
            'pattern': r'(?P<shooter>.+?) makes (?:\d+-foot )?(?P<shot_type>.+?)(?: \((?P<assistant>.+?) assists\))?$'},
           {'name': 'miss',
            'pattern': r'(?P<shooter>.+?) misses(?: )?(?:\d+-foot )?(?P<shot_type>.+?)?$'},
           {'name': 'blocked',
            'pattern': r'(?P<blocker>.+?) blocks (?P<shooter>.+?)(?:\' |(?: )?\'s )(?:\d+-foot )?(?P<shot_type>.+?)$'},
           {'name': 'foul',
            'pattern': r'(?P<fouler>.+?) (?P<foul_type>offensive|loose ball|personal|shooting) foul \((?P<drawer>.+?) draws the foul\)'},
           {'name': 'charge',
            'pattern': r'(?P<fouler>.+?) (?P<foul_type>offensive) Charge \((?P<drawer>.+?) draws the foul\)'},
           {'name': 'tech_foul',
            'pattern': r'(?P<fouler>.+?) technical foul'},
           {'name': 'rebound',
            'pattern': r'(?P<rebounder>.+?) (?P<rebound_type>offensive|defensive) rebound'},
           {'name': 'team_rebound',
            'pattern': r'(?P<team>.+?) (?P<rebound_type>offensive|defensive) team rebound'},
           {'name': 'shot_clock_turnover',
            'pattern': r'shot clock turnover'},
           {'name': 'bad_pass_turnover',
               'pattern': r'(?P<player>.+?) bad pass(?: \((?P<stealer>.+?) steals\))?'},
           {'name': 'turnover',
            'pattern': r'(?P<player>.+?) (?:(?P<tov_type>out of bounds lost ball|lost ball) )?turnover(?: \((?P<stealer>.+?) steals\))?'},
           {'name': 'traveling',
            'pattern': r'(?P<player>.+?) traveling'},
           {'name': 'substitution',
            'pattern': r'(?P<player_in>.+?) enters the game for (?P<player_out>.+?)$'},
           {'name': 'official_timeout',
            'pattern': r'(?P<timeout_type>Official) timeout'},
           {'name': 'timeout',
            'pattern': r'(?P<team>.+?) (?P<timeout_type>Full|20 Sec\.) timeout'},
           {'name': 'qtr_end',
            'pattern': r'End of the (?P<quarter>\d)(?:st|nd|rd|th) Quarter'},
           {'name': 'game_end',
            'pattern': r'(?P<eog>End of Game)'},)


results = list()
for play in plays:
    desc = play['desc']
    for regex in regexes:
        mo = re.search(regex['pattern'], desc)
        if mo is not None:
            results.append((regex['name'], mo.groupdict(), desc))
            break
    else:
        results.append(('NO MATCH', None, desc))
