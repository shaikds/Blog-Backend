# Post Management API
An API for managing posts built with FastAPI. 
A small project for learning FastAPI framework for backend.

## Key Features
* Create Posts: Allows the creation of new posts with a title, content, and images.

* Read Posts: Can read a specific post by its unique ID, with error handling for when the post is not found.

* Data Validation: Uses Pydantic to ensure all data is valid.

* Error Handling: Returns appropriate status codes, such as 404 Not Found and 400 Bad Request.

* Security: Manages secret variables (like API keys) using a .env file.
