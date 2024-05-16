from sqlmodel import Field, Relationship, SQLModel


class ServiceLink(SQLModel, table=True):
    serviceId: int = Field(foreign_key="services.serviceId", primary_key=True)
    jobId: int = Field(foreign_key="job.jobId", primary_key=True)


class CustomerServiceAreaLink(SQLModel, table=True):
    customerId: int = Field(foreign_key="customer.customerId", primary_key=True)
    serviceAreaId: int = Field(foreign_key="servicearea.serviceAreaId", primary_key=True)


class Services(SQLModel, table=True):
    serviceId: int | None = Field(default=None, primary_key=True)
    service: str
    job: 'Job' = Relationship(back_populates="servicesProvided", link_model=ServiceLink)


class Frequency(SQLModel, table=True):
    frequencyId: int | None = Field(default=None, primary_key=True)
    serviceFrequency: str
    customer: list['Customer'] = Relationship(back_populates="frequency")


class ServiceArea(SQLModel, table=True):
    serviceAreaId: int | None = Field(default=None, primary_key=True)
    townServiced: str
    customer: list['Customer'] = Relationship(back_populates="city", link_model=CustomerServiceAreaLink)


class User(SQLModel, table=True):
    userId: int | None = Field(default=None, primary_key=True)
    email: str
    empId: int | None = Field(default=None, foreign_key="employee.empId")
    customerId: int | None = Field(default=None, foreign_key="customer.customerId")
    password: str


class Invoice(SQLModel, table=True):
    invoiceId: int = Field(default=None, primary_key=True)
    lotSize: str
    invoiceDate: str
    dueDate: str
    emailStatus: bool
    productsUsed: str
    acceptedBy: str
    applyTax: bool
    taxAmount: float
    totalEstimate: float
    paid: bool
    job: 'Job' = Relationship(back_populates="invoice")
    # many to one - many invoices can be associated to one customer
    

class Customer(SQLModel, table=True):
    customerId: int | None = Field(default=None, primary_key=True)
    jobs: list['Job'] = Relationship(back_populates="customer")
    fName: str
    lName: str
    phoneNumber: str
    email: str
    billingAddress: str
    physicalAddress: str
    lastPaymentDate: str
    lastServiceDate: str
    city: list[ServiceArea] = Relationship(back_populates="customer", link_model=CustomerServiceAreaLink)
    isResidential: bool
    comments: str
    frequencyId: int | None = Field(default=None, foreign_key="frequency.frequencyId")
    frequency: Frequency = Relationship(back_populates="customer")


class Employee(SQLModel, table=True):
    empId: int | None = Field(default=None, primary_key=True)
    fName: str
    lName: str
    birthDate: str
    phoneNumber: str
    email: str
    address: str
    laborRate: float
    weeklyHours: float
    expenses: list['Expense'] = Relationship(back_populates="employee")


class Expense(SQLModel, table=True):
    expenseId: int | None = Field(default=None, primary_key=True)
    expenseDate: str
    store: str
    itemsPurchased: str
    totalAmount: str
    reason: str
    purchasedBy: int = Field(default=None, foreign_key="employee.empId")
    linkedJob: int | None = Field(default=None, foreign_key="job.jobId")
    job: 'Job' = Relationship(back_populates='extraExpenses')
    employee: Employee = Relationship(back_populates="expenses")
    # many to one - many expenses can be associated to one employee


class Job(SQLModel, table=True):
    jobId: int | None = Field(default=None, primary_key=True)
    arrivalWindow: str
    clockIn: str
    clockOut: str
    employeeId: int = Field(default=None, foreign_key="employee.empId")
    servicesProvided: list[Services] = Relationship(back_populates="job", link_model=ServiceLink)
    payment: bool
    isActive: bool
    comments: str
    extraExpenses: list[Expense] = Relationship(back_populates="job")
    invoiceId: int | None = Field(default=None, foreign_key="invoice.invoiceId")
    invoice: Invoice = Relationship(back_populates="job")
    customerId: int | None = Field(default=None, foreign_key="customer.customerId")
    customer: Customer = Relationship(back_populates="jobs")