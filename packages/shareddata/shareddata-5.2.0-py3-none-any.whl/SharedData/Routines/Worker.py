# implements a decentralized routines worker
# connects to worker pool
# broadcast heartbeat
# listen to commands
# environment variables:
# SOURCE_FOLDER
# WORKERPOOL_STREAM
# GIT_SERVER
# GIT_USER
# GIT_ACRONYM
# GIT_TOKEN

import os
import time
import sys
import numpy as np
import importlib.metadata


from SharedData.Routines.WorkerLib import *
from SharedData.IO.AWSKinesis import *
from SharedData.Logger import Logger
from SharedData.SharedData import SharedData
shdata = SharedData('SharedData.Routines.Worker', user='worker')

SLEEP_TIME = int(os.environ['SLEEP_TIME'])

SCHEDULE_NAMES = ''
if len(sys.argv) >= 2:
    SCHEDULE_NAMES = str(sys.argv[1])

try:
    SHAREDDATA_VERSION = importlib.metadata.version("shareddata")
    Logger.log.info('SharedData Worker version %s STARTED!' % (SHAREDDATA_VERSION))
except:
    Logger.log.info('SharedData Worker STARTED!')


if SCHEDULE_NAMES != '':
    Logger.log.info('SharedData Worker schedules:%s STARTED!' % (SCHEDULE_NAMES))
    start_schedules(SCHEDULE_NAMES)

consumer = KinesisStreamConsumer(os.environ['WORKERPOOL_STREAM'])

lastheartbeat = time.time()

routines = []

Logger.log.info('ROUTINE STARTED!')
while True:
    # try:

    if not consumer.consume():
        consumer.get_stream()
        Logger.log.error('Cannot consume workerpool messages!')
        time.sleep(5)

    update_routines(routines)

    for record in consumer.stream_buffer:
        print('Received:'+str(record))

        command = record
        if ('job' in command) & ('target' in command):
            if ((command['target'].lower() == os.environ['USER_COMPUTER'].lower())
                    | (command['target'] == 'ALL')):
                process_command(command,routines)

    routines = remove_finished_routines(routines)

    consumer.stream_buffer = []

    if (time.time()-lastheartbeat > 15):
        lastheartbeat = time.time()
        Logger.log.debug('#heartbeat#')

    time.sleep(SLEEP_TIME + SLEEP_TIME*np.random.rand() - SLEEP_TIME/2)

    # except Exception as e:
    #     Logger.log.error('Worker ERROR\n%s' % (str(e)))
    #     consumer.stream_buffer = []
    #     time.sleep(SLEEP_TIME + SLEEP_TIME*np.random.rand() - SLEEP_TIME/2)
