# db_credentials.py contains all source and target database strings and credentials

# Import needed libraries
from libraries import *
# Import datawarehouse_name variable from variables.py
from variables import datawarehouse_name

# Oracle (source db)
oracle_db_config = {
    'user': os.environ['ORCLUID'],
    'password': os.environ['ORCLPWD'],
    'host': '143.34.194.228',
    'port': '1521',
    'service_name': 'XE'
}

# Other source db can continue here

# MariaDB (target db, datawarehouse)
datawarehouse_db_config = {
    'user': os.environ['MDBUID'],
    'password': os.environ['MDBPWD'],
    'host': '98.246.34.198',
    'port': '3306',
    'database': '{}'.format(datawarehouse_name)
}

# Other target db can continue here