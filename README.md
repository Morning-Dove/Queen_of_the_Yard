# Queen of the Yard Lawn Care API

A backend system for managing the business operations for Queen of the Yard Lawn Care.

**Database Models:** The code defines several SQLModels representing different entities in the business, such as customers, employees, expenses, invoices, jobs, services, frequency of service, account types, and service areas. These models map to database tables and define the structure of the data stored in the database.

**API Endpoints:** The FastAPI framework is used to create HTTP API endpoints for interacting with the backend system. These endpoints allow the business to perform various operations, such as retrieving customer information, creating invoices, updating customer details, deleting customers, and more.

**Database Operations:** The code includes functions to perform CRUD (Create, Read, Update, Delete) operations on the database using SQLModel. For example, there are functions to create new customers, retrieve customer data, update customer details, delete customers, and so on.

**Error Handling:** The code handles errors gracefully by raising HTTPExceptions with appropriate status codes and error messages. To ensures meaningful error responses are sent when something goes wrong.

**Integration with Square API:** Integrating the Square API involves adding endpoints and functions to handle payment processing, such as creating payment requests, processing payments, and handling payment confirmations.

Overall, this backend system manages the business operations for Queen of the Yard Lawn Care, including customer management, invoicing, job tracking, and more. With further development and integration with external services like the Square API, this backend system could provide a comprehensive solution for managing the business's financial and operational activities.

## Getting Started

Clone Repository: Clone the repository to your local machine.
```sh
requires python version 3.10 or greater
```

Set Up Virtual Environment: Navigate to the backend folder and set up a virtual environment using your preferred method.

Install Requirements: Install the required Python packages listed in requirements.txt.
```sh
pip install - r requirements.txt
```

Run the Application: Use uvicorn to run the application.
```sh
uvicorn main:app
```

Access the SwaggerUI interface by running 
```sh
http://localhost:8000/docs#
```