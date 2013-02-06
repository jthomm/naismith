
def get_name(play, player_num):
    fn = play['player-first-name-' + str(player_num)]
    ln = play['player-last-name-' + str(player_num)]
    if len(fn):
        return u', '.join([ln, fn])
    else:
        return None


key_words = (
    u'jump',
    u'dunk',
    u'bank',
    u'hook',
    u'running',
    u'driving',
    u'layup',
    u'turnaround',
    u'reverse',
    u'fade away',
    u'put back',
    u'finger roll',
    u'pull up',
    u'tip',
    u'alley oop',
    u'floating',
    u'step back',
)

def get_all_keywords(description):
    return [kw for kw in key_words if kw in description]
    

class Shot(object):
    
    def __init__(self, data):
        self.data = data
    
    @property
    def x(self):
        return float(self.data['x-coord'])
    
    @property
    def y(self):
        return float(self.data['y-coord'])
    
    @property
    def make(self):
        return self.data['event-desc'] == 'Field Goal Made'
    
    @property
    def team(self):
        return unicode(self.data['player-team-alias-1'].upper())
    
    @property
    def oppt(self):
        return unicode(self.data['player-team-alias-3'].upper())
    
    @property
    def shooter(self):
        return get_name(self.data, 1)
    
    @property
    def assist(self):
        return get_name(self.data, 2)
    
    @property
    def block(self):
        return get_name(self.data, 3)
    
    @property
    def point_value(self):
        return int(self.data['points-type'])
    
    @property
    def is_fast_break(self):
        return self.data['fastbreak']
    
    @property
    def tags(self):
        return tuple(get_all_keywords(self.data['detail-desc'].lower()))
    
    @property
    def desc(self):
        return unicode(self.data['details'])
    
    @property
    def as_dict(self):
        return {attr: getattr(self, attr) for attr in \
                ('x',
                 'y',
                 'make',
                 'team',
                 'oppt',
                 'shooter',
                 'assist',
                 'block',
                 'point_value',
                 'is_fast_break',
                 'tags',
                 'desc',)}
