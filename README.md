![Project Logo](https://github.com/viictoo/AirBnB_clone/blob/main/images/logo.png)

# HBNB Console

The **HBNB Console** is a command-line tool(CLI) that allows you to interact with the various models and data of the HBNB programme. It provides a command-line interface to manage instances of various classes through a persistent storage system. This tool is primarily designed to allow interaction with objects in the programme where they can be created, displayed, updated, and deleted.

![Layout](https://github.com/viictoo/AirBnB_clone/blob/main/images/layout.png)

## Features

The HBNB Console supports the following functionalities:

- **Interactive Mode:** You can enter the interactive mode of the console, where you can type commands directly into the terminal.

- **Non-Interactive Mode:** The console can be used in non-interactive mode by piping commands into the console script.

Actions:

- **Create:** Create new instances of classes and save them to the JSON file.

- **Show:** Display detailed information about a specific instance based on its class name and ID.

- **Destroy:** Delete an instance based on its class name and ID.

- **Update:** Update attributes of an instance based on its class name and ID.

- **All:** Display a list of all instances or all instances of a specific class.

- **File Storage:** The console works with a persistent storage system that saves instances in JSON files.

## Running the console

1. Clone the repository.

2. Navigate to the project directory containing the `console.py` script.

3. Run the console using:

   ```
   ./console.py
   ```

   This will start the console in interactive mode, allowing you to type commands directly.

4. Use the available commands to manage instances and data.

## Usage Examples

Here are some example commands you can use in the HBNB Console:

- To create a new instance:

  create <class name>

  ```
  create BaseModel
  ```

- To show details of an instance:
  show <class name>

  ```
  show BaseModel 12345
  ```

- To update attributes of an instance:

  update <class name> <id> <attribute name> "<attribute value>"

  ```
  update BaseModel 12345 name "New Name"
  ```

- To delete an instance:

  destroy <class name> <id>

  ```
  destroy BaseModel 12345
  ```

- To display a list of all instances:

  ```
  all
  ```

- Specific commands eg show, all, count and destroy can also be run in .(dot) format ie:

- To display a list of all instances:
  <class name>.all()

  ```
  BaseModel.all()
  ```

- To count the number of instances:

  <class name>.count()

  ```
  BaseModel.count()
  ```

- To retrieve an instance based on its ID:

  <class name>.show(<id>)

  ```
  BaseModel.show(12345)
  ```

- To update an instance based on its ID:

  <class name>.update(<id>, <attribute name>, <attribute value>)

  ```
  BaseModel.update(12345, "first_name", "Juan")
  ```

- To exit the console:

  ```
  quit
  ```

## Project Contributors

Victor Lang'at

- GitHub: viictoo

Kook Calvin Ayen

- Github: Kook16
