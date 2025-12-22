# Expense Tracker – CS50 Final Project

#### Video Demo: <URL WILL BE ADDED AFTER RECORDING>

#### Author: Piotr Grzybowski [GitHub username]

---

## Description

Expense Tracker is a web application designed to help users record and monitor their personal expenses. The application allows users to add, edit, and review expenses, as well as view summarized spending data grouped by categories. Expenses can be assigned to custom categories, making it easier to organize and analyze financial activity.

The application includes user authentication, allowing each user to register and log in to a personal account. All expenses and categories are associated with the authenticated user, ensuring that financial data is private and separated between users.

In addition to basic expense management, the application enables users to create, edit, and delete expense categories. The expense history can be filtered by category, allowing users to quickly review specific types of spending and gain better insight into their financial habits.

The main problem addressed by this project is the lack of awareness of everyday expenses. By providing a structured overview of recorded costs, the application helps users analyze their spending patterns and make more informed financial decisions.

This application was developed as the final project for Harvard’s CS50 course. The goal of the project was to apply the knowledge gained throughout the course in a practical context, focusing on backend development, database design, and building a complete web application from scratch.

---

## Project Overview

The application is designed as a user-based system that requires registration and authentication before accessing any financial data. New users can create an account, while returning users can log in using their credentials. Before authentication, access to the application is limited to login and registration functionality only.

After successful login, the user is redirected to the main dashboard. The dashboard provides a high-level overview of the user’s financial activity, including a summary of total expenses and the number of recorded entries. Expenses are additionally grouped by categories to give a clearer picture of spending distribution.

Authenticated users gain access to full application functionality through the navigation menu. This includes adding new expenses, viewing expense history, and managing expense categories.

When adding a new expense, the user provides the expense amount, selects a category, and may optionally include a description. Input validation ensures that required fields, such as amount and category, are provided before the expense can be saved. After a successful submission, the user is redirected to the expense history view.

The expense history displays a list of all expenses recorded by the user. From this view, users can filter expenses by category, add new entries, and edit or delete existing expenses. Each expense entry is uniquely identified and all operations are performed on a per-user basis.

The application also includes a dedicated section for managing expense categories. Users can create new categories by providing a unique name and a short description. Existing categories can be edited, and unused categories can be deleted. Validation rules ensure data consistency and prevent invalid operations.

Additionally, users can manage their account settings, including updating their username and changing their password. For security reasons, existing passwords are never displayed, and only a new password can be set.

---

## Technology Stack

The application was built using technologies introduced during the CS50 course, combined with tools and platforms I was already familiar with. The selected stack focuses on backend fundamentals, relational data modeling, and clear application architecture.

**Python** was used as the main programming language. It was introduced during the course and serves as the foundation for application logic, request handling, and data processing.

**Flask** is a lightweight backend web framework used to manage routing, request handling, session-based authentication, and overall application structure. Its minimalistic approach provides full control over the request–response flow and aligns well with the backend concepts taught in CS50.

**SQLAlchemy** was used to execute raw SQL queries within the Flask application. Instead of relying on ORM abstractions, raw SQL was intentionally chosen to maintain direct control over database operations and to strengthen understanding of relational queries and data manipulation.

**Alembic** was used for database migrations. It allows versioning and controlled evolution of the database schema, making it possible to safely create, modify, and maintain tables and relationships during development.

**PostgreSQL** is used as the relational database management system. It stores all application data, including users, expenses, and categories. PostgreSQL was selected for its reliability, strong support for relational constraints, and suitability for real-world backend applications.

**Neon** is used as the cloud platform hosting the PostgreSQL database. It provides a managed, serverless PostgreSQL environment, allowing the application to connect to a remote database without maintaining local database infrastructure.

**Jinja** is the templating engine used to dynamically render HTML pages using data provided by the Flask backend. It enables server-side rendering of user-specific views and application content.

**Bootstrap** is used as the primary CSS framework for building the user interface. It provides a set of reusable UI components, layout utilities, and predefined styles that speed up frontend development and ensure visual consistency.

**CSS** is used for custom styling and fine-tuning the appearance beyond the default Bootstrap components.

**JavaScript** is used sparingly to enhance user experience, such as displaying confirmation dialogs for destructive actions and showing informational toast notifications.

---

## Application Architecture

The application uses environment-based configuration stored in a `.env` file. The `DATABASE_URL` variable contains the connection string required to connect to the PostgreSQL database hosted on the Neon platform. Additionally, the `FLASK_ENV` variable defines the runtime environment of the Flask application, with development mode used by default.

The `DATABASE_URL` configuration is essential for establishing a database connection and for the correct operation of the application. Without a valid database connection, the application cannot function properly.

The application operates using HTTP GET and POST requests, depending on the purpose of each route. GET requests are used to retrieve and display application data, while POST requests are used to submit new data provided by the user through HTML forms.

When handling a GET request, the backend processes the request, retrieves relevant data from the database, formats the results, and returns a dynamically rendered HTML response using server-side templates.

POST requests are treated as data submission actions. Input data provided by the user is validated before any further processing occurs. If the validation rules are satisfied, the data is processed and persisted in the database using SQL queries.

Routes and application sections that require authentication are protected using the `login_required` decorator. This mechanism checks whether a user identifier is present in the current session. If the user is not authenticated, access is denied and the application redirects the user to the login or registration page.

The application actively validates user input submitted through forms before performing database operations. If validation fails or a database constraint error occurs, the application redirects the user back to the originating view and provides feedback using the Flask `flash` mechanism, which is displayed to the user in the form of toast notifications.

## Database Design

The database consists of three main tables: `users`, `categories`, and `expenses`. The schema was designed to support a multi-user application while maintaining clear relationships between users, their expenses, and expense categories.

The `users` table stores user account information. Each user is identified by a unique primary key `id`. The `username` field is a string with a maximum length of 80 characters and must be unique. User passwords are not stored directly; instead, a hashed password is saved in the `hash` field, which supports secure authentication.

The `categories` table stores expense category data. Each category has a unique primary key `id` and a unique `name` field with a maximum length of 100 characters. An optional `description` field allows additional information to be stored for each category. Categories are used to organize expenses and provide meaningful grouping of financial data.

The `expenses` table is the core table of the application. Each expense record includes a unique primary key `id`, a numeric `amount` value, and an optional `description`. The `created_at` field is automatically populated by the database server at the time of record creation.

Each expense is associated with exactly one user and one category. The `user_id` field creates a foreign key relationship with the `users` table, ensuring that all expenses are owned by a specific authenticated user. The `category_id` field creates a foreign key relationship with the `categories` table, allowing expenses to be grouped and filtered by category. These relationships enforce data consistency and enable user-scoped access to financial records.

---

## Key Features

- **User authentication** – supports multiple users by providing registration and login functionality, with all data scoped to the authenticated user.
- **Expense creation** – allows users to add expense records that are explicitly associated with their account.
- **Category management** – enables creating and editing expense categories, and deleting categories only if they are not currently in use.
- **Expense history** – provides a complete list of user expenses, with the ability to filter by category, as well as edit or delete existing entries.
- **Server-side data validation** – validates all user input on the backend to prevent invalid, inconsistent, or potentially malicious data from being processed or stored.

---

## File Structure

- **app.py** – the main application entry point. It defines routes, handles request processing, and coordinates application logic.
- **helpers.py** – contains helper and utility functions that are imported and reused across the application where needed.
- **models.py** – defines the database schema and table structures used by SQLAlchemy and Alembic migrations.
- **requirements.txt** – lists all Python dependencies required to run the application.
- **seed_categories.py** – a script used to populate the `categories` table with initial data.
- **alembic.ini** – Alembic configuration file used to manage database migrations.
- **.env** – stores environment variables, including database connection settings and Flask runtime configuration. This file is required for the application to function correctly.
- **.gitignore** – specifies files and directories that should be excluded from version control.
- **templates/** – contains HTML templates rendered by the Flask backend using Jinja.
- **static/** – contains static assets such as custom CSS styles and JavaScript files.
- **migrations/** – stores Alembic migration files that track changes to the database schema.
- **flask_session/** – directory used by Flask to store server-side session data.

## Design Decisions & Trade-offs

**Flask** was chosen as the backend framework due to its lightweight nature, simplicity, and fast configuration. It was heavily used throughout the CS50 course, which allowed for efficient development without unnecessary overhead. Alternative solutions such as Next.js or Node.js with Express were considered, but they introduce additional complexity and require more setup. A transition to a different framework would be reasonable if the application were to be prepared for a production-scale deployment.

**Server-side rendering** was intentionally selected instead of a client-heavy frontend approach. The backend generates complete HTML views in response to user actions, while the frontend layer is limited to handling basic interactions. This approach simplifies the architecture, reduces frontend complexity, and keeps the application logic centralized on the server.

**Raw SQL queries** were used instead of relying on ORM abstractions. This decision provides full control over database interactions and reinforces understanding of relational databases and SQL. The trade-off is increased responsibility for query correctness, validation, and security, which requires careful handling of user input and database constraints.

**PostgreSQL with Neon** was selected as the database solution. Neon provides a serverless PostgreSQL environment with a free tier, making it well-suited for an academic project. This choice removes the need to configure and maintain database infrastructure while still allowing the use of a production-grade relational database system.

The decision was made to **not implement a Single Page Application (SPA), REST API, or automated end-to-end tests**. Due to time constraints and the academic nature of the project, manual testing was performed during development and before each feature was committed to GitHub. Introducing a REST API or SPA architecture would have added an additional abstraction layer that was unnecessary for a Flask-based server-rendered application. If the project were to be expanded or refactored into a JavaScript-based stack (e.g., React with Node.js and Express), implementing a REST API and automated tests would become essential.

---

## Future Improvements

- **REST API layer** – expose application functionality through a RESTful API to allow integration with external clients or a separate frontend application.
- **Frontend SPA** – refactor the frontend into a Single Page Application using a JavaScript framework such as React, with the backend serving as an API-only service.
- **Automated testing** – introduce unit tests and end-to-end tests to improve reliability and reduce the risk of regressions during further development.
- **Advanced reporting** – add more detailed financial summaries, such as monthly reports, charts, and data exports (e.g., CSV).
- **User roles and permissions** – extend the authentication system to support different user roles and more granular access control.
- **Improved validation and error handling** – further strengthen backend validation rules and provide more detailed error feedback.
