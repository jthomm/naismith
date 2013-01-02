from matchprogram import MatchProgram, ProgramSet
import re

def _unicode_not_none(obj):
    return None if obj is None else unicode(obj)

class Parser(object):
    """Parses descriptions from `NBACom` instances
    """

    def __init__(self, nbacom):
        self._nbacom = nbacom
        self._set_player_abbr_pattern()
        self._set_program_parameters()
        self._set_program_set()

    def _set_player_abbr_pattern(self):
        box_score = self._nbacom['box_score']['away'] + self._nbacom['box_score']['home']
        abbrs = list()
        for row in box_score:
            player_abbr = row['player_abbr']
            abbrs.append(player_abbr)
            mo = re.search(r'[A-Z]\. (.+)', player_abbr)
            if mo is not None:
                abbrs.append(mo.group(1))
        self._player_abbr_pattern = r'|'.join(abbrs)

    def _set_program_parameters(self):
        _player_abbr_pattern = self._player_abbr_pattern
        self._program_parameters_set = (
            (r'(?P<start_end>Start|End) of (?P<start_period>\d)(?:st|nd|rd|th) (?P<period_type>Quarter|Overtime)',
             lambda group: {'type': u'period_start' if group['start_end'] == 'Start' else u'period_end',
                            'period': int(group['start_period']) if group['period_type'] == 'Quarter' else int(group['start_period']) + 4
                           },
            ),
            (r'(?P<shooter>%s) (?P<shot_type>.+?) [sS]hot: Made \(\d+ PTS\)(?: Assist: (?P<assister>%s))?' % (_player_abbr_pattern, _player_abbr_pattern,),
             lambda group: {'type': u'make',
                            'shooter': _unicode_not_none(group['shooter']),
                            'shot_type': _unicode_not_none(group['shot_type']),
                            'shot_value': 3 if group['shot_type'] == '3pt' else 2,
                            'assister': _unicode_not_none(group['assister']),
                           },
            ),
            (r'(?P<shooter>%s) (?P<shot_type>.+?) [sS]hot: Missed Block: (?P<blocker>%s)' % (_player_abbr_pattern, _player_abbr_pattern,),
             lambda group: {'type': u'blocked',
                            'shooter': _unicode_not_none(group['shooter']),
                            'shot_type': _unicode_not_none(group['shot_type']),
                            'shot_value': 3 if group['shot_type'] == '3pt' else 2,
                            'blocker': _unicode_not_none(group['blocker']),
                           },
            ),
            (r'(?P<shooter>%s) (?P<shot_type>.+?) [sS]hot: Missed$' % (_player_abbr_pattern,),
             lambda group: {'type': u'miss',
                            'shooter': _unicode_not_none(group['shooter']),
                            'shot_type': _unicode_not_none(group['shot_type']),
                            'shot_value': 3 if group['shot_type'] == '3pt' else 2,
                           },
            ),
            (r'Team Rebound',
             lambda group: {'type': u'team_rebound',
                           },
            ),
            (r'(?P<rebounder>%s) Rebound' % (_player_abbr_pattern,),
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
            (r'(?P<turner>%s) Turnover : (?P<turnover_type>.+?) \(\d TO\) Steal:(?P<stealer>%s) \(' % (_player_abbr_pattern, _player_abbr_pattern,),
             lambda group: {'type': u'turnover',
                            'turner': _unicode_not_none(group['turner']),
                            'turnover_type': _unicode_not_none(group['turnover_type']),
                            'stealer': _unicode_not_none(group['stealer']),
                           },
            ),
            (r'(?P<turner>%s) Turnover : (?P<turnover_type>.+?) \(' % (_player_abbr_pattern,),
             lambda group: {'type': u'turnover',
                            'turner': _unicode_not_none(group['turner']),
                            'turnover_type': _unicode_not_none(group['turnover_type']),
                           },
            ),
            (r'(?P<shooter>%s) Free Throw Technical' % (_player_abbr_pattern,),
             lambda group: {'type': u'free_throw_technical',
                            'shooter': _unicode_not_none(group['shooter']),
                           },
            ),
            (r'(?P<shooter>%s) Free Throw Flagrant (?P<number>\d) of (?P<of>\d) (?P<missed>Missed)?' % (_player_abbr_pattern,),
             lambda group: {'type': u'free_throw_flagrant',
                            'shooter': _unicode_not_none(group['shooter']),
                            'make': True if group['missed'] is None else False,
                            'number': int(group['number']),
                            'of': int(group['of']),
                           },
            ),
            (r'(?P<shooter>%s) Free Throw (?P<number>\d) of (?P<of>\d) (?P<missed>Missed)?' % (_player_abbr_pattern,),
             lambda group: {'type': u'free_throw',
                            'shooter': _unicode_not_none(group['shooter']),
                            'make': True if group['missed'] is None else False,
                            'number': int(group['number']),
                            'of': int(group['of']),
                           },
            ),
            (r'Double Technical - (?P<fouler_one>%s), (?P<fouler_two>%s)$' % (_player_abbr_pattern, _player_abbr_pattern,),
             lambda group: {'type': u'double_technical',
                            'fouler_one': _unicode_not_none(group['fouler_one']),
                            'fouler_two': _unicode_not_none(group['fouler_two']),
                           },
            ),
            (r'(?P<fouler>%s) Technical' % (_player_abbr_pattern,),
             lambda group: {'type': u'technical_foul',
                            'fouler': _unicode_not_none(group['fouler']),
                           },
            ),
            (r'(?P<fouler>.+?) Technical',
             lambda group: {'type': u'non_player_technical',
                            'fouler': _unicode_not_none(group['fouler']),
                           },
            ),
            (r'(?P<fouler>%s) Foul: (?P<foul_type>.+?) \(' % (_player_abbr_pattern,),
             lambda group: {'type': u'foul',
                            'foul_type': _unicode_not_none(group['foul_type']),
                            'fouler': _unicode_not_none(group['fouler']),
                           },
            ),
            (r'(?P<player_out>%s) Substitution replaced by (?P<player_in>%s)' % (_player_abbr_pattern, _player_abbr_pattern,),
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
            (r'Jump Ball (?P<player_one>%s) vs (?P<player_two>%s) \((?P<recoverer>%s) gains possession\)$' % (_player_abbr_pattern, _player_abbr_pattern, _player_abbr_pattern,),
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
            (r'(?P<violator>%s) Violation:(?P<violation_type>.+)' % (_player_abbr_pattern,),
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

    def _set_program_set(self):
        _match_programs = [MatchProgram(*params) 
                           for params in self._program_parameters_set]
        self._program_set = ProgramSet(match_programs=_match_programs,
                                       default={'type': u'UNKNOWN',})

    def resolve_play_type(self, description):
        return self._program_set(description)
