from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from starlette.testclient import TestClient
from sqlmodel import create_engine, Session
import pytest

from main import app, Services, Frequency, ServiceArea, Customer, Employee, User, Invoice, Expense, Job, create_payment
from database import get_db


client = TestClient(app)


@pytest.fixture
def db_session():
    session = MagicMock(spec=Session)
    return session

@pytest.fixture
def override_get_db(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.pop(get_db)


# *** SERVICES ***


def test_get_services():
    with MagicMock() as mock_db:
        mock_db.exec.return_value.all.return_value = [
            Services(serviceId=1, service="Fencing"),
        ]
        app.dependency_overrides[get_db] = lambda: mock_db

        response = client.get("/services")

        assert response.status_code == 200

        expected_response = [
            {
                "serviceId": 1,
                "service": "Fencing",
            }
        ]
        assert response.json() == expected_response


def test_create_service():
    service_data = {
        "serviceId": 1000,
        "service": "Mowing",
    }

    with MagicMock() as mock_db:
        app.dependency_overrides[get_db] = lambda: mock_db
        response = client.post("/services", json=service_data)

        assert response.status_code == 201
        assert response.json() == {"detail": "Service Created"}

        created_service = mock_db.add.call_args[0][0]
        assert created_service.serviceId == service_data["serviceId"]
        assert created_service.service == service_data["service"]


def test_delete_service():
    service_id = 1

    with MagicMock() as mock_db:
        app.dependency_overrides[get_db] = lambda: mock_db
        mock_db.get.return_value = Services(serviceId=service_id)
        response = client.delete(f"/services/{service_id}")

        assert response.status_code == 200
        assert response.json() == {"detail": "Service Deleted"}

        deleted_service = mock_db.delete.call_args[0][0]
        assert deleted_service.serviceId == service_id


# *** FREQUENCY ***


def test_get_frequency():
    with MagicMock() as mock_db:
        mock_db.exec.return_value.all.return_value = [
            Frequency(frequencyId=1, serviceFrequency="Monthly"),
        ]
        app.dependency_overrides[get_db] = lambda: mock_db

        response = client.get("/frequency")

        assert response.status_code == 200

        expected_response = [
            {
                "frequencyId": 1,
                "serviceFrequency": "Monthly",
            }
        ]
        assert response.json() == expected_response


def test_create_frequency():
    frequency_data = {
        "frequencyId": 1000,
        "serviceFrequency": "Monthly",
    }

    with MagicMock() as mock_db:
        app.dependency_overrides[get_db] = lambda: mock_db
        response = client.post("/frequency", json=frequency_data)

        assert response.status_code == 201
        assert response.json() == {"detail": "Frequency Created"}

        created_frequency = mock_db.add.call_args[0][0]
        assert created_frequency.frequencyId == frequency_data["frequencyId"]
        assert created_frequency.serviceFrequency == frequency_data["serviceFrequency"]


def test_update_frequency():
    frequency_id = 1
    updated_frequency_data = {
        "frequencyId": frequency_id,
        "serviceFrequency": "Weekly"
    }

    with MagicMock() as mock_db:
        app.dependency_overrides[get_db] = lambda: mock_db
        mock_db.get.return_value = Frequency(frequencyId=frequency_id)
        response = client.put(f"/frequency/{frequency_id}", json=updated_frequency_data)

        assert response.status_code == 201
        assert response.json() == {"detail": "Frequency Updated"}

        updated_frequency = mock_db.add.call_args[0][0]
        assert updated_frequency.frequencyId == frequency_id
        assert updated_frequency.serviceFrequency == updated_frequency_data["serviceFrequency"]


def test_delete_frequency():
    frequency_id = 1

    with MagicMock() as mock_db:
        app.dependency_overrides[get_db] = lambda: mock_db
        mock_db.get.return_value = Frequency(frequencyId=frequency_id)
        response = client.delete(f"/frequency/{frequency_id}")

        assert response.status_code == 200
        assert response.json() == {"detail": "Frequency Deleted"}

        mock_db.delete.assert_called_once()
        mock_db.commit.assert_called_once()


# *** SERVICE AREA ***

def test_get_service_area():
    with MagicMock() as mock_db:
        mock_db.exec.return_value.all.return_value = [
            ServiceArea(serviceAreaId=1, townServiced="Gooding"),
            ServiceArea(serviceAreaId=2, townServiced="Jerome"),
        ]
        
        app.dependency_overrides[get_db] = lambda: mock_db
        response = client.get("/servicearea")
        assert response.status_code == 200

        expected_response = [
            {"serviceAreaId": 1, "townServiced": "Gooding"},
            {"serviceAreaId": 2, "townServiced": "Jerome"},
        ]
        assert response.json() == expected_response

def test_create_service_area():
    service_area_data = {
        "townServiced": "Jerome"
    }

    with MagicMock() as mock_db:
        app.dependency_overrides[get_db] = lambda: mock_db
        response = client.post("/servicearea", json=service_area_data)

        assert response.status_code == 201
        assert response.json() == {"detail": "Service Area Created"}

        created_service_area = mock_db.add.call_args[0][0]
        assert created_service_area.townServiced == service_area_data["townServiced"]


def test_delete_service_area():
    service_area_id = 1

    with MagicMock() as mock_db:
        app.dependency_overrides[get_db] = lambda: mock_db
        mock_db.get.return_value = ServiceArea(serviceAreaId=service_area_id)
        response = client.delete(f"/servicearea/{service_area_id}")

        assert response.status_code == 200
        assert response.json() == {"detail": "Service Area Deleted"}

        deleted_service_area = mock_db.delete.call_args[0][0]
        assert deleted_service_area.serviceAreaId == service_area_id


# *** CUSTOMER ***


def test_create_customer():
    customer_data = {
        "fName": "Bob",
        "lName": "Johnson",
        "phoneNumber": "123-456-7890",
        "email": "bob@email.com",
        "billingAddress": "123 Apple St",
        "physicalAddress": "123 Apple St",
        "lastPaymentDate": "2025-05-05",
        "lastServiceDate": "2025-04-30",
        "isResidential": True,
        "comments": "New customer",
    }

    with MagicMock() as mock_db:
        app.dependency_overrides[get_db] = lambda: mock_db
        response = client.post("/customer", json=customer_data)

        assert response.status_code == 201
        assert response.json() == {"detail": "Customer Created"}

        created_customer = mock_db.add.call_args[0][0]
        assert created_customer.fName == customer_data["fName"]
        assert created_customer.lName == customer_data["lName"]
        assert created_customer.phoneNumber == customer_data["phoneNumber"]
        assert created_customer.email == customer_data["email"]
        assert created_customer.billingAddress == customer_data["billingAddress"]
        assert created_customer.physicalAddress == customer_data["physicalAddress"]
        assert created_customer.lastPaymentDate == customer_data["lastPaymentDate"]
        assert created_customer.lastServiceDate == customer_data["lastServiceDate"]
        assert created_customer.isResidential == customer_data["isResidential"]
        assert created_customer.comments == customer_data["comments"]


# *** EMPLOYEE ***


def test_create_employee():
    employee_data = {
        "fName": "Bob",
        "lName": "Johnson",
        "birthDate": "2000-01-01",
        "phoneNumber": "123-456-7890",
        "email": "bob@example.com",
        "address": "123 Apple St",
        "laborRate": 20.0,
        "weeklyHours": 40.0
    }

    with MagicMock() as mock_db:
        app.dependency_overrides[get_db] = lambda: mock_db
        response = client.post("/employee", json=employee_data)

        assert response.status_code == 201
        assert response.json() == {"detail": "Employee Created"}

        created_employee = mock_db.add.call_args[0][0]
        assert created_employee.fName == employee_data["fName"]
        assert created_employee.lName == employee_data["lName"]
        assert created_employee.birthDate == employee_data["birthDate"]
        assert created_employee.phoneNumber == employee_data["phoneNumber"]
        assert created_employee.email == employee_data["email"]
        assert created_employee.address == employee_data["address"]
        assert created_employee.laborRate == employee_data["laborRate"]
        assert created_employee.weeklyHours == employee_data["weeklyHours"]


def test_update_employee():
    emp_id = 10
    updated_employee_data = {
        "fName": "Bob",
        "lName": "Johnson",
        "phoneNumber": "987-654-3210",
        "email": "bob@email.com",
        "birthDate": "2000-01-01",
        "address": "123 Apple St",
        "laborRate": 20.5,
        "weeklyHours": 40.0,
    }

    with MagicMock() as mock_db:
        app.dependency_overrides[get_db] = lambda: mock_db
        mock_db.get.return_value = Employee(**updated_employee_data)
        response = client.put(f"/employee/{emp_id}", json=updated_employee_data)

        assert response.status_code == 201
        assert response.json() == {"detail": "Employee Updated"}


def test_delete_employee():
    emp_id = 1

    with MagicMock() as mock_db:
        app.dependency_overrides[get_db] = lambda: mock_db
        mock_db.get.return_value = Employee(empId=emp_id)
        response = client.delete(f"/employee/{emp_id}")

        assert response.status_code == 200
        assert response.json() == {"detail": "Employee Deleted"}


# *** USER ***


def test_get_user():
    user_data = [
        User(userId=1, email="user1@example.com", empId=1, customerId=None, password="password1"),
        User(userId=2, email="user2@example.com", empId=None, customerId=2, password="password2"),
    ]

    with MagicMock() as mock_db:
        mock_db.exec.return_value.all.return_value = user_data
        app.dependency_overrides[get_db] = lambda: mock_db
        response = client.get("/user")

        assert response.status_code == 200
        assert response.json() == [
            {"userId": 1, "email": "user1@example.com", "empId": 1, "customerId": None, "password": "password1"},
            {"userId": 2, "email": "user2@example.com", "empId": None, "customerId": 2, "password": "password2"},
        ]

def test_create_user():
    user_data = {
        "email": "test@example.com",
        "empId": 1000,
        "customerId": 1000,
        "password": "password123",
    }

    with MagicMock() as mock_db:
        app.dependency_overrides[get_db] = lambda: mock_db
        response = client.post("/user", json=user_data)

        assert response.status_code == 201
        assert response.json() == {"detail": "User Created"}

        created_user = mock_db.add.call_args[0][0]
        assert created_user.email == user_data["email"]
        assert created_user.empId == user_data["empId"]
        assert created_user.customerId == user_data["customerId"]
        assert created_user.password == user_data["password"]


def test_delete_user():
    user_id = 1
    with MagicMock() as mock_db:
        app.dependency_overrides[get_db] = lambda: mock_db
        mock_db.get.return_value = User(userId=user_id, email="user@example.com", empId=None, customerId=1, password="password")
        response = client.delete(f"/user/{user_id}")

        assert response.status_code == 200
        assert response.json() == {"detail": "User Deleted"}

        mock_db.delete.assert_called_once()
        mock_db.commit.assert_called_once()


# *** INVOICE ***


def test_create_invoice():
    invoice_data = {
        "lotSize": "Large",
        "invoiceDate": "2025-05-10",
        "dueDate": "2025-05-17",
        "emailStatus": True,
        "productsUsed": "Product A, Product B",
        "acceptedBy": "John Doe",
        "applyTax": True,
        "taxAmount": 10.0,
        "totalEstimate": 100.0,
        "paid": False,
    }

    with MagicMock() as mock_db:
        app.dependency_overrides[get_db] = lambda: mock_db
        response = client.post("/invoice", json=invoice_data)

        assert response.status_code == 201
        assert response.json() == {"detail": "Invoice Created"}

        created_invoice = mock_db.add.call_args[0][0]
        assert created_invoice.lotSize == invoice_data["lotSize"]
        assert created_invoice.invoiceDate == invoice_data["invoiceDate"]
        assert created_invoice.dueDate == invoice_data["dueDate"]
        assert created_invoice.emailStatus == invoice_data["emailStatus"]
        assert created_invoice.productsUsed == invoice_data["productsUsed"]
        assert created_invoice.acceptedBy == invoice_data["acceptedBy"]
        assert created_invoice.applyTax == invoice_data["applyTax"]
        assert created_invoice.taxAmount == invoice_data["taxAmount"]
        assert created_invoice.totalEstimate == invoice_data["totalEstimate"]
        assert created_invoice.paid == invoice_data["paid"]


def test_update_invoice():
    updated_invoice_data = {
        "invoiceId": 1,
        "lotSize": "Large",
        "invoiceDate": "2024-05-10",
        "dueDate": "2024-05-25",
        "emailStatus": False,
        "productsUsed": "Product X, Product Y",
        "acceptedBy": "Alice Johnson",
        "applyTax": True,
        "taxAmount": 15.0,
        "totalEstimate": 200.0,
        "paid": True
    }

    with MagicMock() as mock_db:
        app.dependency_overrides[get_db] = lambda: mock_db
        mock_db.get.return_value = Invoice(**updated_invoice_data)
        response = client.put(f"/invoice/{updated_invoice_data['invoiceId']}", json=updated_invoice_data)

        assert response.status_code == 201
        assert response.json() == {"detail": "Invoice Updated"}


def test_delete_invoice():
    invoice_id = 1
    with MagicMock() as mock_db:
        app.dependency_overrides[get_db] = lambda: mock_db
        mock_db.get.return_value = Invoice(invoiceId=invoice_id)
        response = client.delete(f"/invoice/{invoice_id}")
        
        assert response.status_code == 200
        assert response.json() == {"detail": "Invoice Deleted"}


# *** EXPENSE ***


def test_create_expense():
    expense_data = {
        "expenseDate": "2024-05-03",
        "store": "Home Depot",
        "itemsPurchased": "Chainsaw fuel",
        "totalAmount": "200.00",
        "reason": "ran out of fuel",
    }

    with MagicMock() as mock_db:
        app.dependency_overrides[get_db] = lambda: mock_db
        response = client.post("/expense", json=expense_data)

        assert response.status_code == 201
        assert response.json() == {"detail": "Expense Created"}

        created_expense = mock_db.add.call_args[0][0]
        assert created_expense.expenseDate == expense_data["expenseDate"]
        assert created_expense.store == expense_data["store"]
        assert created_expense.itemsPurchased == expense_data["itemsPurchased"]
        assert created_expense.totalAmount == expense_data["totalAmount"]
        assert created_expense.reason == expense_data["reason"]


def test_update_expense():
    expense_id = 1
    updated_expense_data = {
        "expenseDate": "2024-05-03",
        "store": "Home Depot",
        "itemsPurchased": "Chainsaw fuel",
        "totalAmount": "200.00",
        "reason": "ran out of fuel",
    }

    with MagicMock() as mock_db:
        app.dependency_overrides[get_db] = lambda: mock_db
        response = client.put(f"/expense/{expense_id}", json=updated_expense_data)

        assert response.status_code == 201
        assert response.json() == {"detail": "Expense Updated"}

        existing_expense = mock_db.get.return_value
        for key, value in updated_expense_data.items():
            assert getattr(existing_expense, key) == value


def test_delete_expense():
    expense_id = 1

    with MagicMock() as mock_db:
        app.dependency_overrides[get_db] = lambda: mock_db
        mock_db.get.return_value = Expense(invoiceId=expense_id)
        response = client.delete(f"/expense/{expense_id}")

        assert response.status_code == 200
        assert response.json() == {"detail": "Expense Deleted"}


# *** JOB ***


def test_create_job():
    job_data = {
        "arrivalWindow": "08:00-10:00",
        "clockIn": "08:15",
        "clockOut": "10:00",
        "employeeId": 1,
        "payment": True,
        "isActive": True,
    }

    with MagicMock() as mock_db:
        app.dependency_overrides[get_db] = lambda: mock_db
        response = client.post("/job", json=job_data)

        assert response.status_code == 201
        assert response.json() == {"detail": "Job Created"}

        created_job = mock_db.add.call_args[0][0]
        assert created_job.arrivalWindow == job_data["arrivalWindow"]
        assert created_job.clockIn == job_data["clockIn"]
        assert created_job.clockOut == job_data["clockOut"]
        assert created_job.employeeId == job_data["employeeId"]
        assert created_job.payment == job_data["payment"]
        assert created_job.isActive == job_data["isActive"]


############################
# *** SQUARE PAYMENTS ***
############################


# *** list_payments ***

@patch('main.requests.get')
def test_list_payments(mock_get):
    mock_response = {
        'payments': [
            {'id': "N660Kal63Svrcev0BFhBDclL9lNZY", 'amount': 100},
            {'id': "TTNksUg2Y2xZiTI0UYJqBIrPFWNZY", 'amount': 200}
        ]
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    response = client.get("/payments")

    assert response.status_code == 200
    assert response.json() == mock_response['payments']

@patch('main.requests.get')
def test_list_payments_error(mock_get):

    mock_get.return_value.status_code = 404
    mock_get.return_value.text = "Payment not found"

    response = client.get("/payments")

    assert response.status_code == 404
    assert response.json() == {"detail": "Payment not found"}
