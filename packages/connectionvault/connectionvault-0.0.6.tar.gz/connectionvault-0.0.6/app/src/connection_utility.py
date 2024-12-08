# import pyodbc
import yaml
import os

# Retrieve and verify the environment variable
conn_home = os.getenv('conn_home')
print(f"conn_home: {conn_home}")

# Define the path for the connections file
connections_file = os.path.join(conn_home, 'connections.yaml')
print(f"connections_file: {connections_file}")

# Check if the file exists
if os.path.exists(connections_file):
    print("File exists.")
else:
    print("File does not exist.")

# @trace_func
def make_string(conn_det):
    if conn_det['ConnectionType'] == 'postgres':
        conn_str = f"{conn_det['driver']}://{conn_det['user']}:{conn_det['password']}@{conn_det['host']}:{conn_det['port']}/{conn_det['database']}"
        return conn_str
    elif conn_det['ConnectionType'] == 'sqlserver':
        conn_str = f"mssql+pyodbc://{conn_det['user']}:{conn_det['password']}@{conn_det['host']}:{conn_det['port']}/{conn_det['database']}?driver={conn_det['driver']}&TrustServerCertificate=yes"
        return conn_str

    elif conn_det['ConnectionType'] == 'other':
        print('for future rdbms additions')
        conn_str = 'empty'
        return conn_str
    #  keep adding for more rdbms systesm later
    # elif conn_det['ConnectionType'] == 'other':
        # print('for future rdbms additions')
    else:
         print("Invalid choice. Please try again.")

    # return connections

# @trace_func
def load_connections():
    connections =  {}
    if os.path.exists(connections_file):
        with open(connections_file, 'r') as file:
            connections = yaml.safe_load(file)
    else: print("File does not exist.")
    return connections

# @trace_func
def choose_connection(connections):
    # print('we are in choose_connection functi')
    print('---------------------------------------------------------------------------------')
    print("Available connections:")
    for i, conn_name in enumerate(connections.keys()):
        print(f"{i}: {conn_name}")
    # exitcode = len(connections)+1
    print(f"{len(connections)}: Exit") # Adding an exit option
    # print(f"{exitcode}: Exit")

    while True:
        print('---------------------------------------------------------------------------------')
        choice = input("Choose a connection by number: ")
        if choice.isdigit():
            # print('while true isdigit')
            choice = int(choice)
            # print('while true if - choice is int')
            if choice in range(len(connections)):
                conn_name = list(connections.keys())[choice]
                # print('while true -- if - if return connections[conn_name]')
                conn_det=connections[conn_name]
                conn_str= make_string(conn_det)

                return conn_str
    
            elif choice == len(connections): # Handling the exit option
                print("Exiting.")
                return None
            else: print(f"Invalid choice. Please enter a number between 0 and {len(connections)}.")
        else: print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    load_connections()