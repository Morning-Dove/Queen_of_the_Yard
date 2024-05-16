from sqlmodel import Field, Relationship, SQLModel

class ServiceLink(SQLModel, table=True):
    serviceId: int = Field(foreign_key="services.serviceId", primary_key=True)
    invoiceId: int = Field(foreign_key="invoice.invoiceId", primary_key=True)
    customerId: int = Field(foreign_key="customer.customerId", primary_key=True)
    jobId: int = Field(foreign_key="job.jobId", primary_key=True)


class CustomerJobsLink(SQLModel, table=True):
    customerId: int = Field(foreign_key="customer.customerId", primary_key=True)
    jobId: int = Field(foreign_key="job.jobId", primary_key=True)

class CustomerFrequencyLink(SQLModel, table=True):
    frequencyId: int = Field(foreign_key="frequency.frequencyId", primary_key=True)
    customerId: int = Field(foreign_key="customer.customerId", primary_key=True)


class Services(SQLModel, table=True):
    serviceId: int | None = Field(default=None, primary_key=True)
    service: str
    # invoiceId: int | None = Field(default=None, foreign_key="invoice.invoiceId")
    # invoice: 'Invoice' = Relationship(back_populates="servicesProvided")
    invoice: 'Invoice' = Relationship(back_populates="servicesProvided", link_model=ServiceLink)
    #customerId: int | None = Field(default=None, foreign_key="customer.customerId")
    customer: 'Customer' = Relationship(back_populates="servicesProvided", link_model=ServiceLink)
    #jobId: int | None = Field(default=None,foreign_key="job.jobId")
    job: 'Job' = Relationship(back_populates="servicesProvided", link_model=ServiceLink)


class Frequency(SQLModel, table=True):
    frequencyId: int | None = Field(default=None, primary_key=True)
    serviceFrequency: str
    #customerId: int | None = Field(default=None, foreign_key="customer.customerId")
    customer: 'Customer' = Relationship(back_populates="frequency", link_model=CustomerFrequencyLink)


# class AccountType(SQLModel, table=True):
#     accountTypeId: int | None = Field(default=None, primary_key=True)
#     isResidential: bool
#     isCommercial: bool
#     jobId: int | None = Field(default=None, foreign_key="job.jobId")
#     job: 'Job' = Relationship(back_populates="resOrCom")
#     customerId: int = Field(default=None, foreign_key="customer.customerId")
#     customer: 'Customer' = Relationship(back_populates="resOrComm")


class ServiceArea(SQLModel, table=True):
    serviceAreaId: int | None = Field(default=None, primary_key=True)
    townServiced: str
    # jobId: int | None = Field(default=None, foreign_key="job.jobId")
    # job: 'Job' = Relationship(back_populates="serviceTown")
    customerId: int | None = Field(default=None, foreign_key="customer.customerId")
    customer: 'Customer' = Relationship(back_populates="city")


class User(SQLModel, table=True):
    userId: int | None = Field(default=None, primary_key=True)
    email: str
    empId: int | None = Field(default=None, foreign_key="employee.empId")
    customerId: int | None = Field(default=None, foreign_key="customer.customerId")
    password: str


class Invoice(SQLModel, table=True):
    invoiceId: int = Field(default=None, primary_key=True)
    #customerId: int = Field(foreign_key="customer.customerId")
    #customer: 'Customer' = Relationship(back_populates="invoices")
    lotSize: str
    servicesProvided: list[Services] = Relationship(back_populates="invoice", link_model=ServiceLink)
    invoiceDate: str
    dueDate: str
    emailStatus: bool
    productsUsed: str
    acceptedBy: str
    applyTax: bool
    taxAmount: float
    totalEstimate: float
    paid: bool
    #jobId: int | None = Field(default=None, foreign_key="job.jobId")
    job: 'Job' = Relationship(back_populates="invoice")
    # many to one - many invoices can be associated to one customer
    

class Customer(SQLModel, table=True):
    customerId: int | None = Field(default=None, primary_key=True)
    #jobId: int | None = Field(default=None, foreign_key="job.jobId")
    jobs: list['Job'] = Relationship(back_populates="customer", link_model=CustomerJobsLink)
    fName: str
    lName: str
    phoneNumber: str
    email: str
    billingAddress: str
    physicalAddress: str
    lastPaymentDate: str
    lastServiceDate: str
    city: ServiceArea = Relationship(back_populates="customer")
    servicesProvided: list[Services] = Relationship(back_populates="customer", link_model=ServiceLink)
    isResidential: bool
    # resOrComm: AccountType = Relationship(back_populates="customer")
    comments: str
    #invoices: list[Invoice] = Relationship(back_populates="customer")
    #invoiceId: int | None = Field(default=None, foreign_key="invoice.invoiceId")
    frequency: Frequency = Relationship(back_populates="customer", link_model=CustomerFrequencyLink)



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
    # serviceTown: ServiceArea = Relationship(back_populates="job")
    # resOrCom : AccountType = Relationship(back_populates="job")
    payment: bool
    isActive: bool
    comments: str
    extraExpenses: list[Expense] = Relationship(back_populates="job")
    invoiceId: int | None = Field(default=None, foreign_key="invoice.invoiceId")
    invoice: Invoice = Relationship(back_populates="job")
    #customerId: int = Field(default=None, foreign_key="customer.customerId")
    customer: Customer = Relationship(back_populates="jobs", link_model=CustomerJobsLink)