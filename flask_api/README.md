**Hansel Bank API Documentation**

**Overview**

Hansel Bank API Link deployed in :

1. Koyeb : https://wet-francoise-greedybugz-3bc4de3c.koyeb.app/
2. GitHub : https://github.com/revou-fsse-oct24/milestone-3-ClementHansel

The Hansel Bank API is a RESTful backend for a modern banking application. It provides core functionality for:

- **User Management**: Registering, logging in, and managing user profiles.
- **Account Management**: Creating, retrieving, updating, and deleting bank accounts.
- **Transaction Management**: Performing transactions (deposits, withdrawals, transfers) and retrieving transaction histories with filtering.

This documentation details the API endpoints, system architecture, testing and development challenges, and potential improvements for production-readiness.

**1\. API Components**

**1.1. User Management**

**New Features and Enhancements**

- **User Registration and Authentication:**
  - Introduced a registration flow requiring username, password, and email.
  - Authentication has been streamlined using JWT tokens for secure user login.

**Endpoints:**

**POST /api/users/register**

- Registers a new user account.
- **Request Body**:

json

CopyEdit

{

"username": "exampleuser",

"password": "examplepassword",

"email": "<user@example.com>"

}

- **Response**:

json

CopyEdit

{

"message": "User registered successfully"

}

**POST /api/users/login**

- Authenticates the user and returns a JWT token.
- **Response**:

json

CopyEdit

{

"access_token": "token_here",

"user_id": 1

}

**GET /api/users/profile**

- Retrieves the profile of the currently authenticated user.

**PUT /api/users/me**

- Updates the authenticated user’s profile (e.g., changing username).

**PUT /api/users/password**

- Changes the user’s password.

**PATCH /api/users/profile**

- Updates additional profile details (e.g., address, phone).

**DELETE /api/users/**

- Deletes a user account (requires proper authorization).

**1.2. Account Management**

**New Features and Enhancements**

- **Account Creation and Management**:
  - Users can now create, view, update, and delete bank accounts.
  - Enhancements include returning the account balance and name on account creation and update.

**Endpoints:**

**POST /api/accounts**

- Creates a new bank account for the authenticated user.
- **Request Body**:

json

CopyEdit

{

"account_name": "Savings Account",

"initial_balance": 1000

}

- **Response**:

json

CopyEdit

{

"account_id": 1

}

**GET /api/accounts**

- Retrieves all accounts owned by the authenticated user.

**GET /api/accounts/{id}**

- Retrieves details of a specific account by its ID.

**PUT /api/accounts/{id}**

- Updates details of an existing account.

**DELETE /api/accounts/{id}**

- Deletes a bank account.

**1.3. Transaction Management**

**New Features and Enhancements**

- **Transaction Types and Management**:
  - Introduced the transaction_type field to clearly differentiate between deposit, withdrawal, and transfer.
  - Allows users to perform transactions and retrieve detailed history.

**Endpoints:**

**POST /api/transactions**

- Creates a new transaction (deposit, withdrawal, or transfer).
- **Request Body**:

json

CopyEdit

{

"account_id": 1,

"amount": 100,

"transaction_type": "deposit"

}

- **Response**:

json

CopyEdit

{

"transaction_id": 1

}

**GET /api/transactions**

- Retrieves all transactions for the authenticated user’s accounts.

**GET /api/transactions/{id}**

- Retrieves details of a specific transaction.

**2\. Development Challenges**

**Difficulties Faced**

- **JWT Authentication & Data Types**:
  - Ensuring the token’s subject was stored and verified correctly as a string was challenging. We had to ensure proper handling when decoding the JWT token.
- **URL Prefix Management**:
  - Initially faced issues with duplicate URL segments (e.g., /api/users/users). Standardizing all authentication endpoints under /api/users solved the problem.
- **Database Initialization for Testing**:
  - Using an in-memory SQLite database for tests required proper teardown and lifecycle management. Pytest fixtures were used to automate database setup and cleanup.
- **Environment Configuration**:
  - Loading sensitive configuration data, such as SECRET_KEY and JWT_SECRET_KEY, using environment variables and the python-dotenv library added complexity to the development process.
- **Handling Input Variations**:
  - Standardized key names across endpoints (e.g., using transaction_type instead of type) for clarity and consistency.

**3\. Potential Improvements**

**Security Enhancements**

- **Input Validation**:
  - Integrate libraries like Marshmallow or Pydantic for robust request and response validation.
- **Rate Limiting**:
  - Use Flask-Limiter to prevent abuse by limiting the number of requests per user or IP address.
- **Two-Factor Authentication (2FA)**:
  - Implement 2FA for sensitive operations, adding an extra layer of security to user actions.

**Performance & Scalability**

- **Caching**:
  - Utilize Redis or similar caching strategies to optimize frequently accessed endpoints, such as transaction histories.
- **Database Optimization**:
  - Add proper indexing for commonly queried fields and use pagination to manage large datasets efficiently.
- **Asynchronous Processing**:
  - Offload heavy tasks (e.g., batch transactions) to background jobs using Celery to improve app performance.

**Feature Enhancements**

- **Audit Logging**:
  - Implement detailed logging for all modifications to user accounts and transactions to track changes and identify issues.
- **Enhanced Filtering & Pagination**:
  - Improve transaction endpoints by adding advanced filtering options (e.g., filter by transaction type, date range) and pagination.
- **Account Linking**:
  - Add support for linking external bank accounts or consolidating multiple internal accounts.
- **Real-Time Notifications**:
  - Implement WebSocket support to provide users with real-time notifications on account activity (e.g., deposits, withdrawals).
- **Dispute Management**:
  - Add endpoints to allow users to report and resolve transaction disputes.

**Testing & Deployment**

- **Expanded Testing**:
  - Increase the coverage of unit, integration, and end-to-end tests using tools like pytest and Postman to ensure reliability.
- **CI/CD Integration**:
  - Set up automated testing pipelines (e.g., GitHub Actions, Travis CI) to ensure that tests are run on every commit and pull request.
- **Production Deployment**:
  - Transition the app to use a production-grade WSGI server like Gunicorn, and containerize it with Docker for easier deployment to cloud platforms like AWS, GCP, or Heroku.

**4\. Conclusion**

The Hansel Bank API has evolved significantly, with the implementation of critical features like JWT authentication, user profile management, transaction handling, and account management. Alongside functional improvements, we've also focused on security and performance enhancements to make the API more scalable and secure for production use.

**Next Steps:**

- Continue refining the API with additional features like real-time notifications and dispute management.
- Implement further security measures such as rate limiting and 2FA for enhanced protection.
- Optimize the backend for scalability and deploy the application using modern infrastructure practices (e.g., Docker and Kubernetes).
