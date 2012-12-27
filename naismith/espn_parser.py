import re



class MatchError(Exception):
    """Indicates the string provided to a `Program` instance does not match
    the instance's pattern.
    """

    message = '\'%s\' does not match pattern \'%s\''

    def __init__(self, string, pattern):
        self.string = string
        self.pattern = pattern

    def __str__(self):
        return self.message % (self.string, self.pattern)



class MatchProgram(object):
    """Combination of regular expression pattern and post procedure to be 
    called on match object's `groupdict`.  If no match object is found, calling 
    the program raises a `MatchError`.  Otherwise, the object returns the result 
    of calling its post procedure:

    >>> pattern = r'(?P<player_name>.+?) (?:traveling|discontinued dribble)'
    >>> post_proc = lambda group: {'type': u'turnover',
    ...                            'tov_type': u'traveling',
    ...                            'player': unicode(group['player_name']),}
    >>>
    >>> traveling = MatchProgram(pattern=pattern, post_proc=post_proc))
    >>>
    >>> traveling('LeBron James discontinued dribble')
    {'type': u'turnover', 'tov_type': u'traveling', 'player': u'LeBron James'}
    >>>
    >>> traveling('Kevin Garnett loose ball foul')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "match_program.py", line 46, in __call__
        raise MatchError(string, compiled_pattern.pattern)
    match_program.MatchError: 'Kevin Garnett loose ball foul' does not match pattern '(?P<player_name>.+?) (?:traveling|discontinued dribble)'
    """

    def __init__(self, pattern=r'.*', post_proc=lambda group: group):
        self.compiled_pattern = re.compile(pattern)
        self.post_proc = post_proc

    def __call__(self, string):
        compiled_pattern = self.compiled_pattern
        match_obj = compiled_pattern.search(string)
        if match_obj is None:
            raise MatchError(string, compiled_pattern.pattern)
        else:
            return self.post_proc(match_obj.groupdict())



class ProgramSet(object):
    """Ordered set of `MatchProgram` instances to be run consecutively until
    a match is found.  If no match is found, return a generic result to indicate 
    unknown or missing information.
    """

    def __init__(self, programs=None, generic_result=None):
        self.programs = list() if programs is None else programs
        self.generic_result = generic_result

    def __call__(self, string):
        for program in self.programs:
            try:
                return program(string)
            except MatchError:
                pass
        else:
            return self.generic_result



program_parameters_set = (
    (r'(?P<shooter>.+?) (?P<result>makes|misses) free throw(?P<clear_path> clear path)? (?P<number>\d) of (?P<of>\d)',
     lambda group: {'type': u'free_throw',
                    'shooter': _unicode_not_none(group['shooter']),
                    'make': True if group['result'] == 'makes' else False,
                    'number': int(group['number']),
                    'of': int(group['of']),
                    'clear_path': False if group['clear_path'] is None else True,
                   },
    ),
    (r'(?P<shooter>.+?) (?P<result>makes|misses) technical free throw',
     lambda group: {'type': u'technical_free_throw',
                    'shooter': _unicode_not_none(group['shooter']),
                    'make': True if group['result'] == 'makes' else False,
                   },
    ),
    (r'(?P<shooter>.+?) makes (?:\d+-foot )?(?P<shot_type>.+?)(?: \((?P<assist>.+?) assists\))?$',
     lambda group: {'type': u'make',
                    'shooter': _unicode_not_none(group['shooter']),
                    'shot_type': None if group['shot_type'] is None or group['shot_type'].endswith('-foot') else unicode(group['shot_type']),
                    'shot_value': 3 if group['shot_type'] is not None and group['shot_type'].startswith('three point') else 2,
                    'assister': _unicode_not_none(group['assist']),
                   },
    ),
    (r'(?P<shooter>.+?) misses(?: )?(?:\d+-foot )?(?P<shot_type>.+?)?$',
     lambda group: {'type': u'miss',
                    'shooter': _unicode_not_none(group['shooter']),
                    'shot_type': None if group['shot_type'] is None or group['shot_type'].endswith('-foot') else unicode(group['shot_type']),
                    'shot_value': 3 if group['shot_type'] is not None and group['shot_type'].startswith('three point') else 2,
                   },
    ),
    (r'(?P<block>.+?) blocks (?P<shooter>.+?)(?:\' |(?: )?\'s )(?:\d+-foot )?(?P<shot_type>.+?)$',
     lambda group: {'type': u'blocked',
                    'shooter': _unicode_not_none(group['shooter']),
                    'shot_type': None if group['shot_type'] is None or group['shot_type'].endswith('-foot') else unicode(group['shot_type']),
                    'shot_value': 3 if group['shot_type'] is not None and group['shot_type'].startswith('three point') else 2,
                    'blocker': _unicode_not_none(group['block']),
                   },
    ),
    (r'(?P<fouler>.+?) (?P<foul_type>offensive|loose ball|personal|shooting|clear path|personal take) foul \((?P<drawer>.+?) draws the foul\)',
     lambda group: {'type': u'foul',
                    'fouler': _unicode_not_none(group['fouler']),
                    'drawer': _unicode_not_none(group['drawer']),
                    'foul_type': _unicode_not_none(group['foul_type']),
                   },
    ),
    (r'(?P<fouler>.+?) offensive Charge \((?P<drawer>.+?) draws the foul\)',
     lambda group: {'type': u'foul',
                    'fouler': _unicode_not_none(group['fouler']),
                    'drawer': _unicode_not_none(group['drawer']),
                    'foul_type': u'offensive',
                   },
    ),
    (r'(?P<fouler>.+?) (?P<foul_type_prefix>shooting|personal) block(?: foul)? \((?P<drawer>.+?) draws the foul\)',
     lambda group: {'type': u'foul',
                    'fouler': _unicode_not_none(group['fouler']),
                    'drawer': _unicode_not_none(group['drawer']),
                    'foul_type': u'%s block' % group['foul_type_prefix'],
                   },
    ),
    (r'Double (?P<foul_type>technical) foul\: (?P<fouler_one>.+?) and (?P<fouler_two>.+?)$',
     lambda group: {'type': u'double_technical',
                    'fouler_one': _unicode_not_none(group['fouler_one']),
                    'fouler_two': _unicode_not_none(group['fouler_two']),
                   },
    ),
    (r'(?P<fouler>.+?) (?P<foul_type>technical) foul',
     lambda group: {'type': u'technical_foul',
                    'fouler': _unicode_not_none(group['fouler']),
                   },
    ),
    (r'(?P<fouler>.+?) (?P<foul_type>flagrant) foul type (?P<flagrant_type>\d) \((?P<drawer>.+?) draws the foul\)',
     lambda group: {'type': u'flagrant_foul',
                    'fouler': _unicode_not_none(group['fouler']),
                    'drawer': _unicode_not_none(group['drawer']),
                    'flagrant_type': int(group['flagrant_type']),
                   },
    ),
    (r'(?P<team>.+?) delay of game violation',
     lambda group: {'type': u'delay_of_game',
                    'delaying_team_nickname': _unicode_not_none(group['team']),
                   },
    ),
    (r'(?P<goaltender>.+?) (?P<goaltending_type>offensive|defensive) goaltending violation',
     lambda group: {'type': u'goaltending',
                    'goaltender': _unicode_not_none(group['goaltender']),
                    'goaltending_type': _unicode_not_none(group['goaltending_type']),
                   },
    ),
    (r'(?P<violator>.+?) (?P<violation_type>kicked ball|lane) violation',
     lambda group: {'type': u'violation',
                    'violation_type': _unicode_not_none(group['violation_type']),
                    'violator': _unicode_not_none(group['violator']),
                   },
    ),
    (r'(?P<rebounder>.+?) (?P<rebound_type>offensive|defensive) rebound',
     lambda group: {'type': u'rebound',
                    'rebounder': _unicode_not_none(group['rebounder']),
                    'rebound_type': _unicode_not_none(group['rebound_type']),
                   },
    ),
    (r'(?P<team>.+?) (?P<rebound_type>offensive|defensive) team rebound',
     lambda group: {'type': u'team_rebound',
                    'rebounding_team_nickname': _unicode_not_none(group['team']),
                    'rebound_type': _unicode_not_none(group['rebound_type']),
                   },
    ),
    (r'(?P<tov_type>shot clock) turnover',
     lambda group: {'type': u'turnover',
                    'turnover_type': u'shot clock violation',
                   },
    ),
    (r'(?P<turner>.+?) bad pass(?: \((?P<stealer>.+?) steals\))?',
     lambda group: {'type': u'turnover',
                    'turnover_type': u'bad pass',
                    'turner': _unicode_not_none(group['turner']),
                    'stealer': _unicode_not_none(group['stealer']),
                   },
    ),
    (r'(?P<turner>.+?) lost ball turnover \((?P<stealer>.+?) steals\)',
     lambda group: {'type': u'turnover',
                    'turnover_type': u'lost ball',
                    'turner': _unicode_not_none(group['turner']),
                    'stealer': _unicode_not_none(group['stealer']),
                   },
    ),
    (r'(?P<turner>.+?) possession lost ball turnover(?: )?(?P<stealer>.+?)?$',
     lambda group: {'type': u'turnover',
                    'turnover_type': u'lost ball',
                    'turner': _unicode_not_none(group['turner']),
                    'stealer': _unicode_not_none(group['stealer']),
                   },
    ),
    (r'(?P<turner>.+?) (?:(?P<turnover_type>steps out of bounds|out of bounds lost ball|double dribble|disc dribble|offensive goaltending) )?turnover',
     lambda group: {'type': u'turnover',
                    'turnover_type': _unicode_not_none(group['turnover_type']),
                    'turner': _unicode_not_none(group['turner']),
                   },
    ),
    (r'(?P<turner>.+?) traveling',
     lambda group: {'type': u'turnover',
                    'turnover_type': u'traveling',
                    'turner': _unicode_not_none(group['turner']),
                   },
    ),
    (r'(?P<player_in>.+?) enters the game for (?P<player_out>.+?)$',
     lambda group: {'type': u'substitution',
                    'player_in': _unicode_not_none(group['player_in']),
                    'player_out': _unicode_not_none(group['player_out']),
                   },
    ),
    (r'(?P<timeout_type>Official) timeout',
     lambda group: {'type': u'timeout',
                    'timeout_type': u'official',
                   },
    ),
    (r'(?P<team>.+?) (?P<timeout_type>Full|20 Sec\.) timeout',
     lambda group: {'type': u'timeout',
                    'timeout_type': u'full' if group['timeout_type'] == 'full' else u'twenty-second',
                    'timeout_team_nickname': _unicode_not_none(group['team']),
                   },
    ),
    (r'End of the (?P<quarter>\d)(?:st|nd|rd|th) Quarter',
     lambda group: {'type': u'period_end',
                    'period': int(group['quarter']),
                   },
    ),
    (r'End of the (?P<ovt>\d)(?:ST|ND|RD|TH) Overtime',
     lambda group: {'type': u'period_end',
                    'period': int(group['ovt']) + 4,
                   },
    ),
    (r'(?P<eog>End of Game)',
     lambda group: {'type': u'game_end',
                   },
    ),
    (r'(?P<away_player>.+?) vs\. (?P<home_player>.+?) \((?P<recoverer>.+?) gains possession\)',
     lambda group: {'type': u'jump_ball',
                    'away_player': _unicode_not_none(group['away_player']),
                    'home_player': _unicode_not_none(group['home_player']),
                    'recoverer': _unicode_not_none(group['recoverer']),
                   },
    ),
)



programs = [MatchProgram(pattern=params[0], post_proc=params[1]) \
            for params in program_parameters_set]

resolve_play_type = ProgramSet(programs=programs,
                               generic_result={'type': u'UNKNOWN'})



"""Utils"""

def _unicode_not_none(obj):
    return None if obj is None else unicode(obj)
