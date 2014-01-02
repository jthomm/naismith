import datetime

start = datetime.date(2013, 12, 31)
until = datetime.date.today()
#until = start + datetime.timedelta(days=1)

one_day = datetime.timedelta(days=1)



def log(message):
    print u'[{0}]\t{1}'.format(datetime.datetime.now().isoformat(), message)



problem_pbp_ids = ('2013120434428',)




from fetching import si

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
    start += one_day
