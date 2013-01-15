import re

class PlayByPlay(tuple):
    """Tuple of dictionaries containing information about each play. 
    Table rows containing only team names (two cells) are ommitted.
    """

    def __new__(cls, tag):
        """Instantiate with `tag` representing entire NBA.com play-by-play 
        page:

        >>> import requests
        >>> import bs4
        >>> 
        >>> html = requests.get(pbp_page_url).text
        >>> tag = bs4.BeautifulSoup(html)
        >>> pbp = PlayByPlay(tag)
        """
        lst = list()
        pbp_table_tag = tag.find(**{'id': 'nbaGIPlay'}).table
        for tr in pbp_table_tag.find_all('tr'):
            data = [_tag_text_stripped(td) for td in tr.find_all('td')]
            if len(data) == 1:
                # Usually marks the start or end of a quarter
                lst.append({'desc': data[0],
                            'clock': None,
                            'team': None,
                            'score': None,})
            elif len(data) == 3:
                # Home team plays on the right, away plays are on the left
                if data[0] == u'':
                    team = u'home'
                    desc = data[2]
                else:
                    team = u'away'
                    desc = data[0]
                try:
                    clock, score = data[1].split(u' ', 1)
                except ValueError:
                    clock = data[1]
                    score = None
                lst.append({'desc': desc,
                            'clock': clock,
                            'team': team,
                            'score': score,})
        return super(PlayByPlay, cls).__new__(cls, lst)



"""Utils"""

def _tag_text_stripped(td):
    return re.sub(r'[\n\s]+', u' ', td.text).strip()
