[![Upload Python Package](https://github.com/ankit48365/ConnectionVault/actions/workflows/python-publish.yml/badge.svg)](https://github.com/ankit48365/ConnectionVault/actions/workflows/python-publish.yml)
![Latest Release](https://img.shields.io/badge/release-v0.0.4-blue)

# ConnectionVault

## Purpose


The purpose of this project is to centralize the database connections file (as YAML) on a user's machine. The project has two utilities:

1. **Connection Manager:** Allows you to choose and load a connection string in a Python code quickly.

   Python code usage example:

   ```python
   from app.src.connection_utility import load_connections, choose_connection
   from sqlalchemy import create_engine
   import pandas as pd

   def main():
       connections = load_connections()
       conn = choose_connection(connections)

       engine = create_engine(conn)
       query = input("Input your query: ")
       df = pd.read_sql_query(query, engine)
       print(df)

   if __name__ == "__main__":
       main()```
2. **Connection Utility:** Allows you to save new connections, and add, update, delete, or see existing connections in the saved YAML file.

## Running the Project

To run this project, you need to define and save a path with the name `conn_home`. This is where you’ll save the `connections.yaml` file, which stores your database credentials.

## For Windows (CMD):

```
# Define and save the path
setx conn_home "C:\path\outside\your\project\preferably"

# Check the path
echo %conn_home%

# Define and save the path
setx conn_home "C:\path\outside\your\project\preferably"

# Check the path
echo %conn_home%
```
## For Windows Powershell:

```
# Define and save the path
[System.Environment]::SetEnvironmentVariable('conn_home', 'C:\path\outside\your\project\preferably', 'User')

# Check the path
$env:conn_home
```

### For Linux:

```bash
# Define and save the path in your .bashrc
echo 'export conn_home="path/outside/your/project/preferably"' >> ~/.bashrc

# Source the .bashrc to apply changes
source ~/.bashrc
```
