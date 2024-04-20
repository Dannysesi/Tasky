# Tasky - Task Manager Application
---
Tasky is a web-based task management application built with Django. It allows users to create, assign, and track tasks within an organization. Tasky provides role-based authentication, ensuring that users only have access to data and functionalities based on their assigned roles.

## Features

- **User Authentication:** Users can register, log in, and manage their accounts.
- **Role-Based Access Control:** Different roles (e.g., admin, manager, team member) have different levels of access to the application's functionalities.
- **Task Management:** Users can create, edit, and delete tasks. Tasks can be assigned to specific users and have statuses (pending, in progress, completed).
- **User Dashboard:** Each user has a personalized dashboard where they can manage their tasks and account settings.

## Getting Started

To run this project locally, follow these steps:

1. Clone this repository:

   ```bash
   git clone https://github.com/Dannysesi/Tasky
   # Install Dependencies:
   pip install -r requirements.txt
   # Apply migrations:
   python manage.py migrate
   # Create superuser:
   python manage.py createsuperuser
   # Runserver (default: http://localhost:8000)
   python manage.py runserver


2. Contributing:
   If you'd like to contribute to this project, please follow these steps:
   ```bash
   # Fork the repository
   git clone https://github.com/Dannysesi/Tasky
   cd task
   # Create a new branch for your feature
   git checkout -b feature-name
   # Make your changes and commit them
   git add .
   git commit -m 'Add some feature'
   # Push to the branch
   git push origin feature-name


## License

[MIT](https://choosealicense.com/licenses/mit/)

