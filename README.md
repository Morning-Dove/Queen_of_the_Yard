A backend system for managing the business operations for Queen of the Yard Lawn Care.
A brief description of the components and functionality included in the code:

**Database Models:** The code defines several SQLAlchemy models representing different entities in the business, such as customers, employees, expenses, invoices, jobs, services, frequencies, account types, and service areas. These models map to database tables and define the structure of the data stored in the database.

**API Endpoints:** The FastAPI framework is used to create HTTP API endpoints for interacting with the backend system. These endpoints allow clients to perform various operations, such as retrieving customer information, creating invoices, updating customer details, deleting customers, and more.

**Database Operations:** The code includes functions to perform CRUD (Create, Read, Update, Delete) operations on the database using SQLModel. For example, there are functions to create new customers, retrieve customer data, update customer details, delete customers, and so on.

**Authentication:** 

**Error Handling:** The code handles errors gracefully by raising HTTPExceptions with appropriate status codes and error messages. This ensures that clients receive meaningful error responses when something goes wrong.

**Integration with Square API:** The code doesn't include direct integration with the Square API, but you mentioned an interest in using the Square API for processing payments. Integrating the Square API would involve adding endpoints and functions to handle payment processing, such as creating payment requests, processing payments, and handling payment confirmations.

Overall, the provided code forms the foundation of a backend system for managing the business operations of Queen of the Yard Lawn Care, including customer management, invoicing, job tracking, and more. With further development and integration with external services like the Square API, this backend system could provide a comprehensive solution for managing the business's financial and operational activities.

#### Getting Started
```sh
requires python version 3.5 or greater
```
```sh
pip install requirements.txt
```


# Lawn Care API

## Pydantic Models

**Services**

Attributes:

- serviceId (int)
- serviceProvided (str)

**Frequency**

Attributes:

- frequencyId (int)
- serviceFrequency (str)

**AccountType**

Attributes:

- accountTypeId (int)
- isResidential (bool)
- isCommercial (bool)

**ServiceArea**

Attributes:

- serviceAreaId (int)
- townServiced (str)

## REST Endpoints

| Name                                | Method | Path                   |
|-------------------------------------|--------|------------------------|
| Retrieve services collection        | GET    | /services              |
| Retrieve service by serviceId       | GET    | /services/:serviceId   |
| Create service                      | POST   | /services              |
| Update service by serviceId         | PUT    | /services/:serviceId   |
| Delete service by serviceId         | DELETE | /services/:serviceId   |
| Retrieve frequency collection       | GET    | /frequency             |
| Retrieve frequency by frequencyId   | GET    | /frequency/:frequencyId|
| Create frequency                    | POST   | /frequency             |
| Update frequency by frequencyId     | PUT    | /frequency/:frequencyId|
| Delete frequency by frequencyId     | DELETE | /frequency/:frequencyId|
| Retrieve account type collection    | GET    | /accounttype           |
| Retrieve service area collection    | GET    | /servicearea           |
| Retrieve service area by serviceAreaId| GET  | /servicearea/:serviceAreaId|
| Create service area                 | POST   | /servicearea           |
| Update service area by serviceAreaId| PUT    | /servicearea/:serviceAreaId|
| Delete service area by serviceAreaId| DELETE | /servicearea/:serviceAreaId|
| Retrieve user collection            | GET    | /user                  |
| Retrieve user by userId             | GET    | /user/:userId          |
| Create user                         | POST   | /user                  |
| Update user by userId               | PUT    | /user/:userId          |
| Delete user by userId               | DELETE | /user/:userId          |
| Retrieve invoice collection         | GET    | /invoice               |
| Retrieve invoice by invoiceId       | GET    | /invoice/:invoiceId    |
| Create invoice                      | POST   | /invoice               |
| Update invoice by invoiceId         | PUT    | /invoice/:invoiceId    |
| Delete invoice by invoiceId         | DELETE | /invoice/:invoiceId    |
| Retrieve customer collection        | GET    | /customer              |
| Retrieve customer by customerId     | GET    | /customer/:customerId  |
| Create customer                     | POST   | /customer              |
| Update customer by customerId       | PUT    | /customer/:customerId  |
| Delete customer by customerId       | DELETE | /customer/:customerId  |
| Retrieve employee collection        | GET    | /employee              |
| Retrieve employee by EmpId          | GET    | /employee/:EmpId       |
| Create employee                     | POST   | /employee              |
| Update employee by EmpId            | PUT    | /employee/:EmpId       |
| Delete employee by EmpId            | DELETE | /employee/:EmpId       |
| Retrieve expense collection         | GET    | /expense               |
| Retrieve expense by expenseId       | GET    | /expense/:expenseId    |
| Create expense                      | POST   | /expense               |
| Update expense by expenseId         | PUT    | /expense/:expenseId    |
| Delete expense by expenseId         | DELETE | /expense/:expenseId    |
| Retrieve job collection             | GET    | /job                   |
| Retrieve job by JobId               | GET    | /job/:JobId            |
| Create job                          | POST   | /job                   |
| Update job by JobId                 | PUT    | /job/:JobId            |
| Delete job by JobId                 | DELETE | /job/:JobId            |