# Running the Django Application

This guide will walk you through setting up and running the Django application on your local machine. Ensure you have Python, pip, and PostgreSQL installed before you start.

## Step 1: Extract Files from Zipped File

Extract the files from the zipped archive of the repository. Locate the zipped file in your system and use any file extraction tool or command line utility to unzip the contents into a folder of your choice.

## Step 2: Set Up a Virtual Environment

Create a virtual environment to manage your project's dependencies separately by running:

python -m venv venv

Activate the virtual environment:

- On Windows:

  .\venv\Scripts\activate

- On macOS and Linux:

  source venv/bin/activate

## Step 3: Install Required Libraries

Install the required libraries specified in `requirements.txt`:

pip install -r requirements.txt

## Step 4: Set Up the Database

1. Ensure PostgreSQL is running on your system.
2. Create a database for the project using the `todo_db.sql` file provided:

   psql -U [username] -d postgres -f path/to/todo_db.sql

   Replace `[username]` with your PostgreSQL username.

3. Update the database configuration in `todo/todo/settings.py` to match your PostgreSQL settings:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

   Ensure you replace `your_db_name`, `your_db_user`, and `your_db_password` with the actual database name, user, and password.

## Step 5: Navigate to the Project Directory

Ensure you are in the directory containing `manage.py`:

cd path/to/todo

## Step 6: Run the Django Server

Start the Django development server:

python manage.py runserver

The server will start, and you should see something like this:

```shell
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

## Step 7: Making Requests Using Postman

With the server running, you can now use Postman to make requests to your Django application. Here is a link to a Postman collection with sample requests for the application:

[Postman Collection with Sample Requests](https://richard-quayson.postman.co/workspace/My-Workspace~8623b0d5-b357-477a-88e8-966a777ca0f6/folder/22193987-ba80c1be-c9c6-4633-90fa-30069ece7821?action=share&creator=22193987&ctx=documentation)

## Step 8: Link to GitHub repository:

Find the link to the repository [here]().