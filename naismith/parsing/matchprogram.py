import re



class MatchError(Exception):
    """Indicates the string provided to a `MatchProgram` instance does not match
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
    a match is found.  If no match is found, return a default result to indicate 
    unknown or missing information.
    """

    def __init__(self, match_programs=None, default=None):
        self.match_programs = match_programs or list()
        self.default = default or dict()

    def __call__(self, string):
        for match_program in self.match_programs:
            try:
                return match_program(string)
            except MatchError:
                pass
        else:
            return self.default
