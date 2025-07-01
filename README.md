# Skills-Python

Skills-Python is a REST API service for managing skills in projects. Built with Python using Flask, SQLAlchemy, Flask-JWT-Extended, and SQLite.

## Features

- Manage users and projects
- Assign skills to projects
- JWT-based authentication
- Evaluation management
- Client logo serving
- Role management

## Technologies Used

- **Python 3.11+**
- **Flask**
- **SQLAlchemy**
- **Flask-JWT-Extended**
- **Flask-CORS**
- **Flask-Bcrypt**
- **SQLite**

## Installation

1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd skills-python
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```sh
   python app.py
   ```

## API Endpoints

### Initialize Data

Create sample users with projects:

```http
POST http://localhost:5000/init
Content-Type: application/json
```

### Generate Token

Generate an authentication token for a user:

```http
POST http://localhost:5000/token
Content-Type: application/json

{
    "userId": 1,
    "username": "Zoro"
}
```

### Login

Authenticate a user and get a JWT token:

```http
POST http://localhost:5000/users/login
Content-Type: application/json

{
    "username": "admin",
    "password": "password"
}
```

### Projects

- `GET /projects` - Get all projects for authenticated user
- `GET /projects/<id>` - Get project details
- `POST /projects` - Create a new project
- `PUT /projects/<id>` - Update a project
- `DELETE /projects/<id>` - Delete a project
- `POST /projects/<id>/evaluation` - Create evaluation for project
- `PUT /projects/<id>/values` - Save evaluation values
- `GET /projects/<id>/evaluations-dates` - Get evaluation dates
- `GET /projects/<id>/evaluations` - Get evaluations by project and date

### Users

- `GET /users` - Get all users
- `GET /user` - Get current user info
- `GET /users/<id>` - Get user details
- `POST /users` - Create a new user

### Skills

- `GET /skills` - Get all skills

### Roles

- `GET /roles` - Get all roles
- `GET /roles/<id>` - Get role by ID
- `POST /roles` - Create a new role
- `PUT /roles/<id>` - Update a role
- `DELETE /roles/<id>` - Delete a role

### Clients

- `GET /clients` - Get all clients
- `GET /logo/<client_id>` - Get client logo image

### Evaluations

- `GET /evaluation` - Get all evaluations

## Usage

After running `python app.py`, the API will be available at `http://localhost:5000/`.

Most endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## Environment Variables

Create a `.env` file in the project root:

```
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=sqlite:///mydb.db
PORT=5000
```

## License

This project is licensed under the MIT License.
