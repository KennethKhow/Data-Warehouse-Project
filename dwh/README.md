## Project
Datawarehouse


## Table Of Contents

* [Introduction](#introduction)
* [Requirements](#requirements)
* [Installation](#installation)
* [Configuration](#configuration)
* [Environment Variables](#environment-variables)
* [Change Docker Virtual Disk Path](#change-docker-virtual-disk-path) (*Optional*)
* [Deployment](#deployment)
* [Usage](#usage)
* [Troubleshooting](#troubleshooting)
* [Optimizations](#optimizations)
* [Documentation](#documentation)
* [References](#references)


## [Introduction](#introduction)

What is a data warehouse?

![Data Warehouse Architecture]()

A data warehouse is a special type of data management system specifically designed to support business intelligence like data forecasting, data analysis, data mining, etc. A data warehouse must fulfill four unique characteristics:

1. Subject-oriented
2. Integrated
3. Nonvolatile
4. Time-variant

The operating system I used to develop and test this project is Windows 10 Pro. I do want to clarify that this project is a somewhat simpler version of my actual data warehouse project with KK Supermart & Superstore Sdn Bhd during my internship period. This is due to confidentiality issues. In this project, a data warehouse that facilitates sales analysis was designed with a snowflake schema. Both conceptual and logical ERD diagrams of the data warehouse are listed below:

* Conceptual ERD diagram: `dwh(conceptual).png`
* Logical ERD diagram: `dwh(logical).png`

Data extract from a source database, and the data need to load into a target data warehouse after data transformation. This can be achieved by a unique type of API called ETL (ETL stands for Extract, Transform, Load) data pipeline. The source database and the target database are listed below:

* Source database: Oracle 11g Express Edition
* Target data warehouse: MariaDB Server 10.6.7

ETL data pipelines were written in Python scripts and all Python dependencies were listed in `requirements.txt`. All Python scripts utilize Prefect Core Engine (Prefect library) to schedule and run tasks as flows. The ETL data pipeline can be deployed with various options:

1. Deployed locally on a host machine
2. Deployed locally on a host machine with Prefect Cloud
3. Deployed in a Docker container
4. Deployed in a Docker container with Prefect Cloud


## [Requirements](#requirements)

:bookmark_tabs: Prerequisites:

To make this project more interesting, we can use two machines to demonstrate this project. One of the machines, calls it computer A is used to install Oracle and MariaDB Server databases. Computer A will act as a remote server. Another machine, calls it computer B will act as a local machine. Oracle Instant Client, SQL Developer, and HeidiSQL need to install on computer B. Oracle Instant Client provides basic requirements for a user to interact with remote Oracle database on computer A. Both SQLDeveloper and HeidiSQL are GUI tools to query Oracle and MariaDB Server databases respectively. I will install Oracle 11g Express Edition instead of Oracle Instant Client on Computer B for easy and quick installation and setup to demonstrate this project. Then, we connect SQLDeveloper to the remote Oracle database in computer A.
 
Alternatively, we can also install Oracle and MariaDB Server databases on a single local machine to demonstrate this project.

**Run with a single local machine**

![Run with a single local machine]()

* Oracle 11g Express Edition as a local database, Oracle Instant Client and SQLDeveloper
* MariaDB Server 10.6.7[^1] as a local database
* Deployed locally on a host machine: Python 3.10.4
* Deployed locally on a host machine with Prefect Cloud: Python 3.10.4 and Docker Desktop
* Deployed in a Docker container: Docker Desktop
* Deployed in a Docker container with Prefect Cloud: Docker Desktop

**Run with two machines**

![Run with two machines]()

Computer A (*Remote Server*)
* Oracle 11g Express Edition as a remote database
* MariaDB Server 10.6.7 as a remote database

Computer B (*Local Machine*)
* Deployed locally on a host machine: Oracle Instant Client, SQL Developer, HeidiSQL and Python 3.10.4
* Deployed locally on a host machine with Prefect Cloud: Oracle Instant Client, SQL Developer, HeidiSQL, Python 3.10.4 and Docker Desktop
* Deployed in a Docker container[^2]: Oracle Instant Client, SQL Developer, HeidiSQL, Docker Desktop
* Deployed in a Docker container with Prefect Cloud[^2]: Oracle Instant Client, SQL Developer, HeidiSQL, Docker Desktop

[^1]: When you install MariaDB Server 10.6.7, HeidiSQL GUI tool is automatically installed. You do not need to install HeidiSQL separately.
[^2]: Oracle Instant Client, SQL Developer and HeidiSQL are not even needed with these two deployment methods. The ETL data pipeline still can execute smoothly in the Docker container. Oracle Instant Client, SQL Developer and HeidiSQL merely serve as tools to check the result.


## [Installation](#installation)

**Install Oracle 11g Express Edition**:
* Follow this [link](https://www.oicbasics.com/2020/01/download-oracle-database-11g-xe-express.html) to install Oracle 11g Express Edition step by step.

**Install MariaDB Server MariaDB Server 10.6.7**: 
* Use this [link](https://mariadb.org/download/?t=mariadb&p=mariadb&r=10.6.8&os=windows&cpu=x86_64&pkg=msi&m=nus) to install MariaDB Server 10.6.7[^3].
* Remember to add MariaDB Server into the PATH system variable.
* In this project, I will use the default `root` user with password `1234`.

**Install Oracle Instant Client**:
* Use this [link](https://www.oracle.com/database/technologies/instant-client/downloads.html) to install Oracle Instant Client.

**Install SQL Developer**:
* Use this [link](https://www.oracle.com/tools/downloads/sqldev-downloads.html) to install SQL Developer[^4].

**Install HeidiSQL**:
* Use this [link](https://www.heidisql.com/download.php) to install HeidiSQL[^5].

**Install Python 3.10.4**:
* Use this [link](https://www.python.org/downloads/release/python-3104/) to install Python 3.10.4.
* Remember to add Python into the PATH system variable.

**Install Docker Desktop**:
* Use this [link](https://docs.docker.com/get-docker/) to install Docker Desktop.
* Remember to add Docker Desktop into the PATH system variable.
* You may run into the issue with WSL 2. If you do, please make sure to follow the instruction given by the error message to fix the error.  

[^3]: MariaDB Server 10.6.7 has already been deprecated. You can install MariaDB Server 10.6.8. 
[^4]: You need to sign in to your Oracle account to download SQL Developer.
[^5]: You may need to turn off your antivirus software when extracting the zipped file of the HeidiSQL installer.


## [Configuration](#configuration)

**Connect SQL Developer to the local or remote Oracle database**

The local/remote Oracle database is in a machine with an IP address of `143.34.194.228`. The Oracle database connects to port `1521`. The service name of the Oracle database is `XE`. You can check all these details in `tnsnames.ora` file in the `ORACLE_HOME\network\admin` directory. We have to connect to the Oracle database as the `OT` user with a password of `1234`.

1. Open CMD as administrator and log in as sys user:

```shell
sqlplus / as sysdba
```

2. Use CREATE USER statement to create a user with OT as the username and 1234 as the password:

```shell
CREATE USER OT IDENTIFIED BY 1234;
```

3. Grant privileges to the OT user:

```shell
GRANT CONNECT, RESOURCE, DBA TO OT;
```

4. Close CMD and open SQL Developer.
5. Click the plus icon to add a new connection in SQL Developer.
6. Use Test as the connection name.
7. Fill in all connection details.

Connection details:
* Username: `OT`
* Password: `1234`
* Hostname: `143.34.194.228`
* Port: `1521`
* Service_name: `XE`

8. Click Test button to check the status of the connection. Finally, click Connect[^6] button to connect the local/remote Oracle database.

[^6]: For a remote database, temporarily disable the firewall on Computer A because Window Defender will block all TCP connections by default.

**Connect HeidiSQL to the local or remote MariaDB Server database**

The local/remote MariaDB Server database is in a machine with an IP address of `98.246.34.198`. The MariaDB Server database connects to port `3306`. We have to connect to the MariaDB Server database as the `root` user with a password of `1234`.

1. Open HeidiSQL and click the New button to add a new connection in HeidiSQL. 
2. Change the session name to Test.
3. Fill in all connection details.

Connection details:
* Host: `98.246.34.198`
* Port: `3306` (MariaDB Server default port)
* User: `root` (MariaDB Server default user with all privileges)
* Password: `1234`

4. Click the Open button to connect to the MariaDB Server database. 

You need to obtain the IP address of the machine that has Oracle and MariaDB Server installed. You can run this command in CMD as administrator to check for the IP address:

```shell
ipconfig
```

I will use 1234 as the password for this project but you can set up your own password.


## [Environment Variables](#environment-variables)

To run this project locally, you will need to add the following environment variables to your system variables

Oracle User ID and Password:

`ORCLUID = OT` `ORCLPWD = 1234`

MariaDB Server User ID and Password:

`MDBUID = root` `MDBPWD = 1234`


## [Change Docker Virtual Disk Path](#change-docker-virtual-disk-path)

This section is *optional*.

**Solution on how to change the file path of Docker virtual disk with WSL2 on Window 10**

Open CMD as administrator and run the following commands:

1. 
```shell
wsl --list -v
```
2. 
```shell 
wsl --shutdown
```
3. Do change the file_path to your desired file path: 
```shell
mkdir file_path\Docker\wsl\data
```
4. 
```shell
wsl --export docker-desktop-data "file_path\Docker\wsl\data\docker-desktop-data.tar"
```
5. 
```shell 
wsl --unregister docker-desktop-data
```
6. 
```shell 
wsl --import docker-desktop-data "file_path\Docker\wsl\data"
```
7. 
```shell
"file_path\Docker\wsl\data\docker-desktop-data.tar" --version 2
```
8. 
```shell 
del file_path\Docker\wsl\data\docker-desktop-data.tar
```

For a detailed explanation, please refer [here](https://blog.codetitans.pl/post/howto-docker-over-wsl2-location/).


## [Deployment](#deployment)

It is time to make our hands dirty. We will model a real-life data warehouse and ETL data pipelines as close as possible in this project :slightly_smiling_face:.

1. Make a directory called `project`.
2. Clone my GitHub repository into your `project` directory.
3. Create a sample database with the `OT` user by running `OT_schema.sql` in SQL Developer.
4. Create a sample data warehouse with the `root` user by running `dwh.sql` in HeidiSQL.

**Deployed locally on a host machine**

![Deployed locally on a host machine]()

5. Open CMD as administrator with `file_path\project\dwh\local\etl` as the directory and run the following command to create a virtual environment:

```shell
python -m venv venv
```

6. Activate the virtual environment:

```shell
venv\Scripts\activate
```

7. Install all Python dependencies:

```shell
python -m pip install --no-cache-dir -r requirements.txt
```

8. Run etl.py 

```shell
python etl.py
```

9. You will get prompted by the program with different options for running ETL data pipelines like this:

```shell
(venv) file_path\dwh\local\etl>python etl.py

ETL Option:
 department
 outlet
 product
 sales
 type register to register in Prefect Cloud

Please key in your option or type exit to quit:
```

You can select `department`/`product` first. Next, `outlet`. Lastly, `sales`.   
10. After you have done everything, you can deactivate the Python virtual environment by running the following command:

```shell
deactivate
```

**Deployed locally on a host machine with Prefect Cloud**

![Deployed locally on a host machine with Prefect Cloud]()

:heavy_exclamation_mark: The Prefect server requires Docker and Docker Compose to be running.

You also need a Prefect Cloud account to use this deployment. You can create a Prefect Cloud account [here](https://universal.prefect.io/). After you have successfully created a Prefect Cloud account, do create an API key in account settings for authentication purposes. Copy and paste the API key name and the API key into `prefect_cloud.txt`.

5. Open CMD as administrator with `file_path\project\dwh\local\etl` as the directory and run the following command to create a virtual environment:

```shell
python -m venv venv
```

6. Activate the virtual environment:

```shell
venv\Scripts\activate
```

7. Install all Python dependencies:

```shell
python -m pip install --no-cache-dir -r requirements.txt
```

8. Configure Prefect to use the Prefect Cloud backend by running the following command:

```shell
prefect backend cloud
```

9. Authenticate with an API key:

```shell
prefect auth login --key <API Key>
```

10. Create a Prefect project:

```shell
prefect create project "test"
```

I will create a project named test. If you already have a project in the Prefect Cloud, do skip this step.
11. Start a Prefect local agent:

```shell
prefect agent local start
```

12. Open a new CMD as administrator with `file_path\project\dwh\local\etl` as the directory without closing the previous CMD window and activate the virtual environment again with the command in step 6.
13. If you want to register for another project, you need to change the project name.

```python
flow.register(project_name = "your project name")
```

14. Run etl.py 

```shell
python etl.py
```

15. You can select `register` to register all ETL data pipelines in Prefect Cloud.
16. Log into your Prefect Cloud account and use the Prefect Cloud UI to quick run ETL Python scripts in the following order:

`etl_departments`/`etl_products` `etl_outlets` `etl_sales`

You can check all registered ETL Python scripts in the Flow tab in your Dashboard.
17. After you have done everything, you can stop the Prefect local agent by using Ctrl + c in the CMD and deactivate the Python virtual environment by running the following command:

```shell
deactivate
```

**Deployed in a Docker container**

![Deployed in a Docker container]()

5. Open CMD as administrator with `file_path\project\dwh\docker\etl` as the directory and run the following command to build, create and start a container:

```shell
docker-compose up -d
```

6. Check the `CONTAINER ID`:

```shell
docker ps
```

7. Copy the `CONTAINER ID` and paste it into the following command:

```shell
docker exec -it <CONTAINER ID> bash
```

This is to execute the container in an interactive mode (`-it`) with the Bash shell.
8. Execute `.profile` in the home directory and activate the Python virtual environment:

```shell
source ~/.profile && source /app/venv/bin/activate
```

9. Run etl.py 

```shell
python etl.py
```

10. You will get prompted by the program with different options for running ETL data pipelines like this:

```shell
(venv) file_path\dwh\local\etl>python etl.py

ETL Option:
 department
 outlet
 product
 sales
 type register to register in Prefect Cloud

Please key in your option or type exit to quit:
```

You can select `department`/`product` first. Next, `outlet`. Lastly, `sales`.
11. After you have done everything, you can deactivate the Python virtual environment by running the following command:

```shell
deactivate
```

12. Exit the Bash shell of the container:

```shell
exit
```

13. Stop and remove the container:

```shell
docker-compose down
```


**Deployed in a Docker container with Prefect Cloud**

![Deployed in a Docker container with Prefect Cloud]()

You need a Prefect Cloud account to use this deployment. You can create a Prefect Cloud account [here](https://universal.prefect.io/). After you have successfully created a Prefect Cloud account, do create an API key in account settings for authentication purposes. Copy and paste the API key name and the API key into `prefect_cloud.txt`.

5. Open CMD as administrator with `file_path\project\dwh\docker\etl` as the directory and run the following command to build, create and start a container:

```shell
docker-compose up -d
```

6. Check the `CONTAINER ID`:

```shell
docker ps
```

7. Copy the `CONTAINER ID` and paste it into the following command:

```shell
docker exec -it <CONTAINER ID> bash
```

This is to execute the container in an interactive mode (`-it`) with the Bash shell.

8. Execute `.profile` in the home directory and activate the Python virtual environment:

```shell
source ~/.profile && source /app/venv/bin/activate
```

9. Configure Prefect to use the Prefect Cloud backend by running the following command:

```shell
prefect backend cloud
```

10. Authenticate with an API key:

```shell
prefect auth login --key <API Key>
```

11. Create a Prefect project:

```shell
prefect create project "test"
```

I will create a project named test. If you already have a project in the Prefect Cloud, do skip this step.
12. Start a Prefect local agent:

```shell
prefect agent local start
```

13. Open a new CMD as administrator with `file_path\project\dwh\docker\etl` as the directory without closing the previous CMD window and go through steps 6 to 9 again.
14. If you want to register for another project, you need to change the project name.

```python
flow.register(project_name = "your project name")
```

15. Run etl.py 

```shell
python etl.py
```

16. You can select `register` to register all ETL data pipelines in Prefect Cloud.
17. Log into your Prefect Cloud account and use the Prefect Cloud UI to quick run ETL Python scripts in the following order:

`etl_departments`/`etl_products` `etl_outlets` `etl_sales`

You can check all registered ETL Python scripts in the Flow tab in your Dashboard.
18. After you have done everything, you can stop the Prefect local agent by using Ctrl + c in the Bash shell and deactivate the Python virtual environment by running the following command:

```shell
deactivate
```

19. Exit the Bash shell of the container:

```shell
exit
```

20. Stop and remove the container:

```shell
docker-compose down
```


## [Usage](#usage)

The directory of `dwh` is listed below:

```shell
dwh            
├───docker     # docker directory includes etl directory for ETL data pipelines, Dockerfile, docker-compose.yml, install.sh, and requirements.txt. 
│   └───etl
├───ERD        # ERD directory includes conceptual and logical entity relationship diagrams for OT_schema.sql and dwh.sql.     
├───image      # image directory stores all images required by the README.md file.
├───local      # local directory includes etl directory for ETL data pipelines and requirements.txt.
│   └───etl
└───sql        # sql directory contains OT_schema.sql to create a mock database and dwh.sql to create a mock data warehouse.
```

`docker` directory is for the deployment of ETL data pipelines in a Docker container. This directory includes a `Dockerfile` to build a custom slim Python version 3.10.4 image with Oracle Instant Client version 19.8 and all Python dependencies installed. `install.sh` installs Oracle Instant Client version 19.8 and configures Oracle Instant Client's system PATH variables in Linux. `requirements.txt` stores all Python dependencies. `docker-compose.yml` is to build the image from the `Dockerfile`, create, and run a Docker container.

`local` directory is for the deployment of ETL data pipelines in a local machine that has Python installed. `requirements.txt` stores all Python dependencies to pip install required Python libraries. To install needed Python libraries for this project, you can just run the following command:

```shell
pip install --no-cache-dir -r requirements.txt
```

Make sure to run this command in the `file_path\project\dwh\local\etl` directory.

`etl` directory in `docker` directory and `local` directory has same Python files (`*.py`). In `etl` directory, the purpose of each Python module is listed below:

1. `libraries.py`: Imports all required libraries.
2. `variables.py`: Stores all data warehouse names in target databases.
3. `sql_queries.py`: Stores extract SQL queries in a list to query source databases and target table names in target databases.
4. `flow.py`: Defines schedules with specific time zones for Prefect Scheduler and task dependencies for Prefect Flow
5. `db_credentials.py`: Stores all source and target databases credential information.
6. `etl.py`: Includes extract(), transform(), and load() functions to carry out ETL processes.

Python libraries used:

* `datetime`: To parse date and time information
* `os`: To use environment variables
* `pandas`: To use dataframe for better data analytics, manipulation, and visualization
* `prefect`: To automate ETL data pipelines with a specific schedule
* `pytz`: To use a specific time zone
* `rich`: To give the colorful text in the terminal
* `sqlalchemy`: To establish connections with source databases and target databases
* `timeit`: To check the execution time of ETL data pipelines

For further references, please refer [here](https://pypi.org/). 

**How it works?**

All defined functions are individual Prefect tasks.

```python
@prefect.task
def extract(query):
    :

@prefect.task
def transform(df):
    :

@prefect.task()
def load(load_table, df):
    :
```

When running `etl.py`, Prefect tasks will be executed by following a specific Prefect flow in `flow.py`. The first task is to extract data from a source database and store data into a pandas dataframe with the `extract()` function in `extract.py`.

**Extract function**:

```python
def extract(query):
    try:
        src_conn_str = "oracle://{uid}:{pwd}@{host}:{port}/?service_name={sid}"
        src_engine = sqlalchemy.create_engine(src_conn_str.format(uid = oracle_db_config['user'], pwd = oracle_db_config['password'], host = oracle_db_config['host'], port = oracle_db_config['port'], sid = oracle_db_config['service_name']), max_identifier_length = 128)
        df = pd.read_sql(query, src_engine)
        return df 
    except SQLAlchemyError as error:
        # Signal error
        raise signals.FAIL(message = "Data extract error. Error code: {}".format(error))
```

`src_conn_str` is the connection string for a source database. The `extract()` function uses SQLAlchemy `create_engine()` function to establish a connection with a source database. Data from the source database is stored as a local variable in the form of a pandas dataframe with the `read_sql()` function.

Then, the next task is to transform data stored in the pandas dataframe passed from the `extract()` function with a `transform()` function in `etl.py`.

**Transform function**:

```python
def transform(choice, df):
    try:
        if choice == "department":
            df.drop_duplicates('dept_no')
            departments_df = pd.DataFrame(df)
            return departments_df
        
        elif choice == "outlet":
            df.drop_duplicates('outlet_no')
            outlets_df = pd.DataFrame(df)
            return outlets_df
            :
    except SQLAlchemyError as error:
        # Signal error
        raise signals.FAIL(message = "Data transform error. Error code: {}".format(error))
```

This `transform()` function utilizes pandas `drop_duplicates()` function to drop all duplicate values.

Finally, the transformed data in the pandas dataframe is passed to the `load()` function in `etl.py` to load the transformed data into a target data warehouse.   

**Load function**: 

```python
def load(load_table, df):
    try:
        @compiles(Insert)
        def prefix_insert_with_ignore(insert, compiler, **kwargs):
            return compiler.visit_insert(insert.prefix_with("IGNORE"), **kwargs)  
        tg_conn_str = "mariadb+mariadbconnector://{uid}:{pwd}@{host}:{port}/{db}"
        tg_engine = sqlalchemy.create_engine(tg_conn_str.format(uid = datawarehouse_db_config['user'], pwd = datawarehouse_db_config['password'], host = datawarehouse_db_config['host'], port = datawarehouse_db_config['port'], db = datawarehouse_db_config['database']))
        return df.to_sql(load_table, tg_engine, if_exists = 'append', index = False, chunksize = 5000, method = 'multi')
    except SQLAlchemyError as error:
        # Signal error
        raise signals.FAIL(message = "Data load error. Error code: {}".format(error))
```

`tg_conn_str` is the connection string for a target database. The `load()` function also uses SQLAlchemy `create_engine()` function to establish a connection with a target database. Data is loaded into a target database with the `to_sql()` function in the pandas library.

```python
@compiles(Insert)
def prefix_insert_with_ignore(insert, compiler, **kwargs):
    return compiler.visit_insert(insert.prefix_with("IGNORE"), **kwargs)
```

This block of code in the `load()` function has a similar function to the MariaDB Server supported `INSERT IGNORE` statement.

**Prefect flow**:

In `flow.py`, the `prefect_flow()` function will defined all task dependencies and triggers.

```python
def prefect_flow(choice):
    # outlet etl
    if choice == "department":   
        with prefect.Flow("etl_departments") as flow:
            # Task dependencies
            data = extract(oracle_extract[0])
            result = transform(choice, data)
            load_data = load("departments_dim", result)
            
            # Triggers
            result.set_upstream(data)
            load_data.set_upstream(result)
        return flow
    :
```

This flow tells us
1. First task: Extract data from a source database with the `extract()` function
2. Second task: Transform data from the extracted data with the `transform()` function
3. Third task: Load data to a target database from the transformed data with the `load()` function

**Prefect Scheduler**:

Besides defining Prefect Flow in `flow.py`, all schedule information is stored in this Python module.

```python
# Define timezones and datetime variables
kl_tz = pytz.timezone("Asia/Kuala_Lumpur")
dt = datetime.datetime(2022, 5, 23, 9, 30, 0)

# Prefect Scheduler to automate ETL data pipelines
schedule = Schedule(clocks = [IntervalClock(start_date = kl_tz.localize(dt, is_dst = True), interval = datetime.timedelta(minutes = 30))])
```

We use the `pytz` Python library to assign the time zone of Kuala Lumpur, Malaysia to the `kl_tz` variable. We also use the `datetime` Python library here to parse the start date and the start time to the `dt` variable. Finally, the `schedule` variable stores relevant information with the Prefect Scheduler like when to start a Prefect flowand the interval for each execution of the Prefect flow. In this example, the interval for each execution of a Prefect flow is set to 30 minutes.

You can add `schedule = schedule` in the `prefect.Flow()` function to automate the ETL data pipeline with a specific schedule.

```python
def prefect_flow():
    with prefect.Flow("etl_products", schedule = schedule) as flow:
        :
    return flow
```


## [Troubleshooting](#troubleshooting)

All Python codes had been refactored into various Python modules for the ease of troubleshooting. All Python codes are embedded with the Prefect library to manage tasks, dependencies, flows, and schedules. With Prefect, we can easily identify which stage fails during the execution of the ETL data pipeline by checking the status of each task. For instance, let us run `etl_departments` by selecting `department`:

```shell
(venv) file_path\project\dwh\local\etl>etl.py

ETL Option:
 department
 outlet
 product
 sales
 type register to register in Prefect Cloud

Please key in your option or type exit to quit: department
[2022-06-23 14:29:00+0800] INFO - prefect.FlowRunner | Beginning Flow run for 'etl_departments'
[2022-06-23 14:29:00+0800] INFO - prefect.TaskRunner | Task 'extract': Starting task run...
[2022-06-23 14:29:08+0800] INFO - prefect.TaskRunner | Task 'extract': Finished task run for task with final state: 'Success'
[2022-06-23 14:29:08+0800] INFO - prefect.TaskRunner | Task 'transform': Starting task run...
[2022-06-23 14:29:08+0800] INFO - prefect.TaskRunner | Task 'transform': Finished task run for task with final state: 'Success'
[2022-06-23 14:29:08+0800] INFO - prefect.TaskRunner | Task 'load': Starting task run...
[2022-06-23 14:29:09+0800] INFO - prefect.TaskRunner | Task 'load': Finished task run for task with final state: 'Success'
[2022-06-23 14:29:09+0800] INFO - prefect.FlowRunner | Flow run SUCCESS: all reference tasks succeeded
Execution time: 8.403129099984653 s
```

From this example, the status of each task is Success. All tasks are executed successfully without any failure. I will use the same example again but change the source database port from `1521` to `1522` in `db_credentials.py`.

```shell
(venv) file_path\project\dwh\local\etl>etl.py

ETL Option:
 department
 outlet
 product
 sales
 type register to register in Prefect Cloud

Please key in your option or type exit to quit: department
[2022-06-23 14:31:24+0800] INFO - prefect.FlowRunner | Beginning Flow run for 'etl_departments'
[2022-06-23 14:31:24+0800] INFO - prefect.TaskRunner | Task 'extract': Starting task run...
[2022-06-23 14:31:30+0800] INFO - prefect.TaskRunner | FAIL signal raised: FAIL('Data extract error. Error code: (cx_Oracle.DatabaseError) ORA-12541: TNS:no listener\n(Background on this error at: https://sqlalche.me/e/14/4xp6)')
[2022-06-23 14:31:31+0800] INFO - prefect.TaskRunner | Task 'extract': Finished task run for task with final state: 'Failed'
[2022-06-23 14:31:31+0800] INFO - prefect.TaskRunner | Task 'transform': Starting task run...
[2022-06-23 14:31:31+0800] INFO - prefect.TaskRunner | Task 'transform': Finished task run for task with final state: 'TriggerFailed'
[2022-06-23 14:31:31+0800] INFO - prefect.TaskRunner | Task 'load': Starting task run...
[2022-06-23 14:31:31+0800] INFO - prefect.TaskRunner | Task 'load': Finished task run for task with final state: 'TriggerFailed'
[2022-06-23 14:31:31+0800] INFO - prefect.FlowRunner | Flow run FAILED: some reference tasks failed.
Execution time: 6.295316600007936 s
```

You can see from the output the first task failed, and other tasks failed as well. With a Prefect trigger, a task will fail when the prior task failed. A task always depends on its upstream task. A short log message is generated to tell why such a task failed. You can use the link in the log message to troubleshoot possible errors in the Python script. In this example, we only need to fix this error in `extract()` since only the first task has an error. The error occurs because the wrong port number is passed to the `extract()` function. If the error occurs in the third task, then we need to fix this error in `load()`. This method efficiently reduces the scope of troubleshooting.


## [Optimizations](#optimizations)

The execution time of all ETL data pipelines is optimized by finding the most optimal `chunksize` of the load function, `load()`.

```python
def load(load_table, df):
    try:
        :
        df.to_sql(load_table, tg_engine, if_exists = 'append', index = False, chunksize = 5000, method = 'multi')
    except SQLAlchemyError as error:
        raise signals.FAIL(message = "Data load error. Error code: {}".format(error))
```

Codes are also refactored into different Python modules to reduce duplicate codes. The 'multi' method is used in the `to_sql()` function to insert multiple values into the target database. By working with the actual ETL data pipeline, the chunksize is optimized with a value of `5000` to give the minimum execution time for extracting, transforming, and loading 315859 values from the Oracle database to the MariaDB Server database.

Results:

| chunksize | Execution Time 1 (s) | Execution Time 2 (s) | Execution Time 3 (s) | Average Execution Time (s) | Average Execution Time (min) |
| --------- | -------------------- | -------------------- | -------------------- | -------------------------- | -------------------- |
| 4500      | 167.527784000034     | 153.930623200023     | 218.361539100005     | 179.9399821                | 2.998999702            |
| 5000      | 175.540902699984     | 168.974699599959     | 183.514505499973     | 176.0100359                | 2.933500599            |
| 5500      | 264.790257699962     | 203.113148700038     | 236.148032099998     | 234.6838128                | 3.911396881            |
| 6000      | 206.675690300064     | 196.09619480010588   | 203.50375129992608   | 202.0918788                | 3.36819798             |
| 6500      | 223.414989700075     | 214.719917100039     | 189.8871252000099    | 209.3406773                | 3.489011289            |

We can simply optimize the ETL data pipelines by changing the `chunksize`.


## [Documentation](#documentation)

All documentation here is related to this project. For further references, please refer to

* [Docker Docs](https://docs.docker.com/)
* [MariaDB Server Docs](https://mariadb.com/kb/en/)
* [Oracle Docs](https://docs.oracle.com/en/database/oracle/oracle-database/)
* [Pandas Docs](https://pandas.pydata.org/docs/)
* [Prefect Docs](https://docs.prefect.io/)
* [Python Docs](https://www.python.org/doc/)
* [Rich Docs](https://rich.readthedocs.io/en/stable/)
* [SQLAlchemy Docs](https://docs.sqlalchemy.org/en/14/)


## [References](#references)

* [30 Days of Python - Day 17 - Data Science Pipeline with Jupyter, Pandas, & FastAPI - Python TUTORIAL](https://youtu.be/CApCQKuWqBM) by CodingEntrepreneurs on Youtube
* [Create an ETL pipeline in Python with Pandas in 10 minutes](https://towardsdev.com/create-an-etl-pipeline-in-python-with-pandas-in-10-minutes-6be436483ec9) by Nazia Habib on Towards Dev
* [Data Warehouse Concepts | Data Warehouse Tutorial | Data Warehouse Architecture | Edureka](https://youtu.be/CHYPF7jxlik) by edureka! on Youtube
* [Data Warehouse Tutorial](https://www.javatpoint.com/data-warehouse) on javaTpoint
* [ETL (Extract, Transform, and Load) Process in Data Warehouse](https://www.guru99.com/etl-extract-load-process.html) by David Taylor on Guru99
* [How can I change the location of docker images when using Docker Desktop on WSL2 with Windows 10 Home?](https://stackoverflow.com/questions/62441307/how-can-i-change-the-location-of-docker-images-when-using-docker-desktop-on-wsl2/63752264#63752264) by Franks Chow on StackOverflow
* [How to build ETL pipelines in Python](https://knowtechie.com/how-to-build-etl-pipelines-in-python/) by Chris Smith on KnowTechie
* [How to build an ETL pipeline with Python | Data pipeline | Export from SQL Server to PostgreSQL](https://youtu.be/dfouoh9QdUw) by BI Insights Inc on Youtube
* [HowTo: Change Docker containers storage location with WSL2 on Windows 10](https://blog.codetitans.pl/post/howto-docker-over-wsl2-location/) by Pawel Hofman on Coding with Titans
* [Oracle Tutorial](https://www.oracletutorial.com/) on ORACLETUTORIAL.COM
* [Prefect Tutorial | Indestrutible Python Code](https://youtu.be/0IcN117E4Xo) by Kevin Fortier on Youtube
* [Python: Pandas.to_sql INSERT IGNORE the correct way (sqlalchemy)](https://sick.codes/python-pandas-to_sql-insert-ignore-the-correct-way-sqlalchemy/) by Sick Codes on sick.codes
* [Top 15 Data Warehouse Tools & Software 2022](https://www.datamation.com/big-data/top-15-data-warehouse-tools/) by James Maguire on Datamation
* [Understand Slowly Changing Dimensions](https://youtu.be/Sg2AAk1vwEs) by Bryan Cafferky on Youtube
* [What Is a Data Warehouse?](https://youtu.be/AHR_7jFCMeY) by 365 Data Science on Youtube