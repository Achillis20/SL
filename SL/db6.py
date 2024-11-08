import mysql.connector
from mysql.connector import Error


# Function to get user input
def get_name_input(prompt_message):
    return input(prompt_message)


# Function to create columns based on user input
def get_columns_input():
    columns = []
    while True:
        column_name = get_name_input("Enter column name (or type 'done' to finish): ")
        if column_name.lower() == 'done':
            break
        data_type = get_name_input(f"Enter data type for '{column_name}' (e.g., INT, VARCHAR): ").upper()

        if data_type == 'VARCHAR':
            size = get_name_input("Enter size for VARCHAR: ")
            columns.append(f"{column_name} {data_type}({size})")
        else:
            columns.append(f"{column_name} {data_type}")
    return ', '.join(columns)


# Function to insert data into the table
def insert_data(cursor, table_name):
    column_names = get_name_input("Enter column names separated by commas: ")
    values = get_name_input("Enter values separated by commas: ")
    insert_query = f"INSERT INTO {table_name} ({column_names}) VALUES ({', '.join(['%s'] * len(values.split(',')))})"
    cursor.execute(insert_query, tuple(values.split(',')))
    connection.commit()
    print(f"Inserted 1 row into '{table_name}' table.")


# Function to delete data from the table
def delete_data(cursor, table_name):
    condition = get_name_input("Enter condition for deletion (e.g., id=1): ")
    delete_query = f"DELETE FROM {table_name} WHERE {condition}"
    cursor.execute(delete_query)
    connection.commit()
    print("Deleted row(s) based on condition.")


# Function to update data in the table
def update_data(cursor, table_name):
    set_values = get_name_input("Enter column(s) and value(s) to set (e.g., name='John Doe'): ")
    condition = get_name_input("Enter condition for updating (e.g., id=1): ")
    update_query = f"UPDATE {table_name} SET {set_values} WHERE {condition}"
    cursor.execute(update_query)
    connection.commit()
    print("Updated row(s) based on condition.")


# Initialize connection to None to handle the exception case
connection = None

# Connect to MySQL
try:
    # Predefined MySQL connection credentials
    user = 'root'  # Replace with your MySQL username
    password = 'your_password'  # Replace with your MySQL password

    # Establishing the connection
    connection = mysql.connector.connect(
        host='localhost',
        user=user,
        password=password,
        auth_plugin='mysql_native_password'
    )

    if connection.is_connected():
        print("Connection successful!")
        cursor = connection.cursor()

        # Step 1: Ask for the database name and check if it exists
        while True:
            db_name = get_name_input("Enter database name: ")
            cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
            db_exists = cursor.fetchone()

            if db_exists:
                print(f"Database '{db_name}' already exists.")
                choice = get_name_input("Do you want to enter a different database name? (y/n): ").lower()
                if choice == 'n':
                    break
            else:
                cursor.execute(f"CREATE DATABASE {db_name}")
                print(f"Database '{db_name}' created.")
                break

        # Step 2: Connect to the specified or created database
        connection.database = db_name

        # Step 3: Ask for the table name and check if it exists
        while True:
            table_name = get_name_input("Enter table name: ")
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            table_exists = cursor.fetchone()

            if table_exists:
                print(f"Table '{table_name}' already exists.")
                choice = get_name_input("Do you want to enter a different table name? (y/n): ").lower()
                if choice == 'n':
                    break
            else:
                columns_definition = get_columns_input()
                create_table_query = f'''
                CREATE TABLE {table_name} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    {columns_definition}
                )
                '''
                cursor.execute(create_table_query)
                print(f"Table '{table_name}' created.")
                break

        # Menu-driven input for insert, delete, update operations
        while True:
            print("\nMenu:")
            print("1. Insert record")
            print("2. Delete record")
            print("3. Update record")
            print("4. Exit")
            choice = get_name_input("Enter your choice: ")

            if choice == '1':
                insert_data(cursor, table_name)
            elif choice == '2':
                delete_data(cursor, table_name)
            elif choice == '3':
                update_data(cursor, table_name)
            elif choice == '4':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

except Error as e:
    print(f"Error: {e}")
finally:
    # Close connection only if it was successfully created
    if connection is not None and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")
