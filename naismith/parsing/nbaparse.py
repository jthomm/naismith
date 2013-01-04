from matchprogram import MatchProgram, ProgramSet
import re



def _unicode_not_none(obj):
    return None if obj is None else unicode(obj)



program_parameters_set = (
    (r'(?P<start_end>Start|End) of (?P<start_period>\d)(?:st|nd|rd|th) (?P<period_type>Quarter|Overtime)',
     lambda group: {'type': u'period_start' if group['start_end'] == 'Start' else u'period_end',
                    'period': int(group['start_period']) if group['period_type'] == 'Quarter' else int(group['start_period']) + 4
                   },
    ),
    (r'(?P<shooter>{player_abbr_pattern}) (?P<shot_type>.+?) [sS]hot: Made \(\d+ PTS\)(?: Assist: (?P<assister>{player_abbr_pattern}))?',
     lambda group: {'type': u'make',
                    'shooter': _unicode_not_none(group['shooter']),
                    'shot_type': _unicode_not_none(group['shot_type']),
                    'assister': _unicode_not_none(group['assister']),
                   },
    ),
    (r'(?P<shooter>{player_abbr_pattern}) (?P<shot_type>.+?) [sS]hot: Missed Block: (?P<blocker>{player_abbr_pattern})',
     lambda group: {'type': u'blocked',
                    'shooter': _unicode_not_none(group['shooter']),
                    'shot_type': _unicode_not_none(group['shot_type']),
                    'blocker': _unicode_not_none(group['blocker']),
                   },
    ),
    (r'(?P<shooter>{player_abbr_pattern}) (?P<shot_type>.+?) [sS]hot: Missed$',
     lambda group: {'type': u'miss',
                    'shooter': _unicode_not_none(group['shooter']),
                    'shot_type': _unicode_not_none(group['shot_type']),
                   },
    ),
    (r'Team Rebound',
     lambda group: {'type': u'team_rebound',
                   },
    ),
    (r'(?P<rebounder>{player_abbr_pattern}) Rebound',
     lambda group: {'type': u'rebound',
                    'rebounder': _unicode_not_none(group['rebounder']),
                   },
    ),
    (r'Team Turnover : (?P<turnover_type>.+?)(?: Turnover)?',
     lambda group: {'type': u'turnover',
                    'turner': u'team',
                    'turnover_type': _unicode_not_none(group['turnover_type']),
                   },
    ),
    (r'(?P<turner>{player_abbr_pattern}) Turnover : (?P<turnover_type>.+?) \(\d TO\) Steal:(?P<stealer>{player_abbr_pattern}) \(',
     lambda group: {'type': u'turnover',
                    'turner': _unicode_not_none(group['turner']),
                    'turnover_type': _unicode_not_none(group['turnover_type']),
                    'stealer': _unicode_not_none(group['stealer']),
                   },
    ),
    (r'(?P<turner>{player_abbr_pattern}) Turnover : (?P<turnover_type>.+?) \(',
     lambda group: {'type': u'turnover',
                    'turner': _unicode_not_none(group['turner']),
                    'turnover_type': _unicode_not_none(group['turnover_type']),
                   },
    ),
    (r'(?P<shooter>{player_abbr_pattern}) Free Throw Technical',
     lambda group: {'type': u'free_throw_technical',
                    'shooter': _unicode_not_none(group['shooter']),
                   },
    ),
    (r'(?P<shooter>{player_abbr_pattern}) Free Throw Flagrant (?P<number>\d) of (?P<of>\d) (?P<missed>Missed)?',
     lambda group: {'type': u'free_throw_flagrant',
                    'shooter': _unicode_not_none(group['shooter']),
                    'make': True if group['missed'] is None else False,
                    'number': int(group['number']),
                    'of': int(group['of']),
                   },
    ),
    (r'(?P<shooter>{player_abbr_pattern}) Free Throw (?P<number>\d) of (?P<of>\d) (?P<missed>Missed)?',
     lambda group: {'type': u'free_throw',
                    'shooter': _unicode_not_none(group['shooter']),
                    'make': True if group['missed'] is None else False,
                    'number': int(group['number']),
                    'of': int(group['of']),
                   },
    ),
    (r'Double Technical - (?P<fouler_one>{player_abbr_pattern}), (?P<fouler_two>{player_abbr_pattern})$',
     lambda group: {'type': u'double_technical',
                    'fouler_one': _unicode_not_none(group['fouler_one']),
                    'fouler_two': _unicode_not_none(group['fouler_two']),
                   },
    ),
    (r'(?P<fouler>{player_abbr_pattern}) Technical',
     lambda group: {'type': u'technical_foul',
                    'fouler': _unicode_not_none(group['fouler']),
                   },
    ),
    (r'(?P<fouler>.+?) Technical',
     lambda group: {'type': u'non_player_technical',
                    'fouler': _unicode_not_none(group['fouler']),
                   },
    ),
    (r'(?P<fouler>{player_abbr_pattern}) Foul: (?P<foul_type>.+?) \(',
     lambda group: {'type': u'foul',
                    'foul_type': _unicode_not_none(group['foul_type']),
                    'fouler': _unicode_not_none(group['fouler']),
                   },
    ),
    (r'(?P<player_out>{player_abbr_pattern}) Substitution replaced by (?P<player_in>{player_abbr_pattern})',
     lambda group: {'type': u'substitution',
                    'player_in': _unicode_not_none(group['player_in']),
                    'player_out': _unicode_not_none(group['player_out']),
                   },
    ),
    (r'Team Timeout : (?P<timeout_type>Regular|Short)',
     lambda group: {'type': u'timeout',
                    'timeout_type': _unicode_not_none(group['timeout_type']),
                   },
    ),
    (r'Jump Ball (?P<player_one>{player_abbr_pattern}) vs (?P<player_two>{player_abbr_pattern}) \((?P<recoverer>{player_abbr_pattern}) gains possession\)$',
     lambda group: {'type': u'jump_ball',
                    'player_one': _unicode_not_none(group['player_one']),
                    'player_two': _unicode_not_none(group['player_two']),
                    'recoverer': _unicode_not_none(group['recoverer']),
                   },
    ),
    (r'Team Violation : (?P<violation_type>.+?)(?: Violation)?$',
     lambda group: {'type': u'team_violation',
                    'violation_type': _unicode_not_none(group['violation_type']),
                   },
    ),
    (r'(?P<violator>{player_abbr_pattern}) Violation:(?P<violation_type>.+)',
     lambda group: {'type': u'violation',
                    'violation_type': _unicode_not_none(group['violation_type']),
                    'violator': _unicode_not_none(group['violator']),
                   },
    ),
    (r'^$',
     lambda group: {'type': u'BLANK',
                   },
    ),
)



class Parser(object):
    """Parses descriptions from `NBACom` instance plays.
    """

    def __init__(self, nbacom):
        self.nbacom = nbacom
        player_abbr_pattern = self._get_player_abbr_pattern()
        programs = list()
        for params in program_parameters_set:
            pattern = params[0].format(player_abbr_pattern=player_abbr_pattern)
            post_proc = params[1]
            programs.append(MatchProgram(pattern=pattern, post_proc=post_proc))
        self.parse_description = ProgramSet(match_programs=programs,
                                            default={'type': u'UNKNOWN',})

    def _get_player_abbr_pattern(self):
        abbrs = set()
        box_score = self.nbacom['box_score']
        for row in box_score['away'] + box_score['home']:
            player_abbr = row['player_abbr']
            abbrs.add(re.escape(player_abbr))
            match = re.search(r'[A-Z]\. (.+)', player_abbr)
            if match is not None:
                abbrs.add(re.escape(match.group(1)))
        return r'|'.join(abbrs)



class NBAParsedPlays(tuple):
    """Tuple of dictionaries containing information parsed from play or event 
    description merged with information scraped from NBA.com.
    """

    def __new__(cls, nbacom):
        parser = Parser(nbacom)
        lst = list()
        for scraped_play in nbacom['plays']:
            parsed_play = parser.parse_description(scraped_play['desc'])
            parsed_play.update(scraped_play)
            lst.append(parsed_play)
        return super(ParsedPlays, cls).__new__(cls, lst)
