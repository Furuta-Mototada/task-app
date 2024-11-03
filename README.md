# Todo App

## Table of Contents
1. [Backend (Flask)](#backend-flask)
   - [Setup](#setup)
   - [Project Structure](#project-structure)
   - [API Endpoints](#api-endpoints)
2. [Frontend (React)](#frontend-react)
   - [Setup](#setup-1)
   - [Project Structure](#project-structure-1)
   - [Features](#features)
3. [Recording](#recording)

## Backend (Flask)

### Setup

1. Navigate to the `app-flask` directory:
    ```sh
    cd app-flask
    ```

2. Create a virtual environment:
    ```sh
    python -m venv venv
    ```

3. Activate the virtual environment:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

5. Run the Flask application:
    ```sh
    python3 app.py
    ```

### Project Structure

- `app.py`: Entry point for the Flask application.
- `project/`: Contains the main application code.
  - `__init__.py`: Initializes the Flask app and its extensions.
  - `auth.py`: Handles authentication routes.
  - `models.py`: Defines the database models.
  - `task.py`: Handles task-related routes.

### API Endpoints

#### Task Endpoints

- `GET /api/tasks`: Retrieve tasks.
- `POST /api/tasks`: Create a new task.
- `PUT /api/tasks/:task_id`: Update a task.
- `DELETE /api/tasks/:task_id`: Delete a task.
- `PUT /api/tasks/:task_id/complete`: Mark a task as complete.
- `PUT /api/tasks/:task_id/move`: Move a task to a different list.
- `PUT /api/tasks/:task_id/expand`: Expand or collapse a task.

#### List Endpoints

- `GET /api/lists`: Retrieve lists.
- `POST /api/lists`: Create a new list.
- `PUT /api/lists/:list_id`: Update a list title.
- `DELETE /api/lists/:list_id`: Delete a list.

#### Authentication Endpoints

- `POST /api/auth/login`: Log in a user.
- `POST /api/auth/register`: Register a new user.
- `POST /api/auth/logout`: Log out a user.
- `GET /api/auth/current_user`: Get the current logged-in user.
- `PUT /api/auth/user`: Update the current user's password.
- `DELETE /api/auth/user`: Delete the current user's account.

## Frontend (React)

### Setup

1. Navigate to the [app-react](http://_vscodecontentref_/13) directory:
    ```sh
    cd app-react
    ```

2. Install the dependencies:
    ```sh
    npm install
    ```

3. Start the React application:
    ```sh
    npm start
    ```

### Project Structure

- `src/`: Contains the main application code.
  - `ApiClient.js`: Handles API requests.
  - `ProtectedRoute.js`: Handles protected routes.
  - `App.js`: Main application component.
  - `components/`: Contains reusable components.
    - `AddListModal.js`: Modal for adding a new list.
    - `AddTaskModal.js`: Modal for adding a new task.
    - `Board.js`: Main board component displaying lists and tasks.
    - `EditListModal.js`: Modal for editing a list title.
    - `EditTaskModal.js`: Modal for editing a task.
    - `List.js`: Component for displaying a list and its tasks.
    - `Sidebar.js`: Navigation sidebar component.
    - `TaskCard.js`: Component for displaying an individual task.
    - `UserProfile.js`: Component for displaying and updating user profile settings.
  - `contexts/`: Contains context providers.
    - `ApiProvider.js`: Provides API client context.
    - `AuthProvider.js`: Provides authentication context.
  - `pages/`: Contains page components.
    - `AuthPage.js`: Page for user authentication (login/register).
    - `HomePage.js`: Main home page displaying the board.
    - `ProfilePage.js`: Page for user profile settings.

### Features

![App Review](app-review.png)

1. **User Authentication**
   - **Login**: Users can log in using their username and password.
   - **Register**: New users can register by providing a username and password.
   - **Logout**: Logged-in users can log out of their account.

2. **Profile Management**
   - **Update Password**: Users can update their account password.
   - **Delete Account**: Users can delete their account, including all associated data.

3. **List Management**
   - **Initialization**: When users create their account, Todo and Completed lists are added. These cannot be modified or deleted. 
   - **Create List**: Users can create new lists.
   - **Update List**: Users can update the title of existing lists.
   - **Delete List**: Users can delete lists, including all associated tasks.

4. **Task Management**
   - **Create Task**: Users can create new tasks within a list.
   - **Update Task**: Users can update the title and description of existing tasks.
   - **Delete Task**: Users can delete tasks, including all associated subtasks.
   - **Complete Task**: Users can mark tasks as complete or incomplete.
   - **Move Task**: Users can move tasks between different lists.
   - **Expand/Collapse Task**: Users can expand or collapse tasks to show or hide subtasks.
   - **Subtask**: Users can create/update/delete/complete/expand&collapse subtasks. Subtasks cannot be moved around.


## Recording
[Watch the video on Loom](https://www.loom.com/share/8455756e85a945ea9b668652abd3c7ff?sid=16b93682-05b5-4772-bda2-99b43c8e07dd)