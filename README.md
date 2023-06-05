Blog API

This project is a RESTful API for a blogging platform, developed using Flask, Flask-RESTful, Flask-Smorest, SQLAlchemy, and Marshmallow. It provides a comprehensive set of endpoints for user management and blog post operations. In addition, it integrates with Cloudinary to support image uploading for profile pictures and blog posts.

## Features

### User Management

Users can sign up, log in, and have their information securely stored in the database. User passwords are hashed before storage for enhanced security. Additionally, users can upload profile pictures, which are stored and managed through Cloudinary.

### Token-based Authentication

The API uses JWT (JSON Web Tokens) for user authentication. This allows for secure data transmission between the client and server. After a user logs in, they receive a token which they then use for authentication when making requests.

### Blog Post Operations

Users can create, update, view, and delete blog posts. All blog post operations require user authentication. Users can also upload images for their blog posts, with image storage handled by Cloudinary.

### Validation and Serialization

The API uses Marshmallow for data validation and serialization. This helps ensure data integrity when interacting with the database.

### Error Handling

The API includes error handling, providing meaningful feedback to clients when errors occur.

## Installation

```bash
# Clone the repository

# Enter the project directory

# Install Python dependencies
pip install -r requirements.txt

# Run the application
flask run
