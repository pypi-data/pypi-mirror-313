
from SharedData.Metadata import Metadata
from SharedData.Metadata import isnan

from SharedData.Logger import Logger
from SharedData.IO.AWSKinesis import KinesisLogStreamConsumer, KinesisStreamProducer
import os
import glob
import subprocess
import pytz
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime
from tzlocal import get_localzone
local_tz = pytz.timezone(str(get_localzone()))

#TODO: ADD STOPED STATE TO REALTIME ROUTINES
#TODO: MESSAGES OF PREVIOUS ROUTINES BEING ASINGED TO LATER ROUTINES
class Schedule:

    def __init__(self, schedule_name):
        self.schedule_name = schedule_name

        self.consumer = KinesisLogStreamConsumer()
        self.dflogs = pd.DataFrame([])
        self.producer = KinesisStreamProducer(os.environ['WORKERPOOL_STREAM'])

        self.LoadSchedule()

    def LoadSchedule(self):

        self.lastschedule = []
        self.schedule = []

        today = datetime.now().date()
        year = today.timetuple()[0]
        month = today.timetuple()[1]
        day = today.timetuple()[2]

        _sched = Metadata('SCHEDULES/'+self.schedule_name).static.reset_index()
        if _sched.empty:
            errmsg = 'Schedule %s not found!' % (self.schedule_name)
            Logger.log.error(errmsg)
            raise Exception(errmsg)
        sched = pd.DataFrame(columns=_sched.columns)
        for i, s in _sched.iterrows():
            if not isnan(s['runtimes']):
                runtimes = s['runtimes'].split(',')
                for t in runtimes:
                    hour = int(t.split(':')[0])
                    minute = int(t.split(':')[1])
                    dttm = local_tz.localize(
                        datetime(year, month, day, hour, minute))
                    s['runtimes'] = dttm
                    # sched = sched.reindex(columns=s.index.union(sched.columns))
                    sched = pd.concat([sched, pd.DataFrame(s).T])
            else:
                hour = int(0)
                minute = int(0)
                dttm = local_tz.localize(
                    datetime(year, month, day, hour, minute))
                s['runtimes'] = dttm
                # sched = sched.reindex(columns=s.index.union(sched.columns))
                sched = pd.concat([sched, pd.DataFrame(s).T])

        sched = sched.sort_values(
            by=['runtimes', 'name']).reset_index(drop=True)
        sched['routine'] = [s.replace('\\', '/') for s in sched['routine']]
        sched['computer'] = [s.split(':')[0] for s in sched['routine']]
        sched['script'] = [s.split(':')[-1] for s in sched['routine']]

        sched.loc[sched['dependencies'].isnull(), 'dependencies'] = ''
        sched['dependencies'] = [s.replace('\\', '/')
                                 for s in sched['dependencies']]

        sched['lastmsg'] = 'nan'
        sched['lastmsgts'] = pd.NaT
        sched['lastmsgage'] = np.nan

        sched['runmsgsent'] = False
        sched['runmsgts'] = pd.NaT
        sched['runmsgage'] = np.nan

        if not 'isrealtime' in sched.columns:
            sched['isrealtime'] = False

        sched['status'] = 'nan'
        sched['status'] = sched['status'].astype(str)

        # SAVE ROUTINES SCHEDULE IN EXECUTION SEQUENCE
        uruntimes = sched['runtimes'].unique()
        runtime = uruntimes[0]
        sched_sort = pd.DataFrame(columns=sched.columns)
        for runtime in uruntimes:
            # mark pending routines
            while True:
                idx = runtime.astimezone(tz=local_tz) >= sched['runtimes']
                idx = (idx) & ((sched['status'] == 'nan')
                               | (sched['status'] == 'WAITING DEPENDENCIES'))

                dfpending = sched[idx]
                expiredidx = dfpending.duplicated(['routine'], keep='last')
                if expiredidx.any():
                    expiredids = expiredidx.index[expiredidx]
                    sched.loc[expiredids, 'status'] = 'EXPIRED'
                dfpending = dfpending[~expiredidx]
                i = 0
                for i in dfpending.index:
                    r = dfpending.loc[i]

                    if not isnan(r['dependencies']):
                        run = True
                        sched.loc[i, 'status'] = 'WAITING DEPENDENCIES'
                        dependencies = r['dependencies'].replace(
                            '\n', '').split(',')
                        for dep in dependencies:
                            idx = sched['routine'] == dep
                            idx = (idx) & (
                                sched['runtimes'] <= runtime.astimezone(tz=local_tz))
                            ids = sched.index[idx]
                            if len(ids) == 0:
                                Logger.log.error(
                                    'Dependency not scheduled for '+r['routine'])
                                raise Exception(
                                    'Dependency not scheduled for '+r['routine'])
                            else:
                                if not str(sched.loc[ids[-1], 'status']) == 'COMPLETED':
                                    run = False
                        if run:
                            sched.loc[i, 'status'] = 'PENDING'
                    else:
                        sched.loc[i, 'status'] = 'PENDING'

                idx = sched['status'] == 'PENDING'
                if idx.any():
                    sched_sort = pd.concat([sched_sort, sched[idx]])
                    sched_sort['status'] = 'nan'
                    sched.loc[idx, 'status'] = 'COMPLETED'
                else:
                    break

        sched_sort.index.name = 'sequence'
        self.schedule = sched_sort
        self.schedule = self.schedule.reset_index(drop=True)
        self.lastschedule = self.schedule.copy()
        self.save()

    def updateLogs(self):
        local_tz = pytz.timezone(str(get_localzone()))
        # RefreshLogs
        dflogs = self.consumer.getLogs().copy()
        if not dflogs.empty:
            # CREATE ROUTINE INDEX FROM LOGS COLUMNS
            dflogs['routine'] = dflogs['user_name']+':'+dflogs['logger_name']
            # BUG: AttributeError: 'float' object has no attribute 'replace'
            dflogs.loc[dflogs['routine'].isnull(), 'routine'] = ''
            dflogs['routine'] = [s.replace('\\', '/')
                                 for s in dflogs['routine']]
            # LOCALIZE TIME
            dflogs = dflogs[dflogs['asctime'].notnull()].copy()
            dflogs['asctime'] = pd.to_datetime(dflogs['asctime'])
            dflogs['asctime'] = [dt.astimezone(
                tz=local_tz) for dt in dflogs['asctime']]
        self.dflogs = dflogs

    def UpdateRoutinesStatus(self):
        sched = self.schedule
        local_tz = pytz.timezone(str(get_localzone()))
        now = datetime.now().astimezone(tz=local_tz)        
        # RefreshLogs
        self.updateLogs()
        dflogs = self.dflogs
        if not dflogs.empty:
            # ROUTINES LAST MESSAGE
            for i in sched.index:
                r = sched.loc[i]
                idx = dflogs['routine'] == r['routine']
                idx = (idx) & (dflogs['asctime'] >= r['runtimes'])
                if np.any(idx):
                    sched.loc[i, 'lastmsg'] = dflogs[idx].iloc[-1]['message']
                    sched.loc[i, 'lastmsgts'] = dflogs[idx].iloc[-1]['asctime']

            # ROUTINES LAST MESSAGE AGE
            for i in sched.index:
                r = sched.loc[i]
                if (isinstance(r['lastmsgts'], pd.Timestamp))\
                        | isinstance(r['lastmsgts'], datetime):
                    if now > r['lastmsgts']:
                        sched.loc[i, 'lastmsgage'] = (now - r['lastmsgts']).seconds
                    else:
                        sched.loc[i, 'lastmsgage'] = 0

                    if (not r['isrealtime']) & (r['status'] != 'ERROR')\
                            & (r['status'] != 'EXPIRED'):
                        if sched.loc[i, 'lastmsgage'] <= 300:
                            sched.loc[i, 'status'] = 'RUNNING'
                        else:
                            sched.loc[i, 'status'] = 'DELAYED'
                        if r['isexternal']:
                            sched.loc[i, 'status'] += ' EXTERNAL'

            # ERROR ROUTINES
            dferr = dflogs[dflogs['message'] == 'ROUTINE ERROR!']
            dferr = dferr.reset_index(drop=True).sort_values(by='asctime')
            i = 0
            for i in dferr.index:
                r = dferr.iloc[i]
                idx = sched['routine'] == r['routine']
                idx = (idx) & (r['asctime'] >= sched['runtimes'])
                if idx.any():
                    ids = idx[::-1].idxmax()
                    sched.loc[ids, 'status'] = 'ERROR'
                    idx = (sched.loc[idx, 'status'] != 'COMPLETED')\
                        & (sched.loc[idx, 'status'] != 'ERROR')
                    idx = idx.index[idx]
                    sched.loc[idx, 'status'] = 'EXPIRED'

            # COMPLETED ROUTINES
            compl = dflogs[dflogs['message'] == 'ROUTINE COMPLETED!'].\
                reset_index(drop=True).sort_values(by='asctime')
            i = 0
            for i in compl.index:
                r = compl.iloc[i]
                idx = sched['routine'] == r['routine']
                idx = (idx) & (r['asctime'] >= sched['runtimes'])
                if idx.any():
                    ids = idx[::-1].idxmax()
                    sched.loc[ids, 'status'] = 'COMPLETED'
                    idx = (sched.loc[idx, 'status'] != 'COMPLETED')\
                        & (sched.loc[idx, 'status'] != 'ERROR')
                    idx = idx.index[idx]
                    sched.loc[idx, 'status'] = 'EXPIRED'

        # EXPIRED SCHED ROUTINES
        idx = now >= sched['runtimes']
        idx = (idx) & ((sched['status'] == 'nan') | (sched['status'].isnull()))
        dfexpired = sched[idx]
        expiredidx = dfexpired.duplicated(['routine'], keep='last')
        if expiredidx.any():
            expiredids = expiredidx.index[expiredidx]
            sched.loc[expiredids, 'status'] = 'EXPIRED'

        # PENDING SCHED ROUTINES
        idx = now >= sched['runtimes']
        idx = (idx) & (sched['isrealtime'] == False)
        idx = (idx) & (sched['runmsgsent'] == False)
        idx = (idx) & ((sched['status'] == 'nan') | (sched['status'].isnull())
                       | (sched['status'] == 'WAITING DEPENDENCIES'))
        dfpending = sched[idx]
        for i in dfpending.index:
            r = dfpending.loc[i]            
            depcompleted = True
            hasdependencies = not isnan(r['dependencies'])
            if hasdependencies:
                dependencies = r['dependencies'].replace('\n', '').split(',')
                for dep in dependencies:
                    idx = sched['routine'] == dep
                    idx = (idx) & (now >= sched['runtimes'])
                    ids = sched.index[idx]
                    if len(ids) == 0:
                        Logger.log.error(
                            'Dependency not scheduled for '+r['routine'])
                    else:
                        rdep = sched.loc[ids[-1]]
                        if not rdep['isrealtime']:
                            if (rdep['status'] != 'COMPLETED'):
                                depcompleted = False
                                break
                        else:
                            if not rdep['isexternal']:
                                if (rdep['status'] != 'RUNNING'):
                                    depcompleted = False
                                    break
                            else:
                                if (rdep['status'] != 'RUNNING EXTERNAL'):
                                    depcompleted = False
                                    break
                if not depcompleted:
                    sched.loc[i, 'status'] = 'WAITING DEPENDENCIES'

            if (not hasdependencies) | (depcompleted):

                if not sched.loc[i, 'isexternal']:
                    sched.loc[i, 'status'] = 'PENDING'
                else:
                    sched.loc[i, 'status'] = 'PENDING EXTERNAL'

        # REALTIME ROUTINES
        idx = (sched['isrealtime'])
        dfrealtime = sched[idx]
        for i in dfrealtime.index:
            r = sched.loc[i]
            depcompleted = True
            hasdependencies = not isnan(r['dependencies'])                        
            if hasdependencies:
                dependencies = r['dependencies'].replace('\n', '').split(',')
                for dep in dependencies:
                    idx = sched['routine'] == dep
                    idx = (idx) & \
                        ((now >= sched['runtimes']) | sched['isrealtime'])
                    ids = sched.index[idx]
                    if len(ids) == 0:
                        Logger.log.error(
                            'Dependency not scheduled for '+r['routine'])
                    else:
                        rdep = sched.loc[ids[-1]]
                        if not rdep['isrealtime']:
                            if (rdep['status'] != 'COMPLETED'):
                                depcompleted = False
                                break
                        else:
                            if not rdep['isexternal']:
                                if (rdep['status'] != 'RUNNING'):
                                    depcompleted = False
                                    break
                            else:
                                if (rdep['status'] != 'RUNNING EXTERNAL'):
                                    depcompleted = False
                                    break
                if not depcompleted:
                    sched.loc[i, 'status'] = 'WAITING DEPENDENCIES'

            if (not hasdependencies) | (depcompleted):
                if not r['isexternal']:
                    if (r['runmsgsent'] == False) & (r['lastmsg'] == 'nan'):
                        sched.loc[i, 'status'] = 'START'
                    elif (r['runmsgsent'] == False) & (r['lastmsg'] != 'nan'):
                        idx = (dflogs['message'] == 'ROUTINE STARTED!')\
                            & (dflogs['routine'] == r['routine'])
                        if (idx.any()) & (r['lastmsgage'] <= 60):
                            sched.loc[i, 'status'] = 'RUNNING'
                        elif (r['lastmsgage'] <= 60):
                            sched.loc[i, 'status'] = 'STARTING'
                        else:
                            sched.loc[i, 'status'] = 'RESTART'
                    elif (r['runmsgsent'] == True):
                        runmsgage = (now - sched.loc[i, 'runmsgts']).seconds
                        idx = (dflogs['message'] == 'ROUTINE STARTED!')\
                            & (dflogs['routine'] == r['routine'])\
                            & (dflogs['asctime'] >= r['runmsgts'])
                        if (idx.any()) & (r['lastmsgage'] <= 60):
                            sched.loc[i, 'status'] = 'RUNNING'
                        elif (r['lastmsgage'] <= 60):
                            if runmsgage <= 300:  # five minute to send first message
                                sched.loc[i, 'status'] = 'STARTING'
                            else:
                                sched.loc[i, 'status'] = 'RUNNING'
                        elif (r['lastmsgage'] > 60):
                            if runmsgage <= 300:  # five minute to send first message
                                sched.loc[i, 'status'] = 'STARTING'
                            else:
                                sched.loc[i, 'status'] = 'RESTART'

                elif r['isexternal']:
                    if (r['lastmsg'] == 'nan'):
                        sched.loc[i, 'status'] = 'START EXTERNAL'
                    elif (r['lastmsg'] != 'nan'):
                        idx = (dflogs['message'] == 'ROUTINE STARTED!')\
                            & (dflogs['routine'] == r['routine'])
                        if (idx.any()) & (r['lastmsgage'] <= 60):
                            sched.loc[i, 'status'] = 'RUNNING EXTERNAL'
                        elif (r['lastmsgage'] <= 60):
                            sched.loc[i, 'status'] = 'STARTING EXTERNAL'
                        elif (r['lastmsgage'] > 60+60):
                            sched.loc[i, 'status'] = 'RESTART EXTERNAL'

        self.schedule = sched

        if not self.schedule.equals(self.lastschedule):
            self.lastschedule = self.schedule.copy()
            self.save()
        return sched

    def RunPendingRoutines(self):
        newcommand = False
        sched = self.schedule

        # Run pending routines
        idx = sched['status'] == 'PENDING'
        idx = (idx) | (sched['status'] == 'START')
        idx = (idx) | (sched['status'] == 'RESTART')
        dfpending = sched[idx]
        for i in dfpending.index:
            r = dfpending.loc[i].copy()
            if (str(r['lastmsg']) == 'nan') | (r['status'] == 'RESTART'):
                newcommand = True
                target = r['computer']

                if 'SharedData' in r['script']:
                    repo = r['script'].split('.')[0]
                    routine = '.'.join(r['script'].split('.')[1:])
                    branch = ''
                else:
                    if '#' in r['script']:  # has branch
                        branch = r['script'].split('/')[0].split('#')[-1]
                        repo = r['script'].split('/')[0].split('#')[0]
                        routine = r['script'].replace(repo, '').\
                            replace('#', '').replace(branch, '')[1:]+'.py'
                    else:
                        branch = ''
                        repo = r['script'].split('/')[0]
                        routine = r['script'].replace(repo, '')[1:]+'.py'

                job = "routine"
                if r['status'] == 'RESTART':
                    job = "restart"

                data = {
                    "sender": "MASTER",
                    "job": job,
                    "target": target,
                    "repo": repo,
                    "routine": routine
                }

                if branch != '':
                    data['branch'] = branch

                if 'args' in r:
                    r['args'] = str(r['args'])
                    if (r['args'] != '') & (r['args'] != 'nan'):
                        data['args'] = r['args']

                self.producer.produce(data, 'command')
                sched.loc[r.name, 'status'] = 'RUNNING'
                now = datetime.now().astimezone(tz=local_tz)
                sched.loc[r.name, 'runmsgsent'] = True
                sched.loc[r.name, 'runmsgts'] = now
                sched.loc[r.name, 'lastmsg'] = 'Command to run sent...'
                sched.loc[r.name, 'lastmsgts'] = now
                sched.loc[r.name, 'lastmsgage'] = 0
                Logger.log.info('Command to run %s:%s sent...' %
                                (target, r['script']))

        self.schedule = sched
        if newcommand:
            self.lastschedule = self.schedule.copy()
            self.save()

        return sched

    def save(self):
        today = pd.Timestamp(pd.Timestamp.now().date())
        todaystr = today.strftime('%Y%m%d')
        md = Metadata('SCHEDULES/'+self.schedule_name+'/'+todaystr)
        md.static = self.schedule.copy()
        idx = md.static['runtimes'] != 'nan'
        md.static.loc[idx, 'runtimes'] = [d.replace(tzinfo=None) 
                                          for d in md.static['runtimes'][idx]]
        # md.static.loc[idx, 'runtimes'] = [d.tz_localize(
        #     None) for d in md.static['runtimes'][idx]]
        md.save()
