# sql_queries.py contains all sql queries for different source db and targeted tables in target db

# Oracle queries (source db)
oracle_extract_1 = '''SELECT * FROM departments'''
oracle_extract_2 = '''SELECT * FROM outlets'''
oracle_extract_3 = '''SELECT * FROM permissions'''
oracle_extract_4 = '''SELECT * FROM products'''
oracle_extract_5 = '''SELECT * FROM outlet_sales'''
oracle_extract_6 = '''SELECT
                            os.sales_no,
                            o.outlet_no,
                            os.item, 
                            os.quantity_sold,
                            p.unit_price
                        FROM outlets o, outlet_sales os, products p
                        WHERE o.outlet_no = os.outlet
                        AND os.item = p.item_no'''

oracle_extract = [oracle_extract_1, oracle_extract_2, oracle_extract_3, oracle_extract_4, oracle_extract_5, oracle_extract_6]

# Other source db queries can continue here