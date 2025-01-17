# ToDoList Website

## Project Overview

The ToDoList website is a simple yet functional task management application. It allows users to manage their daily tasks efficiently with features to add, delete, and mark tasks as complete. Additionally, the application supports user authentication, enabling functionalities like user registration, password reset, and viewing tasks specific to each user.
#


## Features

### Task Management
- **Add Tasks**: Users can create new tasks by providing a title and an optional description.
- **Delete Tasks**: Tasks can be permanently removed from the list.
- **Mark Tasks as Complete**: Users can toggle a task's status between complete and incomplete.
- **View Tasks**: Tasks are displayed in a list view, filtered by the logged-in user.

### User Authentication
- **User Registration**: New users can create accounts using a secure registration form.
- **Login/Logout**: Existing users can log in to view their tasks or log out to end the session.
- **Password Reset**: Users can request a password reset via email and securely update their credentials.

## Technologies Used

- **Frontend**: HTML, CSS (Bootstrap)
- **Backend**: Django (Python)
- **Database**: SQLite (default Django database)
- **Authentication**: Django authentication system
- **Email**: SMTP (for password reset functionality)
- **Static Files Management**: Whitenoise
