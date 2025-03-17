# User Management System

## Backend Setup

1. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

3. Run the Flask app:
   ```sh
   flask run
   ```

## Frontend Setup

1. Navigate to the `frontend` directory:
   ```sh
   cd frontend
   ```

2. Install the dependencies:
   ```sh
   npm install
   ```

3. Start the React app:
   ```sh
   npm start
   ```

## Usage

- The backend will be running on `http://localhost:5000`.
- The frontend will be running on `http://localhost:3000`.

You can now use the User Management System to add and view users.

## GitHub & Documentation

1. Push the project to GitHub:
   ```sh
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin master
   ```

2. Create a Postman collection for API testing and include it in the repository.

## Database Integration Process

The backend uses Flask with SQLAlchemy for MySQL database integration and PyMongo for MongoDB logging. The frontend is built with React and uses Axios for API calls.
