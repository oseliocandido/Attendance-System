# Employee Attendance Management System

## Overview
This project contains the core functionality to manage user details and their attendance records using SQLite for data storage and Streamlit for user interface. The project is divided into two main sections: Users and Attendance.

## Business Rules
- Each user must have a unique ID.
- User details like name and identification number can be updated.
- Attendance records can be created and modified.
- Each attendance record is associated with a user ID and includes date, time, and type.
- It is possible to fetch attendance records based on user ID and specific time periods.

## Section 1: User Management

### UserController

#### Description

The `UserController` is responsible for handling operations related to user data. It interacts with an SQLite database to store and retrieve user data.

#### Methods
- **`__init__(self, db_path: str) -> None:`**
  - Initializes the UserController with the provided database path.

- **`insert_user(self, name: str, identification: str) -> User:`**
  - Creates a new user in the database. If a user with the same identification already exists, the operation is rolled back and returns None.

- **`get_user_by_id(self, user_id: str) -> User:`**
  - Retrieves a user from the database using the provided user ID.

- **`update_user(self, user_id: str, name: str, identification: str) -> None:`**
  - Updates an existing user's details in the database. Rolls back the transaction if there is an error during the operation.

- **`update_employees_status(self, active: str) -> None:`**
  - Updates the status of all employees in the database.

### UserView

#### Description

The `UserView` is responsible for providing a user interface for managing user data. It leverages Streamlit to create an easy-to-use interface.

#### Methods
- **`add_user_interface(self) -> None:`**
  - Provides a user interface to add a new user to the database.

- **`update_user_interface(self) -> None:`**
  - Provides a user interface to update the details of an existing user.

- **`view_user_interface(self) -> None:`**
  - Provides a user interface to view the details of an existing user.

- **`update_status_users_interface(self) -> None:`**
  - Provides a user interface to update the status of all employees in the database.

## Section 2: Attendance Management

### AttendanceController

#### Description

The `AttendanceController` is responsible for handling operations related to user attendance. It interacts with an SQLite database to store and retrieve attendance data.

#### Methods
- **`__init__(self, db_path: str) -> None:`**
  - Initializes the AttendanceController with the provided database path.

- **`check_attendance(self, user_id: str, date: str, type: str, time: str) -> Attendance:`**
  - Checks if a given attendance record exists. If not, it creates the record. If the record already exists, it rolls back the operation and returns None.

- **`create_attendance(self, user_id: str, date: str, type: str, time: str) -> Attendance:`**
  - Creates a new attendance record in the database with the provided user ID, date, type, and time. If a record with these parameters already exists, it will roll back the operation and return None.

- **`get_attendance_by_userid(self, user_id: str) -> List[Attendance]:`**
  - Retrieves all attendance records from the database that are associated with a given user ID.

- **`

modify_attendance(self, user_id: str, date: str, time: str, point_type: str) -> None:`**
  - Modifies an existing attendance record in the database.

- **`get_attendance_by_user_periods(self, user_id: str, start_date: str, end_date: str) -> List[Attendance]:`**
  - Retrieves all attendance records from the database that are associated with a specific user ID and within a specified date range.

- **`get_all_attendances_by_periods(self, start_date: str, end_date: str) -> List[Attendance]:`**
  - Fetches all attendance records for all users within a specified date range. This method also retrieves the complete name of each user from a join operation with the users table.

### AttendanceView

#### Description

The `AttendanceView` provides a user interface for managing user attendance. It leverages Streamlit to create an easy-to-use interface.

#### Methods
- **`add_attendance(self) -> None:`**
  - Provides a user interface to add a new attendance record to the database.

- **`modify_attendance(self) -> None:`**
  - Provides a user interface to modify an existing attendance record.

- **`view_attendance_by_user(self) -> None:`**
  - Provides a user interface to view the attendance records of a specific user.

- **`view_all_attendances(self) -> None:`**
  - Provides a user interface to view all attendance records in a given date range.

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