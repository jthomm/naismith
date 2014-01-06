import datetime

start = datetime.date(2013, 10, 29)
until = datetime.date.today()
#until = start + datetime.timedelta(days=1)

one_day = datetime.timedelta(days=1)



def log(message):
    print u'[{0}]\t{1}'.format(datetime.datetime.now().isoformat(), message)



problem_pbp_ids = ('2013120434428',)




from fetching import si

# storing
shots = list()

while start < until:
    sp_id = start.strftime('%Y%m%d')
    log('Loading ' + sp_id)
    try:
        sp = si.SchedulePage(sp_id).load()
    except:
        log('There was a problem... skipping this date')
        start += one_day
        continue
    for contest in sp['contests']:
        pbp_id = sp_id + str(contest['id'])
        if pbp_id in problem_pbp_ids:
            continue
        log('\tnow ' + pbp_id)
        pbp = si.PlayByPlay(pbp_id).load()
        log('\tdone...')
        # storing
        for play in pbp['plays']:
            if play['event_desc'].startswith('Field Goal'):
                shots.append(play)
    start += one_day



import sqlite3

n = sqlite3.connect('shots.db')
c = n.cursor()

c.execute('DROP TABLE shots')

c.execute('''
    CREATE TABLE shots (
      game_id TEXT,
      away_abbr TEXT,
      home_abbr TEXT,
      team_abbr TEXT,
      shooter_name TEXT,
      assist_name TEXT,
      block_name TEXT,
      event_desc TEXT,
      detail_desc TEXT,
      details TEXT,
      point_value INTEGER,
      made INTEGER,
      x REAL,
      y REAL,
      json BLOB
    )
''')

import simplejson as json

for shot in shots:
    shot['x'] = -1*shot['x']
    _ = c.execute('INSERT INTO shots VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  (shot['game_id'],
                   shot['away_abbr'],
                   shot['home_abbr'],
                   shot['players'][0]['team_abbr'],
                   shot['players'][0]['last_name'] + ', ' + shot['players'][0]['first_name'],
                   None if shot['players'][1] is None else shot['players'][1]['last_name'] + ', ' + shot['players'][1]['first_name'],
                   None if shot['players'][2] is None else shot['players'][2]['last_name'] + ', ' + shot['players'][2]['first_name'],
                   shot['event_desc'],
                   shot['detail_desc'],
                   shot['details'],
                   shot['point_value'],
                   1 if shot['event_desc'].endswith('Made') else 0,
                   shot['x'],
                   shot['y'],
                   json.dumps(shot, indent=2),))

n.commit()

