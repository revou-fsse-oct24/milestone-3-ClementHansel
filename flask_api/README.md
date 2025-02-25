# **Hansel Bank API Documentation**

## **Overview**

The Hansel Bank API is a RESTful backend designed for a modern banking
application. It provides core features for:

- **User Management:** Registering, logging in, and managing user
  profiles.

- **Account Management:** Creating, retrieving, updating, and deleting
  bank accounts, along with additional metadata and support for
  multiple account types.

- **Transaction Management:** Performing transactions (deposits,
  withdrawals, transfers) and retrieving detailed transaction
  histories with filtering and pagination.

This documentation covers the API endpoints, architecture, development
challenges, and potential improvements for production-readiness.

## **1. API Components**

### **1.1. User Management**

#### **Endpoints**

##### - **POST /api/users**\

_Creates a new user account._\
 **Request Body:**

{

\"username\": \"exampleuser\",

\"password\": \"examplepassword\"

}

**Response:**

{\"user_id\": 1}

##### - **POST /api/users/login**\

_Authenticates the user and returns a JWT token._\
 **Request Body:**

{

\"username\": \"exampleuser\",

\"password\": \"examplepassword\"

}

**Response:**

{\"access_token\": \"\<JWT_TOKEN\>\"}

##### - **GET /api/users/me**\

_Retrieves the profile of the currently authenticated user._\
 **Headers:**

Authorization: Bearer \<JWT_TOKEN\>

**Response:**

{\"user_id\": 1, \"username\": \"exampleuser\"}

- **PUT /api/users/me**\
  _Updates the profile of the authenticated user._\
  **Request Body:** (e.g., updating username)

{\"username\": \"newusername\"}

**Response:**

{\"message\": \"Profile updated\"}

#### **Additional Endpoints (for enhanced user management)**

##### - **PUT /api/users/password**\

_Allows a user to change their password._\
 **Request Body:**

{\"old_password\": \"oldpass\", \"new_password\": \"newpass\"}

##### - **PUT /api/users/email**\

_Allows a user to change their email address._\
 **Request Body:**

{\"new_email\": \"newemail@example.com\"}

##### - **PATCH /api/users/profile**\

_Update additional profile details (contact info, address, etc.)._\
 **Request Body:**

{\"address\": \"123 Main St\", \"phone\": \"555-1234\"}

### **1.2. Account Management**

#### **Endpoints**

##### - **POST /api/accounts**\

_Creates a new bank account for the authenticated user._\
 **Request Body:**

{

\"account_name\": \"Savings Account\",

\"initial_balance\": 1000

}

**Response:**

{\"account_id\": 1}

##### - **GET /api/accounts**\

_Retrieves all accounts belonging to the authenticated user._\
 **Response:**

\[

{\"id\": 1, \"account_name\": \"Savings Account\", \"balance\": 1000}

\]

- **GET /api/accounts/\<account_id\>**\
  _Retrieves details of a specific account by its ID._\
  **Response:**

{

\"id\": 1,

\"account_name\": \"Savings Account\",

\"balance\": 1000,

\"created_at\": \"2025-02-21T12:00:00Z\",

\"transaction_summary\": { \... } // Optional additional metadata

}

##### - **PUT /api/accounts/\<account_id\>**\

_Updates details of an existing account (only for the owner)._\
 **Request Body:**

{\"account_name\": \"Updated Account\", \"initial_balance\": 1200}

**Response:**

{\"message\": \"Account updated\", \"id\": 1, \"account_name\":
\"Updated Account\", \"balance\": 1200}

##### - **DELETE /api/accounts/\<account_id\>**\

_Deletes an account (only for the owner)._\
 **Response:**

{\"message\": \"Account deleted\", \"id\": 1}

#### **Advanced Features in Account Management**

- **Detailed Account Information:**\
  Endpoints could be enhanced to return additional metadata such as
  creation date, transaction summaries, and account status.

- **Multiple Account Types:**\
  Support for different types (checking, savings, credit, investment)
  by adding a field account_type in the Account model.

- **Account Linking:**\
  Endpoints to link external accounts or consolidate multiple
  accounts.

- **Audit Logging:**\
  Implement logging to track modifications to account details for
  auditing and compliance purposes.

### **1.3. Transaction Management**

#### **Endpoints**

##### - **POST /api/transactions**\

_Initiates a new transaction (deposit, withdrawal, or transfer) for
an account._\
 **Request Body:**

{

\"account_id\": 1,

\"amount\": 100,

\"type\": \"deposit\"

}

**Response:**

{\"transaction_id\": 1}

##### - **GET /api/transactions**\

_Retrieves all transactions for the authenticated user\'s
accounts._\
 **Response:**

\[

{

\"id\": 1,

\"account_id\": 1,

\"amount\": 100,

\"type\": \"deposit\",

\"timestamp\": \"2025-02-21T12:00:00Z\",

\"status\": \"completed\" // optional additional detail

}

\]

##### - **GET /api/transactions/\<transaction_id\>**\

_Retrieves details of a specific transaction (authorization
enforced)._\
 **Response:**

{

\"id\": 1,

\"account_id\": 1,

\"amount\": 100,

\"type\": \"deposit\",

\"timestamp\": \"2025-02-21T12:00:00Z\",

\"status\": \"completed\"

}

#### **Advanced Transaction Management Features**

- **Filtering and Pagination:**

  - Endpoints can accept query parameters (e.g.,
    ?type=deposit&start_date=2025-02-01&end_date=2025-02-28&page=1&per_page=20)
    to filter transactions and paginate results.

- **Detailed Transaction Histories:**

  - Include additional details like transaction status (pending,
    completed, failed) and extra metadata.

- **Batch Processing:**

  - Provide endpoints to process multiple transactions
    asynchronously.

- **Notification Integration:**

  - Implement real-time notifications (e.g., via WebSockets) to
    alert users when transactions occur.

- **Dispute Management:**

  - Add endpoints for users to report and resolve disputes regarding
    transactions.

## **2. Development Challenges**

### **Difficulties Faced**

#### - **JWT Authentication & Data Types:**\

Handling JWT tokens correctly was challenging.

- The token\'s subject (sub) needed to be a string during token
  creation but compared as an integer when verifying ownership.

- Converting JWT identity to the correct type was critical to
  avoid unauthorized errors.

#### - **Blueprint & URL Prefix Management:**\

Organizing endpoints using Blueprints required careful management of
URL prefixes.

- Duplicate segments in endpoints (e.g., /api/users/users) were an
  issue until we standardized the route definitions.

#### - **Database Initialization for Testing:**\

Setting up an in-memory SQLite database for tests and ensuring
proper teardown between tests was tricky.

- Using fixtures in pytest to manage the database lifecycle
  helped, but it required careful configuration.

#### - **Environment & Configuration Management:**\

Using environment variables with python-dotenv and ensuring that
sensitive keys (SECRET_KEY, JWT_SECRET_KEY) were loaded correctly
added complexity.

#### - **Handling Multiple Endpoint Variations:**\

Implementing various endpoints (user, account, transaction) with
different HTTP methods and ensuring proper authorization for each
required careful planning and testing.

## **3. Potential Improvements**

### **Security Enhancements**

- **Input Validation:**\
  Use libraries like Marshmallow or Pydantic to validate and serialize
  inputs/outputs.

- **Rate Limiting:**\
  Implement rate limiting (e.g., using Flask-Limiter) to prevent
  abuse.

- **Two-Factor Authentication (2FA):**\
  Integrate additional authentication factors (via SMS, email, or
  authenticator apps) for sensitive operations.

### **Performance & Scalability**

- **Caching:**\
  Use caching strategies (e.g., Redis) for frequently accessed data
  like transaction histories.

- **Database Optimization:**\
  Index key fields and use pagination for endpoints returning large
  datasets.

- **Asynchronous Processing:**\
  Offload heavy operations (e.g., batch transactions) to background
  jobs using Celery.

### **Feature Enhancements**

- **Comprehensive Audit Logging:**\
  Maintain detailed logs for all account modifications and
  transactions for compliance.

- **Enhanced Transaction Filtering & Pagination:**\
  Add query parameters to transaction endpoints for filtering by date
  range, type, or amount, and implement pagination.

- **Account Linking & Consolidation:**\
  Support linking external accounts and consolidating multiple
  accounts into a unified view.

- **Real-Time Notifications:**\
  Integrate WebSocket support for push notifications on account
  activity or transactions.

- **Dispute Management:**\
  Add endpoints for users to report and track disputes regarding
  transactions.

### **Testing & Deployment**

- **More Extensive Testing:**\
  Expand unit tests, integration tests, and load tests. Consider using
  tools like Postman for end-to-end testing.

- **CI/CD Integration:**\
  Set up Continuous Integration pipelines to automatically run tests
  on commits.

- **Production Deployment:**\
  Use a production WSGI server like Gunicorn, and containerize the
  application using Docker for scalability and ease of deployment.
