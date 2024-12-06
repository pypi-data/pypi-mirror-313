import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

if 'AWS_PROFILE' in os.environ:
    if not 'S3_AWS_PROFILE' in os.environ:
        os.environ['S3_AWS_PROFILE'] = os.environ['AWS_PROFILE']
    if not 'KINESIS_AWS_PROFILE' in os.environ:
        os.environ['KINESIS_AWS_PROFILE'] = os.environ['AWS_PROFILE']
else:    
    if (not 'AWS_ACCESS_KEY_ID' in os.environ)\
        or (not 'AWS_SECRET_ACCESS_KEY' in os.environ):
        raise Exception('Missing AWS login credentials environment variable!')

if not 'DATABASE_FOLDER' in os.environ:
    os.environ['DATABASE_FOLDER'] = os.path.expanduser("~")+'/db'

if not 'S3_BUCKET' in os.environ:
    os.environ['S3_BUCKET'] = 's3://shareddata'

if not 'LOG_STREAMNAME' in os.environ:
    os.environ['LOG_STREAMNAME'] = 'shareddata-logs'

if not 'USER_COMPUTER' in os.environ:
    os.environ['USER_COMPUTER'] = os.environ['USERNAME'] + \
        '@'+os.environ['COMPUTERNAME']

if not 'LOG_LEVEL' in os.environ:
    os.environ['LOG_LEVEL'] = 'INFO'

if not 'SAVE_LOCAL' in os.environ:
    os.environ['SAVE_LOCAL'] = 'True'

if not 'GIT_PROTOCOL' in os.environ:
    os.environ['GIT_PROTOCOL'] = 'https'

if not 'GIT_SERVER' in os.environ:
    os.environ['GIT_SERVER'] = 'github.com'

if not 'SOURCE_FOLDER' in os.environ:
    os.environ['SOURCE_FOLDER'] = os.environ['USERPROFILE']+'/src/'

if not 'SLEEP_TIME' in os.environ:
    os.environ['SLEEP_TIME'] = '2'

if not 'WORKERPOOL_STREAM' in os.environ:
    os.environ['WORKERPOOL_STREAM'] = 'shareddata-workerpool'


loaded = True
