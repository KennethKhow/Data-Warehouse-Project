# flow.py contains datatime variables with timezone information for Prefect Scheduler and defines Prefect Flow

# Import needed libraries
from etl import extract, transform, load
from libraries import *
from prefect.schedules import Schedule
from prefect.schedules.clocks import IntervalClock
from sql_queries import oracle_extract

# Define timezones and datetime variables
kl_tz = pytz.timezone("Asia/Kuala_Lumpur")
dt = datetime.datetime(2022, 5, 23, 9, 30, 0)

# Prefect Scheduler to automate ETL data pipelines
schedule = Schedule(clocks = [IntervalClock(start_date = kl_tz.localize(dt, is_dst = True), interval = datetime.timedelta(minutes = 30))])

# Define Prefect Flow       
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
    
    elif choice == "outlet":   
        with prefect.Flow("etl_outlets") as flow:
            # Task dependencies
            data_1 = extract(oracle_extract[1])
            result_1 = transform(choice, data_1)
            load_data_1 = load("outlets_dim", result_1)
            
            data_2 = extract(oracle_extract[2])
            result_2 = transform("permission", data_2)
            load_data_2 = load("permissions_dim", result_2)
            
            # Triggers
            result_1.set_upstream(data_1)
            load_data_1.set_upstream(result_1)
            
            result_2.set_upstream(data_2)
            load_data_2.set_upstream(result_2)
            load_data_2.set_upstream(load_data_1)
        return flow
    
    elif choice == "product":   
        with prefect.Flow("etl_products") as flow:
            # Task dependencies
            data = extract(oracle_extract[3])
            result = transform(choice, data)
            load_data = load("products_dim", result)
            
            # Triggers
            result.set_upstream(data)
            load_data.set_upstream(result)
        return flow
    
    elif choice == "sales":   
        with prefect.Flow("etl_sales") as flow:
            # Task dependencies
            data_1 = extract(oracle_extract[4])
            result_1 = transform("time", data_1)
            load_data_1 = load("times_dim", result_1)
            
            data_2 = extract(oracle_extract[5])
            result_2 = transform(choice, data_2)
            load_data_2 = load("sales_fact", result_2)
            
            # Triggers
            result_1.set_upstream(data_1)
            load_data_1.set_upstream(result_1)
            
            result_2.set_upstream(data_2)
            load_data_2.set_upstream(result_2)
            load_data_2.set_upstream(load_data_1)
        return flow
        