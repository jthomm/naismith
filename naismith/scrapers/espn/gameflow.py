class GameFlow(tuple):
    """Tuple of dictionaries containing away and home team scores and number
    of seconds passed in the game.
    """
    #
    def __new__(cls, tag):
        """Instantiated with `tag` from ESPN.com game flow resource:

        >>> import requests
        >>> import bs4
        >>> 
        >>> base_url = 'http://sports.espn.go.com'
        >>> url = base_url + '/nba/gamepackage/data/gameflow?gameId=400278120'
        >>> xml = requests.get(url).text
        >>> tag = bs4.BeautifulSoup(xml)
        >>> shots = Shots(xml)
        """
        lst = list()
        for score in tag.find_all('s'):
            attrs = score.attrs
            lst.append({'away': int(attrs['a']),
                        'home': int(attrs['h']),
                        'seconds': int(float(attrs['t'])),})
        return super(GameFlow, cls).__new__(cls, lst)
