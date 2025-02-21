# Documentation for User Login and Transaction Handling Diagrams

## Overview

This document provides an explanation of the **User Login** and **Transaction Handling** diagrams created using **Lucidchart**. These diagrams outline the process flow for handling user authentication and transactions in a system.

## 1. User Login Flowchart

![User Login Flowchart]([revou-module-6/user_login.png](https://github.com/revou-fsse-oct24/milestone-3-ClementHansel/blob/main/revou-module-6/revou-module-6/user_login.png))

### Description

The **User Login** flowchart represents the process of user authentication. It covers:

- User credential entry
- Credential verification by the system
- JWT token generation on successful login
- Handling of incorrect credentials

### Steps

1. **User enters credentials** - The user provides a username and password.
2. **Matching the credentials** - The system checks if the credentials match existing records.
3. **Decision: Matched?**
   - **If No** → Save log and show an error message to the user.
   - **If Yes** → Generate a JWT token.
4. **Save Log** - The system logs the authentication attempt.
5. **Return Token to User** - The JWT token is sent to the client for future authentication.
6. **Redirect to User Home Page** - The user is successfully logged in and redirected.

## 2. Transaction Handling Flowchart

![Transaction Handling Flowchart](revou-module-6/transaction_handling.png)

### Description

The **Transaction Handling** flowchart represents the process of checking and deducting a user's balance when making a transaction. It covers:

- Checking available balance
- Handling insufficient balance cases
- Deducting balance for successful transactions
- Invoice generation

### Steps

1. **User clicks the pay button** to initiate a transaction.
2. **Check User Balance** - The system verifies if the user has sufficient funds.
3. **Decision: Enough Balance?**
   - **If No** → Save log, show an insufficient balance message, and redirect to the top-up page.
   - **If Yes** → Deduct the user’s balance.
4. **Save Log** - The system logs the transaction.
5. **Generate Invoice** - The system generates an invoice for the transaction.
6. **Save Invoice** - The invoice details are stored.
7. **Show Invoice** - The user receives the invoice confirmation.

## How to Create These Diagrams in Lucidchart

### Steps to Create a Flowchart

1. **Open Lucidchart** - Log in or create an account at [Lucidchart](https://www.lucidchart.com/).
2. **Create a New Document** - Select "Flowchart" from the templates.
3. **Add Swimlanes** (Optional) - Use the "Swimlane" feature to separate **User** and **System** processes.
4. **Drag and Drop Shapes** - Use:
   - **Rectangles** for process steps.
   - **Diamonds** for decision points.
   - **Arrows** to connect steps.
   - **Circles** for start and end points.
5. **Style the Diagram** - Adjust colors, fonts, and labels for clarity.
6. **Save & Export** - Save the diagram and export it as PNG or PDF for sharing.

## Conclusion

The **User Login** and **Transaction Handling** diagrams provide a clear visual representation of authentication and payment processes. These diagrams can be used to improve system design and ensure a smooth user experience.
