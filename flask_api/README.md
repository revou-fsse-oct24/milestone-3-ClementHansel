# Hansel Bank API Documentation

## Overview

The Hansel Bank API is a RESTful backend for a modern banking application. It provides core functionality for:

- User Management: Registering, logging in, and managing user profiles.

- Account Management: Creating, retrieving, updating, and deleting bank accounts.

- Transaction Management: Performing transactions (deposits, withdrawals, transfers) and retrieving transaction histories with filtering.

This documentation details the API endpoints, system architecture, testing and development challenges, and potential improvements for production-readiness.

---

## 1. API Components

### 1.1. User Management

#### Endpoints

**POST /api/users/register**

Registers a new user account.

Request Body:

{

"username": "exampleuser",

"password": "examplepassword",

"email": "user@example.com"

}

Response:

{

"message": "User registered successfully"

}

\*\*POST /api/users/login\*\*

Authenticates the user and returns a JWT token.

Request Body:

{

"username": "exampleuser",

"password": "examplepassword",

"email": "user@example.com"

}

Response:

{

"access_token": "",

"user_id": 1

}

**GET /api/users/profile**

Retrieves the profile of the currently authenticated user.

Headers:

Authorization: Bearer

Response:

{

"user_id": 1,

"username": "exampleuser",

"email": "user@example.com",

"address": "...",

"phone": "..."

}

**PUT /api/users/me**

Updates the authenticated user’s profile.

Request Body:

{

"username": "newusername"

}

Response:

{

"message": "Profile updated"

}

**PUT /api/users/password**

Changes the user’s password.

Request Body:

{

"old_password": "oldpass",

"new_password": "newpass"

}

**PUT /api/users/email**

Changes the user’s email address.

Request Body:

{

"new_email": "newemail@example.com"

}

**PATCH /api/users/profile**

Updates additional profile details (e.g., address, phone).

Request Body:

{

"address": "123 Main St",

"phone": "555-1234"

}

**DELETE /api/users/**

Deletes a user account (requires proper authorization).

Response:

{

"message": "User deleted successfully"

}

Notes:

- All user-related endpoints are under the \`/api/users\` prefix.

- Registration now requires username, password, and email.

---

### 1.2. Account Management

#### Endpoints

**POST /api/accounts**

Creates a new bank account for the authenticated user.

Request Body:

{

"account_name": "Savings Account",

"initial_balance": 1000

}

Response:

{

"account_id": 1

}

**GET /api/accounts**

Retrieves all accounts owned by the authenticated user.

Response:

[

{

"id": 1,

"account_name": "Savings Account",

"balance": 1000

}

]

**GET /api/accounts/**

Retrieves details of a specific account by its ID.

Response:

{

"id": 1,

"account_name": "Savings Account",

"balance": 1000

}

**PUT /api/accounts/**

Updates details of an existing account (only if owned by the user).

Request Body:

{

"account_name": "Updated Account",

"balance": 1500

}

Response:

{

"message": "Account updated",

"id": 1,

"account_name": "Updated Account",

"balance": 1500

}

**DELETE /api/accounts/**

Deletes a bank account (only if owned by the user).

Response:

{

"message": "Account deleted",

"id": 1

}

Potential Enhancements:

- Return additional metadata (e.g., creation date, transaction summary).

- Support multiple account types and linking external accounts.

- Implement audit logging for account modifications.

---

### 1.3. Transaction Management

#### Endpoints

**POST /api/transactions**

Creates a new transaction (deposit, withdrawal, or transfer).

Note: Use the key "transaction_type" instead of "type".

Request Body:

{

"account_id": 1,

"amount": 100,

"transaction_type": "deposit"

}

Response:

{

"transaction_id": 1

}

**GET /api/transactions**

Retrieves all transactions for the authenticated user’s accounts.

Response:

[

{

"id": 1,

"account_id": 1,

"amount": "100.00",

"transaction_type": "deposit",

"timestamp": "2025-02-21T12:00:00Z"

}

]

**GET /api/transactions/**

Retrieves details of a specific transaction (authorization enforced).

Response:

{

"id": 1,

"account_id": 1,

"amount": "100.00",

"transaction_type": "deposit",

"timestamp": "2025-02-21T12:00:00Z"

}

Potential Enhancements:

- Add query parameters for filtering by type, date range, or amount.

- Implement pagination for large result sets.

- Support additional transaction types (e.g., transfers with separate records for sender and receiver).

- Integrate real-time notifications and dispute management endpoints.

---

## 2. Development Challenges

### Difficulties Faced

- **JWT Authentication & Data Types:**

Handling JWT tokens required ensuring that the token's subject was stored as a string and converting it properly during verification.

- **Blueprint & URL Prefix Management:**

I encountered duplicate URL segments (e.g., \`/api/users/users\`) until I standardized all auth endpoints under \`/api/users\`.

- **Database Initialization for Testing:**

Configuring an in-memory SQLite database for tests and ensuring clean teardown between tests was challenging. Pytest fixtures helped manage this lifecycle.

- **Environment & Configuration Management:**

Loading sensitive configuration (e.g., SECRET_KEY, JWT_SECRET_KEY) using environment variables required careful setup with python-dotenv.

- **Handling Input Variations:**

I standardized key names in transaction requests (using "transaction_type" instead of "type") for clarity and consistency.

---

## 3. Potential Improvements

### Security Enhancements

- **Input Validation:**

Integrate libraries like Marshmallow or Pydantic for robust request and response validation.

- **Rate Limiting:**

Use Flask-Limiter to prevent abuse by limiting the number of requests per user/IP.

- **Two-Factor Authentication (2FA):**

Add an additional authentication factor for sensitive operations.

### Performance & Scalability

- **Caching:**

Use caching strategies (e.g., Redis) for frequently accessed endpoints like transaction histories.

- **Database Optimization:**

Add proper indexing and use pagination to handle large datasets.

- **Asynchronous Processing:**

Offload heavy tasks (e.g., batch transactions) to background jobs with Celery.

### Feature Enhancements

- **Audit Logging:**

Implement comprehensive logging for all modifications to user accounts and transactions.

- **Enhanced Filtering & Pagination:**

Improve transaction endpoints with advanced filtering and pagination parameters.

- **Account Linking:**

Support linking external accounts or consolidating multiple accounts.

- **Real-Time Notifications:**

Integrate WebSocket support for real-time notifications on account activity.

- **Dispute Management:**

Add endpoints to allow users to report and resolve transaction disputes.

### Testing & Deployment

- **Expanded Testing:**

Increase the coverage of unit, integration, and end-to-end tests using pytest and Postman.

- **CI/CD Integration:**

Set up automated testing pipelines to run tests on every commit.

- **Production Deployment:**

Use a production-grade WSGI server (e.g., Gunicorn) and containerize the app with Docker for easier deployment.

---
