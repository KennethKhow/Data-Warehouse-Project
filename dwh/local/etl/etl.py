# etl.py connects to databases and conduct needed queries to extract, transform, and load data from source db to target datawarehouse db

# Import needed libraries
from db_credentials import *
from flow import *
from libraries import *
from prefect.engine import signals
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert
from sqlalchemy.exc import SQLAlchemyError

# Task 1: Extract data
@prefect.task
def extract(query):
    try:
        src_conn_str = "oracle://{uid}:{pwd}@{host}:{port}/?service_name={sid}"
        src_engine = sqlalchemy.create_engine(src_conn_str.format(uid = oracle_db_config['user'], pwd = oracle_db_config['password'], host = oracle_db_config['host'], port = oracle_db_config['port'], sid = oracle_db_config['service_name']), max_identifier_length = 128)
        df = pd.read_sql(query, src_engine)
        return df 
    except SQLAlchemyError as error:
        raise signals.FAIL(message = "Data extract error. Error code: {}".format(error))

# Task 2: Transform data 
@prefect.task()          
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
        
        elif choice == "permission":
            df.drop_duplicates('role_no')
            permissions_df = pd.DataFrame(df)
            return permissions_df
        
        elif choice == "product":
            df.drop_duplicates('item_no')
            products_df = pd.DataFrame(df[['item_no', 'line_no', 'class_no', 'item_name', 'barcode']])
            return products_df
        
        elif choice == "time":
            df.drop_duplicates('sales_no')
            times_df = pd.DataFrame()
            times_df['sales_no'] = df['sales_no']
            times_df['day'] = pd.to_datetime(df['sales_date'], errors = 'coerce', format = "%Y-%m-%d", unit = 'D')
            times_df['week'] = times_df['day'].dt.isocalendar().week
            times_df['month'] = times_df['day'].dt.month_name().str[:3]
            times_df['quarter'] = times_df['day'].dt.to_period(freq = 'Q').dt.strftime("%y Q%q")
            times_df['year'] = times_df['day'].dt.year
            return times_df
        
        elif choice == "sales":
            df.rename(columns = {'item' : 'item_no'}, inplace = True)
            df.rename(columns = {'quantity_sold' : 'quantity'}, inplace = True)
            df['revenue'] = df['quantity'] * df['unit_price']
            sales_df = pd.DataFrame(df)
            return sales_df
        
    except SQLAlchemyError as error:
        raise signals.FAIL(message = "Data transform error. Error code: {}".format(error))

# Task 3: Load data
@prefect.task
def load(load_table, df):
    try:
        @compiles(Insert)
        def prefix_insert_with_ignore(insert, compiler, **kwargs):
            return compiler.visit_insert(insert.prefix_with("IGNORE"), **kwargs)  
        tg_conn_str = "mariadb+mariadbconnector://{uid}:{pwd}@{host}:{port}/{db}"
        tg_engine = sqlalchemy.create_engine(tg_conn_str.format(uid = datawarehouse_db_config['user'], pwd = datawarehouse_db_config['password'], host = datawarehouse_db_config['host'], port = datawarehouse_db_config['port'], db = datawarehouse_db_config['database']))
        return df.to_sql(load_table, tg_engine, if_exists = 'append', index = False, chunksize = 5000, method = 'multi')
    except SQLAlchemyError as error:
        raise signals.FAIL(message = "Data load error. Error code: {}".format(error))

# Choose specific task flow based on user's choice    
def user_choice(choice):
    # Register ETL data pipelines in Prefect Cloud
    if choice == "register":
        x = ["department", "outlet", "product", "sales"]
        
        for i in x:
            flow = prefect_flow(i)
            flow.register(project_name = "test")
    # Run ETL data pipelines with Prefect Core Engine
    else:
        starttime = timeit.default_timer()
        flow = prefect_flow(choice)
        flow.run()
        rich.print("[#606060]Execution time: {} s[/#606060]".format(timeit.default_timer() - starttime))

# Prompt user
def prompt_user():
    option = ["[#ffff00]department[/#ffff00]", "[#00cc00]outlet[/#00cc00]", "[#00ffff]product[/#00ffff]", "[#ff00ff]sales[/#ff00ff]", "type [#ff0000]register[/#ff0000] to register in Prefect Cloud"]
    print("\nETL Option:")
    for i in option:
        rich.print(" " + i)
    rich.print("\nPlease key in your option or type [#ff0000]exit[/#ff0000] to quit:", end = ' ')
    choice = input()
    
    if (choice == "department" or choice == "outlet" or choice == "product" or choice == "sales" or choice == "register"):
        user_choice(choice)
        prompt_user()

    elif choice == "exit":
        exit()
        
    else:
        print("[#ff0000]Invalid option![/#ff0000]")
        prompt_user()

# Run etl.py 
if __name__ == "__main__":
    prompt_user()
    