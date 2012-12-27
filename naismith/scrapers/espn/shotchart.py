class ShotChart(tuple):
    """Tuple of dictionaries containing information about each shot.
    """

    def __new__(cls, tag):
        """Instantiated with `tag` from ESPN.com shot chart resource:

        >>> import requests
        >>> import bs4
        >>> 
        >>> base_url = 'http://sports.espn.go.com'
        >>> url = base_url + '/nba/gamepackage/data/shot?gameId=400278120'
        >>> xml = requests.get(url).text
        >>> tag = bs4.BeautifulSoup(xml)
        >>> shots = Shots(xml)
        """
        lst = list()
        for shot in tag.find_all('shot'):
            attrs = shot.attrs
            lst.append({'made': True if attrs['made'] == 'true' else False,
                        'quarter': int(attrs['qtr']),
                        'desc': unicode(attrs['d']),
                        'player_id': unicode(attrs['pid']),
                        'player_name': unicode(attrs['p']),
                        'team': u'home' if attrs['t'] == 'h' else u'away',
                        'y': int(attrs['y']),
                        'x': int(attrs['x']),
                        'shot_id': unicode(attrs['id']),})
        return super(ShotChart, cls).__new__(cls, lst)
