#Program Name: Library Database System
#Description: This program will allow for the creation/updating of a library database.
#             It will operate using the Python terminal, psycopg2 Python library, and PostgresSQL

import psycopg2

#Lists with data inputs depending on which set of information is selected
locations_list = ["location_name","hours","store_address"]
staff_list = ["staff_first_name","staff_last_name","store_id", "role","hourly_wage"]
inventory_list = ["book_name","book_author","book_author", "customer_id","store_id", "replacement_cost"]
customers_list = ["customer_first_name","customer_last_name","store_id","customer_address"]
table_names = ["locations", "staff", "inventory", "customers"]
id_header_list = ["store_id", "staff_id", "book_id", "customer_id"]


output_array = []
category_list = []

#General lists with each lists as a value
data_list = [locations_list,staff_list, inventory_list, customers_list]

#Individual functions for each type of action
value_list = []
def add_option(data):
    repeat = True
    while repeat:
        output_array = info_input(data_list[data])        
        if data == 0:
            add_query = f"""
            INSERT INTO locations (location_name, hours, store_address)
            VALUES ('{output_array[0]}','{output_array[1]}','{output_array[2]}')
            """
        elif data == 1:
            add_query = f"""
            INSERT INTO staff(staff_first_name, staff_last_name, store_id, role, hourly_wage)
            VALUES ('{output_array[0]}','{output_array[1]}','{output_array[2]}','{output_array[3]}','{output_array[4]}')
            """
        elif data == 2:
            add_query = f"""
            INSERT INTO inventory(book_name,book_author, customer_id,store_id, replacement_cost)
            VALUES ('{output_array[0]}','{output_array[1]}','{output_array[2]}','{output_array[3]}','{output_array[4]}', '{output_array[5]}')
            """
        elif data == 3:
            add_query = f"""
            INSERT INTO customers(customer_first_name,customer_last_name,store_id,customer_address)
            VALUES ('{output_array[0]}','{output_array[1]}','{output_array[2]}','{output_array[3]}')
            """
        
        cur.execute(add_query)
        repeat_response = input("Would you like to add another entry? Enter Y/N:\t")
        if repeat_response == 'Y':
            repeat = True
        else:
            repeat = False


def delete_option(data):
    repeat = True
    while repeat:
        for i in (data_list[data]):
            print(i, "\n")
        categories = int(input("How many categories will you be entering to filter your delete command?:\t"))           
        for i in range (categories):
            category_list.append(input("Enter the category name:\t"))
            value_list.append(input("Enter the value from the coloumn that you would like to specify:\t"))
            
        additional_string = f"{category_list[0]} = '{value_list[0]}'"

        for i in range (categories):
            if (i!=0):
                additional_string += " AND " + f"{category_list[i]} = '{value_list[i]}'"

        delete_query = f"""
            DELETE FROM {table_names[data]}
            WHERE {additional_string}          
        """

        cur.execute(delete_query)
        print('Action completed.')

        repeat_response = input("Would you like to add another entry? Enter Y/N:\t")
        if repeat_response == 'Y':
            repeat = True
        else:
            repeat = False

def search_option(data):
    repeat = True
    while repeat:
        for i in (data_list[data]):
            print(i, "\n")
        categories = int(input("How many categories do you want to include in your search criteria?:\t"))           
        for i in range (categories):
            category_list.append(input("Enter the category name:\t"))
            value_list.append(input("Enter the value from the coloumn that you would like to specify:\t"))
                
        additional_string = f"{category_list[0]} = '{value_list[0]}'"

        for i in range (categories):
            if (i!=0):
                additional_string += " AND " + f"{category_list[i]} = '{value_list[i]}'"

        lim = int(input("How many rows do you want to output?:\t"))

        search_query = f"""
            SELECT * FROM {table_names[data]}
            WHERE {additional_string}
            LIMIT {lim}
        """

        cur.execute(search_query)
        query_result = cur.fetchall()
        for entry in query_result:
            print(entry,"\n")

        repeat_response = input("Would you like to add another entry? Enter Y/N:\t")
        if repeat_response == 'Y':
            repeat = True
        else:
            repeat = False

def update_option(data):
    print('UPDATE Option Selected')
    repeat = True
    while repeat:
        for i in (data_list[data]):
            print(i, "\n")
        categories = int(input("How many categories do you want to include in your search criteria?:\t"))           
        for i in range (categories):
            category_list.append(input("Enter the category name:\t"))
            value_list.append(input("Enter the value from the coloumn that you would like to specify:\t"))
                
        additional_string = f"{category_list[0]} = '{value_list[0]}'"

        for i in range (categories):
            if (i!=0):
                additional_string += " AND " + f"{category_list[i]} = '{value_list[i]}'"

        search_query = f"""
            SELECT * FROM {table_names[data]}
            WHERE {additional_string}
        """

        cur.execute(search_query)
        query_result = cur.fetchall()
        for entry in query_result:
            print(entry,"\n")
        
        unique_id = int(input("Choose which unique ID you want to update the information for:\t"))

        update_array = info_input(data_list[data])

        additional_string = f"{data_list[data][0]} = '{update_array[0]}'"

        for i in range(len(data_list[data])):
            if (i!=0):
                additional_string += ", " + f"{data_list[data][i]} = '{update_array[i]}" 

        update_query = f"""
            UPDATE {table_names[data]}
            SET {additional_string}
            WHERE {id_header_list[data]} = {unique_id}
        """

        cur.execute(update_query)
        print('Action completed.')

        repeat_response = input("Would you like to add another entry? Enter Y/N:\t")
        if repeat_response == 'Y':
            repeat = True
        else:
            repeat = False

def info_input(input_list):
    output_array = []
    for inp in input_list:
        dat = ''
        dat = input(f'Enter data for {inp}:')
        output_array.append(dat)    
    
    return output_array


#Password should be whatever the postgres password was set to.
pw = 'sAmsung.1'

#Connecting to premade 'Library' database (ONLY PREREQ) and creating cursor (for query execution)
conn = psycopg2.connect(
    database = 'Library',
    user = 'postgres',
    password = pw
)
cur = conn.cursor()

#Creating tables (if not already created)
create_table_locations = """
    CREATE TABLE IF NOT EXISTS locations(
    store_id SERIAL PRIMARY KEY,
    location_name VARCHAR(250),
    hours VARCHAR(50),
    store_address VARCHAR(250)
);
"""
cur.execute(create_table_locations)

create_table_staff = """
    CREATE TABLE IF NOT EXISTS staff(
    staff_id SERIAL PRIMARY KEY,
    staff_first_name VARCHAR(100),
    staff_last_name VARCHAR(100),
    store_id INT REFERENCES locations(store_id),
    role VARCHAR(250)   ,
    hourly_wage FLOAT(2)
);
"""

cur.execute(create_table_staff)

create_table_inventory = """
    CREATE TABLE IF NOT EXISTS inventory(
    book_id SERIAL PRIMARY KEY,
    book_name VARCHAR(250),
    book_author VARCHAR(250),
    customer_id INT REFERENCES customers(customer_id),
    store_id INT REFERENCES locations(store_id),
    replacement_cost FLOAT(2)
);
"""
cur.execute(create_table_inventory)

create_table_customers = """
    CREATE TABLE IF NOT EXISTS customers(
    customer_id SERIAL PRIMARY KEY,
    customer_first_name VARCHAR(100),
    customer_last_name VARCHAR(100),
    store_id INT REFERENCES locations(store_id),
    customer_address VARCHAR(250)
);
"""
cur.execute(create_table_customers)

#Collecting user inputs based on what task they would like to perform
selector = input("You can ADD(1)\n\tDELETE(2)\n\tSEARCH(3)\n\tUPDATE(4)\n\tQUIT(q)\nWhat action would you like to compelete today? (Enter the according number):\t")

if selector == 'q':
    quit()

data = int(input("Which section of information would you like to alter today?:\n\tLocations(0)\n\tStaff(1)\n\tInventory(2)\n\tCustomers(3)\n\t"))
1
#Conditional statements that run based on what inputs were provided
if selector == '1':
    add_option(data)
elif selector == '2':
    delete_option(data)
elif selector == '3':
    search_option(data)
elif selector == '4':
    update_option(data)

#Closing all connections
conn.commit()
cur.close()
conn.close()