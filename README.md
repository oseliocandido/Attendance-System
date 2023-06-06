# Employee Attendance Management System

## Overview
The Employee Attendance Management System project is designed to manage user details and their attendance records. The project leverages SQLite for data storage and Streamlit for user interface, and is organized into two key components: User Management and Attendance Management.

The project is hosted on an AWS EC2 instance, ensuring a high level of availability and scalability. It incorporates a continuous integration and continuous deployment (CI/CD) pipeline to keep the system updated with the most recent changes. This is achieved through a batch script that automatically fetches and integrates updates from a GitHub repository.

For secure handling of sensitive information, the project utilizes Streamlit's secrets management. It is worth noting that this secret data is not included in the Git repository, owing to the placement of these files in the .gitignore list, which restricts their push to the Git repository. 

This README document is structured into various sections, each providing detailed information about different aspects of the project. These include sections for User Management, Attendance Management, CI/CD setup, AWS Hosting, Validation Rules, and Streamlit Secrets Management.

## Business Rules
- Each user must have a unique ID.
- User details like name and identification number can be updated.
- Attendance records can be created and modified.
- Each attendance record is associated with a user ID and includes date, time, and type.
- It is possible to fetch attendance records based on user ID and specific time periods.
- The user can retrieve the records of attendance with date range related to current and previous two months only.

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
- `update_employee(self, user_id: str, selecte_columns: list) -> None:`
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

### AttendanceView

The `AttendanceView` provides a user interface for managing user attendance. It leverages Streamlit to create an easy-to-use interface.

#### Methods
- `create_attendance(self) -> None:`
  Provides a user interface to add a new attendance record to the database.
- `change_attendance(self) -> None:`
  Provides a user interface to modify an existing attendance record.
- `get_attendances(self) -> None:`
  Provides a user interface to view the attendance records of a specific user.
- `send_mail_data(self) -> None:`
  Provides a user interface to view all attendance records in a given date range with send mail button.

## Section 3: CI/CD Setup
We use a simple batch file to perform continuous integration and deployment (CI/CD) of the project. The script activates the appropriate environment, kills any existing Streamlit process, pulls the latest changes from the main branch of the GitHub repository, and runs the Streamlit app. This ensures that the project is always up-to-date with the latest changes made to the codebase.


## Section 4: AWS Hosting
The project is hosted on an AWS EC2 instance. We make use of the CI/CD setup to continuously fetch the latest changes from the GitHub repository and update the running application on the EC2 instance. This ensures that our application is always running the most recent version of the code.

## Section 5: Validation Rules
Validation rules have been established in this project to ensure the integrity of data that's being entered. Here are the key rules:

- `is_numeric_field(value):` This function checks if a value is numeric or not.
- `is_6_chars_long(value):` This function checks if a value has a length of 6 characters.
- `validate_phone_number(value):` This function validates if a value follows the pattern of a phone number.
- `is_correct_name(value):` This function checks if a name value is neither None nor an empty string.
  
These rules are critical when creating a new user as they help ensure the consistency and accuracy of user data.

## Section 6: Streamlit Secrets Management
Sensitive data like API keys and database credentials are managed using Streamlit secrets. This file is not included in the Git repository due to security reasons and is present in the .gitignore file. AWS Secrets Manager or similar service can be used to manage and retrieve these secrets in a production environment.

## Dependencies

- Python 3.6+
- SQLite
- Streamlit
- User and Attendance Models (`from models.user import User`, `from models.attendance import Attendance, AttendanceName`)


- Logger Utility (`from utils.logs import log_function_calls`)

## Usage

Initialize instances of UserController and AttendanceController with a path to an SQLite database. Use their methods to manage user and attendance data. Initialize instances of UserView and AttendanceView to provide a user interface for data management. For example:

```python
user_controller = UserController('/path/to/database.db')
attendance_controller = AttendanceController('/path/to/database.db')

user_view = UserView(user_controller)
attendance_view = AttendanceView(attendance_controller)
```
