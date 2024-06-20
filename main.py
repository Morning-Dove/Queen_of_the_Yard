import os
import re
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select
from square.client import Client
from square.http.auth.o_auth_2 import BearerAuthCredentials

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
import requests

from database import get_db
from schema import Customer, Invoice, Job, User, Employee, Expense, Services, Frequency, ServiceArea


URL = "https://connect.squareupsandbox.com/v2"
TOKEN = os.getenv("TOKEN")
SQ_APPLICATION_ID = os.getenv("SQ_APPLICATION_ID")
SQ_APPLICATION_SECRET = os.getenv("SQ_APPLICATION_SECRET")
SQUARE_ACCESS_TOKEN = "SQUARE_ACCESS_TOKEN"#os.getenv("SQUARE_ACCESS_TOKEN")


app = FastAPI()
load_dotenv()


headers: dict[str, str] = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json',
}


client = Client(
    #access_token=SQUARE_ACCESS_TOKEN,
    bearer_auth_credentials=BearerAuthCredentials(access_token=SQUARE_ACCESS_TOKEN),
    environment='sandbox')


#
# *** SERVICES ***
#


@app.get("/services", tags=["Services"])
async def get_services(db: Session = Depends(get_db)) -> list[Services]:
    return db.exec(select(Services)).all()


# Creates a service
@app.post("/services", tags=["Services"])
async def create_service(service: Services, db: Session = Depends(get_db)):
    db.add(service)
    db.commit()
    raise HTTPException(status_code=201, detail="Service Created")


# # Updates or Creates a Service
@app.put("/services/{service}", tags=["Services"])
async def update_service(serviceId: int, updated_service: Services, db: Session = Depends(get_db)):
    existing_service = db.get(Services, serviceId)
    if not existing_service:
        db.add(updated_service)
        db.commit()
        raise HTTPException(status_code=201, detail="Service Created")
    
    for key, value in updated_service.model_dump().items():
        setattr(existing_service, key, value)
    db.add(existing_service)
    db.commit()
    raise HTTPException(status_code=201, detail="Service Updated")


# Delete a service by serviceId
@app.delete("/services/{serviceId}", tags=["Services"])
async def delete_service(serviceId: int, db: Session = Depends(get_db)):
    service = db.get(Services, serviceId)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    db.delete(service)
    db.commit()
    raise HTTPException(status_code=200, detail="Service Deleted")


#
# ***FREQUENCY***
#

@app.get("/frequency", tags=["Frequency"])
async def get_frequency(db: Session = Depends(get_db)) -> list[Frequency]:
    return db.exec(select(Frequency)).all()


# Creates a frequency for time of service
@app.post("/frequency", tags=["Frequency"])
async def create_frequency(frequency: Frequency, db: Session = Depends(get_db)):
    db.add(frequency)
    db.commit()
    raise HTTPException(status_code=201, detail="Frequency Created")


# Updates or Creates a Service
@app.put("/frequency/{frequencyId}", tags=["Frequency"])
async def update_frequency(frequencyId: int, updated_frequency: Frequency, db: Session = Depends(get_db)):
    existing_frequency = db.get(Frequency, frequencyId)
    if not existing_frequency:
        db.add(updated_frequency)
        db.commit()
        raise HTTPException(status_code=201, detail="Frequency Created")
    
    for key, value in updated_frequency.model_dump().items():
        setattr(existing_frequency, key, value)
    db.add(existing_frequency)
    db.commit()
    raise HTTPException(status_code=201, detail="Frequency Updated")


# Delete frequency of service by frequencyId
@app.delete("/frequency/{frequencyId}", tags=["Frequency"])
async def delete_frequency(frequencyId: int, db: Session = Depends(get_db)):
    frequencies = db.get(Frequency, frequencyId)
    if not frequencies:
        raise HTTPException(status_code=404, detail="Frequency of service not found")
    db.delete(frequencies)
    db.commit()
    raise HTTPException(status_code=200, detail="Frequency Deleted")


#
# *** SERVICE AREA ***
#


@app.get("/servicearea", tags=["Service Area"])
async def get_service_area(db: Session = Depends(get_db)) -> list[ServiceArea]:
    return db.exec(select(ServiceArea)).all()


# Creates a Service Area
@app.post("/servicearea", tags=["Service Area"])
async def create_service_area(serviceArea: ServiceArea, db: Session = Depends(get_db)):
    db.add(serviceArea)
    db.commit()
    raise HTTPException(status_code=201, detail="Service Area Created")


# Updates or Creates a town within the service area
@app.put("/servicearea/{serviceAreaId}", tags=["Service Area"])
async def update_service_area(serviceAreaId: int, updated_serviceArea: ServiceArea, db: Session = Depends(get_db)):
    existing_serviceArea = db.get(ServiceArea, serviceAreaId)
    if not existing_serviceArea:
        db.add(updated_serviceArea)
        db.commit()
        raise HTTPException(status_code=201, detail="Service Area Created")
    for key, value in updated_serviceArea.model_dump().items():
        setattr(existing_serviceArea, key, value)
    db.add(existing_serviceArea)
    db.commit()
    raise HTTPException(status_code=201, detail="Service Area Updated")


# Delete a town in a service area by serviceAreaId
@app.delete("/servicearea/{serviceAreaId}", tags=["Service Area"])
async def delete_service_area(serviceAreaId: int, db: Session = Depends(get_db)):
    serviceArea = db.get(ServiceArea, serviceAreaId)
    if not serviceArea:
        raise HTTPException(status_code=404, detail="Service Area not found")
    db.delete(serviceArea)
    db.commit()
    raise HTTPException(status_code=200, detail="Service Area Deleted")


#
# ***CUSTOMER***
#


#Returns a customer by Id or a list of all customers
@app.get("/customer", tags=["Customer"])
async def get_customers(custId: int = None, db: Session = Depends(get_db)):
    if custId:
        return [db.get(Customer, custId)]
    return db.exec(select(Customer)).all()


# Creates a customer
@app.post("/customer", tags=["Customer"])
async def create_customer(customer: Customer, db: Session = Depends(get_db)):
    db_customer = Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    raise HTTPException(status_code=201, detail="Customer Created")


# Updates or Creates a Customer
@app.put("/customer/{customerId}", tags=["Customer"])
async def update_customer(custId: int, updated_customer: Customer, db: Session = Depends(get_db)):
    existing_customer = db.get(Customer, custId)
    if not existing_customer:
        db.add(updated_customer)
        db.commit()
        raise HTTPException(status_code=201, detail="Customer Created")
    for key, value in updated_customer.model_dump().items():
        setattr(existing_customer, key, value)
    db.add(existing_customer)
    db.commit()
    raise HTTPException(status_code=201, detail="Customer Updated")


# Deletes a customer by CustomerId
@app.delete("/customer/{customerId}", tags=["Customer"])
async def delete_customer(custId: int, db: Session = Depends(get_db)):
    customer = db.get(Customer, custId)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(customer)
    db.commit()
    raise HTTPException(status_code=200, detail="Customer Deleted")


#
# ***EMPLOYEE***
#


#Returns an employee by Id or a list of all employees
@app.get("/employee", tags=["Employee"])
async def get_employee(EmpId: int = None, db: Session = Depends(get_db)):
    if EmpId:
        return [db.get(Employee, EmpId)]
    return db.exec(select(Employee)).all()


# Creates an Employee
@app.post("/employee", tags=["Employee"])
async def create_employee(employee: Employee, db: Session = Depends(get_db)):
    db_employee = Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    raise HTTPException(status_code=201, detail="Employee Created")


# Updates or Creates a Employee
@app.put("/employee/{EmpId}", tags=["Employee"])
async def update_employee(EmpId: int, updated_employee: Employee, db: Session = Depends(get_db)):
    existing_employee = db.get(Employee, EmpId)
    if not existing_employee:
        db.add(updated_employee)
        db.commit()
        raise HTTPException(status_code=201, detail="Employee Created")
    for key, value in updated_employee.model_dump().items():
        setattr(existing_employee, key, value)
    db.add(existing_employee)
    db.commit()
    raise HTTPException(status_code=201, detail="Employee Updated")


# Delete an employee by EmpId
@app.delete("/employee/{EmpId}", tags=["Employee"])
async def delete_employee(EmpId: int, db: Session = Depends(get_db)):
    employee = db.get(Employee, EmpId)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
    raise HTTPException(status_code=200, detail="Employee Deleted")


#
# *** USER ***
#


@app.get("/user", tags=['Users'])
async def get_user(db: Session = Depends(get_db)) -> list[User]:
    return db.exec(select(User)).all()


# Creates a user
@app.post("/user", tags=['Users'])
async def create_user(user: User, db: Session = Depends(get_db)):
    email = user.email

    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if not re.match(email_pattern, email):
        raise HTTPException(status_code=400, detail="Invalid email address")

    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    raise HTTPException(status_code=201, detail="User Created")


# Updates or Creates a User
@app.put("/user/{userId}", tags=['Users'])
async def update_user(userId: int, updated_user: User, db: Session = Depends(get_db)):
    existing_user = db.get(User, userId)
    if not existing_user:
        #create_user(updated_user)
        db.add(updated_user)
        db.commit()
        raise HTTPException(status_code=201, detail="User created")
    for key, value in updated_user.model_dump().items():
        setattr(existing_user, key, value)
    db.add(existing_user)
    db.commit()
    raise HTTPException(status_code=201, detail="User Updated.")


# Delete a user by userId
@app.delete("/user/{userId}", tags=['Users'])
async def delete_user(userId: int, db: Session = Depends(get_db)):
    user = db.get(User, userId)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    raise HTTPException(status_code=200, detail="User Deleted")


#
# ** INVOICE ***
#


#Returns a invoice by Id or a list of all invoices
@app.get("/invoice", tags=["Invoice"])
async def get_invoice(invoiceId: int = None, db: Session = Depends(get_db)):
    if invoiceId:
        return [db.get(Invoice, invoiceId)]
    return db.exec(select(Invoice)).all()


# Creates an Invoice
@app.post("/invoice", tags=["Invoice"])
async def create_invoice(invoice: Invoice, db: Session = Depends(get_db)):
    db_invoice = Invoice(**invoice.model_dump())
    db.add(db_invoice)
    db.commit()
    raise HTTPException(status_code=201, detail="Invoice Created")


# Updates or Creates a Invoice
@app.put("/invoice/{invoiceId}", tags=["Invoice"])
async def update_invoice(invoiceId: int, updated_invoice: Invoice, db: Session = Depends(get_db)):
    existing_invoice = db.get(Invoice, invoiceId)
    if not existing_invoice:
        db.add(updated_invoice)
        db.commit()
        raise HTTPException(status_code=201, detail="Invoice Created")
    for key, value in updated_invoice.model_dump().items():
        setattr(existing_invoice, key, value)
    db.add(existing_invoice)
    db.commit()
    raise HTTPException(status_code=201, detail="Invoice Updated")


# Deletes a invoice by invoiceId
@app.delete("/invoice/{invoiceId}", tags=["Invoice"])
async def delete_invoice(invoiceId: int, db: Session = Depends(get_db)):
    invoice = db.get(Invoice, invoiceId)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    db.delete(invoice)
    db.commit()
    raise HTTPException(status_code=200, detail="Invoice Deleted")


#
# *** EXPENSE ***
#


#Returns an expense by Id or a list of all Expenses
@app.get("/expense", tags=["Expense"])
async def get_expense(ExpenseId: int = None, db: Session = Depends(get_db)):
    if ExpenseId:
        return [db.get(Expense, ExpenseId)]
    return db.exec(select(Expense)).all()


# Creates an Expense
@app.post("/expense", tags=["Expense"])
async def create_expense(expense: Expense, db: Session = Depends(get_db)):
    db_expense = Expense(**expense.model_dump())
    db.add(db_expense)
    db.commit()
    raise HTTPException(status_code=201, detail="Expense Created")


# Updates or Creates a Expense
@app.put("/expense/{EmpId}", tags=["Expense"])
async def update_expense(EmpId: int, updated_expense: Expense, db: Session = Depends(get_db)):
    existing_expense = db.get(Expense, EmpId)
    if not existing_expense:
        db.add(updated_expense)
        db.commit()
        raise HTTPException(status_code=201, detail="Expense Created")
    for key, value in updated_expense.model_dump().items():
        setattr(existing_expense, key, value)
    db.add(existing_expense)
    db.commit()
    raise HTTPException(status_code=201, detail="Expense Updated")


# Delete an expense by expenseId
@app.delete("/expense/{expenseId}", tags=["Expense"])
async def delete_expense(expenseId: int, db: Session = Depends(get_db)):
    expense = db.get(Expense, expenseId)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    raise HTTPException(status_code=200, detail="Expense Deleted")


#
# ***JOB***
#


#Returns a job by Id or a list of all jobs
@app.get("/job", tags=["Job"])
async def get_jobs(jobId: int = None, db: Session = Depends(get_db)):
    if jobId:
        return [db.get(Job, jobId)]
    return db.exec(select(Job)).all()


# Creates a Job
@app.post("/job", tags=["Job"])
async def create_job(job: Job, db: Session = Depends(get_db)):
    db.add(job)
    db.commit()
    raise HTTPException(status_code=201, detail="Job Created")


# Updates or Creates a Job
@app.put("/job/{JobId}", tags=["Job"])
async def update_job(jobId: int, updated_job: Job, db: Session = Depends(get_db)):
    existing_job = db.get(Job, jobId)
    if not existing_job:
        db.add(updated_job)
        db.commit()
        raise HTTPException(status_code=201, detail="Job Created")
    for key, value in updated_job.model_dump().items():
        setattr(existing_job, key, value)
    db.add(existing_job)
    db.commit()
    raise HTTPException(status_code=201, detail="Job Updated")


# Deletes a Job by JobId
@app.delete("/job/{JobId}", tags=["Job"])
async def delete_job(jobId: int, db: Session = Depends(get_db)):
    job = db.get(Job, jobId)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    raise HTTPException(status_code=200, detail="Job Deleted")


# Email Submission


def send_email(smtp_server, smtp_port, from_email, password, subject, body, to_email):
    # Set up the server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(from_email, password)

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    server.send_message(msg)
    server.quit()


#########################################################
                ### ***SQUARE*** ###
#########################################################


#
# ***PAYMENTS***
#


#Retrieves a list of payments taken by the account making the request.
@app.get("/payments", tags=["Square Payment"])
async def list_payments():
    response = requests.get(url=f"{URL}/payments", headers=headers)

    if response.status_code == 200:
        payments = response.json()['payments']
        print(payments)
        return payments
    else:
        print(f"Error: {response.status_code}, {response.text}")
        raise HTTPException(status_code=404, detail="Payment not found")

# Gets a Payment by ID
@app.get("/payments/{payment_id}", tags=["Square Payment"])
async def GetPayment(payment_id: str) -> dict:
    response = requests.get(url=f"{URL}/payments/{payment_id}", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=404, detail="Payment not found with payment_id {payment_id}")
    

# Creates a Payment in Square. Dollar amount is in cents. 100 = $1.00
@app.post("/payments", tags=["Square Payment"])
async def create_payment(amount: int, source_id: str, idempotency_key: str):
    payload = {
        "source_id": source_id,
        "idempotency_key": idempotency_key,
        "amount_money": {
            "amount": amount,
            "currency": "USD"
        }
    }

    url = f"{URL}/payments"
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        error_detail = response.json()["errors"][0]["detail"] if "errors" in response.json() else response.text
        raise HTTPException(status_code=response.status_code, detail=f"Failed to create payment: {error_detail}")



# # Completes (captures) a payment. Runs after create payment.
# @app.post("/payments/{payment_id}/complete")
# async def complete_payment(payment_id):
#     pass

# #Cancels (voids) a payment.
# @app.post("/payments/{payment_id}/cancel")
# async def cancel_payment(payment_id):
#     pass

# #Updates a payment with the APPROVED status
# @app.put("/payments/{payment_id}")
# async def update_payment(payment_id):
#     pass

# #
# # *** REFUNDS ***
# #

# #Retrieves a specific refund using the refund_id.
# @app.get("/refunds/{refund_id}")
# async def payment_refund(refund_id):
#     pass


# #Retrieves a list of refunds for the account making the request. 
# @app.get("/refunds")
# async def list_payment_refunds():
#     pass


# #Refunds a payment. 
# @app.post("/refunds")
# async def refund_payment(idempotency_key, amount_money):
#     pass

# #
# # *** INVOICES ***
# #

# #Returns a list of invoices for a given location. 
# @app.get("/invoices")
# async def get_invoices(location_id):
#     pass

# #Retrieves an invoice by invoice ID.
# @app.get("/invoices/{invoice_id}")
# async def get_invoice_byID(invoice_id):
#     pass


# #Creates a draft invoice for an order created using the Orders API
# @app.post("/invoices")
# async def create_invoice(invoice):
#     pass


# #Searches for invoices from a location specified in the filter.
# @app.post("/invoices/search")
# async def search_invoices(query):
#     pass


# #Uploads a file and attaches it to an invoice. 
# @app.post("/invoices/{invoice_id}/attachments")
# async def create_invoice_attachment(invoice_id):
#     pass


# #Cancels an invoice.
# @app.post("/invoices/{invoice_id}/cancel")
# async def cancel_invoice(invoice_id):
#     pass


# #Publishes the specified draft invoice.
# @app.post("/invoices/{invoice_id}/publish")
# async def publish_invoice(invoice_id):
#     pass


# #Updates an invoice by modifying fields, clearing fields, or both.
# @app.put("/invoices/{invoice_id}")
# async def update_invoice(invoice_id):
#     pass


# #Deletes the specified invoice.
# @app.delete("/invoices/{invoice_id}")
# async def delete_invoice(invoice_id):
#     pass


# #Removes an attachment from an invoice and permanently deletes the file.
# @app.delete("/invoices/{invoice_id}/attachments/{attachment_id}")
# async def delete_invoice_attachment(invoice_id, attachment_id):
#     pass








