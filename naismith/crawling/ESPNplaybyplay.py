import re

class PlayByPlay(tuple):
    """Tuple of dictionaries containing information about each play. 
    Table headers and rows denoting quarter summary (one cell) are ommitted.
    """

    def __new__(cls, tag):
        """Instantiate with `tag` representing entire ESPN.com play-by-play 
        page:

        >>> import requests
        >>> import bs4
        >>> 
        >>> html = requests.get(pbp_page_url).text
        >>> tag = bs4.BeautifulSoup(html)
        >>> pbp = PlayByPlay(tag)
        """
        lst = list()
        pbp_table_tag = tag.find('table', {'class': 'mod-data'})
        for tr in pbp_table_tag.find_all('tr'):
            data = [_tag_text_stripped(td) for td in tr.find_all('td')]
            if len(data) == 2:
                # Timeout or end of quarter
                lst.append({'desc': data[1],
                            'clock': data[0],
                            'team': None,
                            'score': None,})
            elif len(data) == 4:
                # Home team plays on the right, away plays are on the left
                if data[1] == u'':
                    team = u'home'
                    desc = data[3]
                else:
                    team = u'away'
                    desc = data[1]
                lst.append({'desc': desc,
                            'clock': data[0],
                            'team': team,
                            'score': data[2],})
        return super(PlayByPlay, cls).__new__(cls, lst)

"""Utils"""

def _tag_text_stripped(td):
    return re.sub(r'[\n\s]+', u' ', td.text).strip()
