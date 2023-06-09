# Employee Attendance Management System

## Overview
The Employee Attendance Management System project is designed to manage user details and their attendance records. The project uses SQLite for data storage and Streamlit for user interface and is organized into two key components: User Management and Attendance Management.

The production project is hosted on AWS EC2 instance, ensuring a high level of availability and scalability. It incorporates a simple continuous integration and continuous deployment (CI/CD) pipeline to keep the system updated with the most recent changes with a batch script that automatically fetches and integrates updates from a GitHub repository.

For secure handling of sensitive information, the project utilizes Streamlit's secrets management. It is worth that this secret data is not included in the Git repository and these files are in the .gitignore list which restricts their push to the Git repository. 

This document is structured into various sections, each providing detailed information about different aspects of the project. These include sections for User Management, Attendance Management, CI/CD setup, Validation Rules and  Secrets Management.

## Business Rules
- Each user must have a unique ID.
- User details and Attendance records can be created and modified.
- Each attendance record is associated with a user ID and includes date, time, and type.
- It is possible to fetch attendance records based on user ID with specific time periods (3 months only).

## Section 1: User Management

### UserController

The `UserController` is responsible for handling operations related to user data. It interacts with an SQLite database to store and retrieve user data.

#### Methods
- `__init__(self, db_path: str) -> None:`
  Initializes the UserController with the provided database path.
- `insert_employeee(self, inputs: dict) -> User:`
  Creates a new user in the database. If a user with the same identification already exists, the operation is rolled back and returns None.
- `select_info_employees(self, selected_columns: list) -> User:`
  Retrieves all information about registered employees with only selected fields.
- `update_employee(self, user_id: str, selecte_columns: list) -> UserDTO:`
  Updates an existing user's details in the database. Rolls back the transaction if there is an error during the operation.
- `update_employees_status(self, user_id:str, status: str) -> UserDTO:`
  Updates the status of a employee in the database. 

### UserView

The `UserView` is responsible for providing a user interface for managing user data. It leverages Streamlit to create an easy-to-use interface.

#### Methods
- `insert_user(self) -> None:`
  Provides a user interface to add a new user to the database.
- `update_user(self) -> None:`
  Provides a user interface to update the details of an existing user.
- `select_users(self) -> None:`
  Provides a user interface to view the details of all registered employees.
- `update_status_users(self) -> None:`
  Provides a user interface to update the status of all employees in the database.

## Section 2: Attendance Management

### AttendanceController

The `AttendanceController` is responsible for handling operations related to user attendance. It interacts with an SQLite database to store and retrieve attendance data.

#### Methods
- `__init__(self, db_path: str) -> None:`
  Initializes the AttendanceController with the provided database path.
- `check_attendance(self, user_id: str, date: str, type: str, time: str) -> Attendance:`
  Checks if a given attendance record exists. If not, it creates the record. If the record already exists, it rolls back the operation and returns None.
- `create_attendance(self, user_id: str, date: str, type: str, time: str) -> Attendance:`
  Creates a new attendance record in the database with the provided user ID, date,

 type, and time. If a record with these parameters already exists, it will roll back the operation and return None.
- `get_attendance_by_userid(self, user_id: str) -> List[Attendance]:`
  Retrieves all attendance records from the database that are associated with a given user ID.
- `modify_attendance(self, user_id: str, date: str, time: str, point_type: str) -> None:`
  Modifies an existing attendance record in the database.
- `get_attendance_by_user_periods(self, user_id: str, start_date: str, end_date: str) -> List[Attendance]:`
  Retrieves all attendance records from the database that are associated with a specific user ID and within a specified date range.
- `get_all_attendances_by_periods(self, start_date: str, end_date: str) -> List[Attendance]:`
  Fetches all attendance records for all users within a specified date range. This method also retrieves the complete name of each user from a join operation with the users table.
- `delete_attendance(self, user_id: str, date: str, point_type: str) -> None:`
   Delete the attedance of specific employee on certain date and point_type.
  

### AttendanceView

The `AttendanceView` provides a user interface for managing user attendance. It leverages Streamlit to create an easy-to-use interface.

#### Methods
- `create_attendance(self) -> None:`
  Provides a user interface to add a new attendance record to the database.
- `change_attendance(self) -> None:`
  Provides a user interface to modify an existing attendance record.
- `get_attendances(self) -> None:`
  Provides a user interface to view the attendance records of a specific user.
- `delete_attendance(self) -> None:`
  Provides a user interface to the delete attendance records of a specific user, date and point_type.
- `send_mail_data(self) -> None:`
  Provides a user interface to view all attendance records in a given date range with send mail button.

## Section 3: CI/CD Setup
Batch file located on `deploy` folder to perform continuous integration and deployment (CI/CD) of the project. The script  kills any existing Streamlit process, pulls the latest changes from the main branch of the GitHub repository and runs the Streamlit app up-to-date code.

## Section 4: Permissions
Certain features and actions in the Employee Attendance Management System require authentication using a password. These features include:
- Creating User
- Updating User Information
- Updating Employee Status
- Modifying Attendance Records

## Section 5: Validation Rules
Validation rules have been established in this project to ensure the integrity of data that's being entered. Here are the key rules:

- `is_numeric_field(value):` This function checks if a value is numeric or not.
- `is_6_chars_long(value):` This function checks if a value has a length of 6 characters.
- `validate_phone_number(value):` This function validates if a value follows the pattern of a phone number.
- `is_correct_name(value):` This function checks if a name value is neither None nor an empty string.
  
These rules are critical when creating a new user as they help ensure the consistency and accuracy of user data.

## Section 6: Streamlit Secrets Management
Sensitive data like API keys and database credentials are managed using Streamlit secrets. This file is not included in the Git repository due to security reasons and is present in the .gitignore file. 

When pulling your app, add a file called `secrets.toml` in a folder called `.streamlit` at the root of the repo and copy/paste your own secrets into that file. More details [here](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management).

## Section 7: Logging Function Calls

The `log.py` file on  `utils` folder contains a decorator function called `log_function_calls` that is used to add logging when some functions are called in the interface. It will store these logs into SQLite database table called `function_calls_log`.

## Section 8: Dependencies
You can install all the required dependencies by running the following command in your terminal:

```bash
pip install -r requirements.txt
```
The `requirements.txt` file contains a list of all the Python packages and their versions required to run the project. 


## Usage

This project employs a central `main` function to handle the operation of the system. In this function, instances of `UserController` and `AttendanceController` are initialized with a path to an SQLite database, which is obtained from the `db_path` variable in the `utils.database` module.

Similarly, instances of `UserView` and `AttendanceView` are also created, which are then used to manage user interactions and system outputs.

The core code structure is as follows:

```python
from utils.database import create_table_users, create_table_attendance, create_table_logs, db_path

def main():
    # Set Streamlit page configuration
    st.set_page_config(
        page_title="Employee Attendance Management System",
        page_icon="📋",
        initial_sidebar_state="expanded"
    )   

    # Instantiate controllers
    user_controller = UserController(db_path)
    attendance_controller = AttendanceController(db_path)

    # Instantiate views
    user_view = UserView(user_controller)
    attendance_view = AttendanceView(user_controller, attendance_controller)

    # Define user actions and corresponding functions
    actions = {
        "Employee Management": ["Register", "View", "Update", "Activate / Deactivate"],
        "Attendance Control": ["Register Attendance", "View Records","Modify Records","Send Data"]
    }

    # User selection handling in the sidebar
    action_type = st.sidebar.radio("Category", list(actions.keys()))
    page = st.sidebar.selectbox(f"Function", actions[action_type])

    # Call corresponding functions based on user's selection
    # If action type is 'Employee Management'
    if action_type == 'Employee Management':
        if page == "Register":
            user_view.insert_user()
        elif page == "View":
            user_view.select_users()
        elif page == "Update":
            user_view.update_user()
        elif page == "Activate / Deactivate":
            user_view.updatestatus_users()
    # If action type is 'Attendance Control'
    else:
        if page == "Register Attendance":
            attendance_view.create_attendance()
        elif page == "View Records":
            attendance_view.get_attendances()
        elif page == "Modify Records":
            attendance_view.change_attendance()
        elif page == "Send Data":
            attendance_view.send_mail_data()


if __name__ == '__main__':
    # Create necessary tables in the database
    create_table_users()
    create_table_attendance()
    create_table_logs()

    # Call the main function
    main()
```
This configuration allows for a flexible, modular system where new actions and their corresponding functions can be added easily 
as the project expands.
When the program is run, it creates necessary tables in the database and then calls the main function to start the interactive interface.
