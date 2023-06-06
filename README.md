# Attendance System - Employee Management Module

The Employee Management Module of the Attendance System is developed using Python. It utilizes an SQLite database to manage the user data, and follows an MVC (Model-View-Controller) design pattern. The `UserController.py` file defines the Controller and includes all the functionalities related to user operations such as insert, select, update status and update an existing employee. 

The code can be found in the section titled "UserController.py Code".

## Overview

The `UserController` class controls the interaction between the View (`UserView.py`) and the Models (`User` and `UserDTO`). It handles the business logic for user management. It uses SQLite to handle all its database operations and leverages the `sqlite3` package in Python for this. 

Each method in the `UserController` class is decorated with the `@log_function_calls` decorator. This decorator is used to log function calls which is useful for debugging and understanding the flow of control in the application.

## UserController.py Code

The code provided includes the following methods:

1. `__init__(self, db_path)`: Initializes the UserController with a database path.
2. `insert_employee(self, inputs)`: Inserts a new employee's data into the database.
3. `select_info_employees(self, selected_columns)`: Selects specific employee information from the database.
4. `update_employees_status(self, id, status)`: Updates the status of an employee in the database.
5. `update_employee(self, selected_columns, user_id)`: Updates the information of an existing employee in the database.

Note: See the "Business Rules" section below for more details on the business rules implemented in these methods.

```python
[UserController.py Code Here]
```

## Business Rules

1. **insert_employee(self, inputs)**: This method takes a dictionary of inputs, containing data about an employee to be added to the system. These data include personal and contact information, role, and notes. It uses a transaction to ensure atomicity - if an error occurs during the insertion process, the changes are rolled back and the database remains in a consistent state.

2. **select_info_employees(self, selected_columns)**: This method fetches selected information about all employees in the database. The columns to be retrieved are passed as a list. The fetched data is used to instantiate `UserDTO` objects, which are then returned as a list.

3. **update_employees_status(self, id, status)**: This method is responsible for updating the status of an employee in the system. The status can either be "Ativo" or "Inativo". This change is based on the user ID passed in as an argument. It first retrieves the user data from the database and checks if the user exists. If not, it returns `None`. If the user is found, the status is updated and the updated `UserDTO` object is returned.

4. **update_employee(self, selected_columns, user_id)**: This method allows updating an employee's details in the database. The `selected_columns` parameter is a list of tuples, where each tuple contains a column name and the corresponding new value. It first updates the relevant fields for the employee, and then fetches the updated user data, returning a `UserDTO` object containing the updated data.

Please ensure you have the necessary permissions to perform these operations, and that the input provided follows the correct format and adheres to all relevant rules and constraints. Always test your functions with various edge cases to ensure they handle all potential input correctly. Also, ensure to handle any exceptions that may occur and log them for troubleshooting.

---

As your project evolves, please continue to update this README to ensure it accurately reflects the current state of your project.