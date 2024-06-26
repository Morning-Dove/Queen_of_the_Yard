"""Add customerservicearealink

Revision ID: f63f50ba53d1
Revises: 
Create Date: 2024-05-16 12:04:46.677585

"""
from typing import Sequence

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'f63f50ba53d1'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer',
    sa.Column('customerId', sa.Integer(), nullable=False),
    sa.Column('fName', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('lName', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('phoneNumber', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('billingAddress', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('physicalAddress', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('lastPaymentDate', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('lastServiceDate', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('isResidential', sa.Boolean(), nullable=False),
    sa.Column('comments', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('customerId')
    )
    op.create_table('employee',
    sa.Column('empId', sa.Integer(), nullable=False),
    sa.Column('fName', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('lName', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('birthDate', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('phoneNumber', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('address', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('laborRate', sa.Float(), nullable=False),
    sa.Column('weeklyHours', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('empId')
    )
    op.create_table('frequency',
    sa.Column('frequencyId', sa.Integer(), nullable=False),
    sa.Column('serviceFrequency', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('frequencyId')
    )
    op.create_table('invoice',
    sa.Column('invoiceId', sa.Integer(), nullable=False),
    sa.Column('lotSize', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('invoiceDate', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('dueDate', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('emailStatus', sa.Boolean(), nullable=False),
    sa.Column('productsUsed', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('acceptedBy', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('applyTax', sa.Boolean(), nullable=False),
    sa.Column('taxAmount', sa.Float(), nullable=False),
    sa.Column('totalEstimate', sa.Float(), nullable=False),
    sa.Column('paid', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('invoiceId')
    )
    op.create_table('servicearea',
    sa.Column('serviceAreaId', sa.Integer(), nullable=False),
    sa.Column('townServiced', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('serviceAreaId')
    )
    op.create_table('services',
    sa.Column('serviceId', sa.Integer(), nullable=False),
    sa.Column('service', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('serviceId')
    )
    op.create_table('customerfrequencylink',
    sa.Column('frequencyId', sa.Integer(), nullable=False),
    sa.Column('customerId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['customerId'], ['customer.customerId'], ),
    sa.ForeignKeyConstraint(['frequencyId'], ['frequency.frequencyId'], ),
    sa.PrimaryKeyConstraint('frequencyId', 'customerId')
    )
    op.create_table('customerservicearealink',
    sa.Column('customerId', sa.Integer(), nullable=False),
    sa.Column('serviceAreaId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['customerId'], ['customer.customerId'], ),
    sa.ForeignKeyConstraint(['serviceAreaId'], ['servicearea.serviceAreaId'], ),
    sa.PrimaryKeyConstraint('customerId', 'serviceAreaId')
    )
    op.create_table('job',
    sa.Column('jobId', sa.Integer(), nullable=False),
    sa.Column('arrivalWindow', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('clockIn', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('clockOut', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('employeeId', sa.Integer(), nullable=False),
    sa.Column('payment', sa.Boolean(), nullable=False),
    sa.Column('isActive', sa.Boolean(), nullable=False),
    sa.Column('comments', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('invoiceId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['employeeId'], ['employee.empId'], ),
    sa.ForeignKeyConstraint(['invoiceId'], ['invoice.invoiceId'], ),
    sa.PrimaryKeyConstraint('jobId')
    )
    op.create_table('user',
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('empId', sa.Integer(), nullable=True),
    sa.Column('customerId', sa.Integer(), nullable=True),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['customerId'], ['customer.customerId'], ),
    sa.ForeignKeyConstraint(['empId'], ['employee.empId'], ),
    sa.PrimaryKeyConstraint('userId')
    )
    op.create_table('customerjobslink',
    sa.Column('customerId', sa.Integer(), nullable=False),
    sa.Column('jobId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['customerId'], ['customer.customerId'], ),
    sa.ForeignKeyConstraint(['jobId'], ['job.jobId'], ),
    sa.PrimaryKeyConstraint('customerId', 'jobId')
    )
    op.create_table('expense',
    sa.Column('expenseId', sa.Integer(), nullable=False),
    sa.Column('expenseDate', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('store', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('itemsPurchased', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('totalAmount', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('reason', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('purchasedBy', sa.Integer(), nullable=False),
    sa.Column('linkedJob', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['linkedJob'], ['job.jobId'], ),
    sa.ForeignKeyConstraint(['purchasedBy'], ['employee.empId'], ),
    sa.PrimaryKeyConstraint('expenseId')
    )
    op.create_table('servicelink',
    sa.Column('serviceId', sa.Integer(), nullable=False),
    sa.Column('invoiceId', sa.Integer(), nullable=False),
    sa.Column('customerId', sa.Integer(), nullable=False),
    sa.Column('jobId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['customerId'], ['customer.customerId'], ),
    sa.ForeignKeyConstraint(['invoiceId'], ['invoice.invoiceId'], ),
    sa.ForeignKeyConstraint(['jobId'], ['job.jobId'], ),
    sa.ForeignKeyConstraint(['serviceId'], ['services.serviceId'], ),
    sa.PrimaryKeyConstraint('serviceId', 'invoiceId', 'customerId', 'jobId')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('servicelink')
    op.drop_table('expense')
    op.drop_table('customerjobslink')
    op.drop_table('user')
    op.drop_table('job')
    op.drop_table('customerservicearealink')
    op.drop_table('customerfrequencylink')
    op.drop_table('services')
    op.drop_table('servicearea')
    op.drop_table('invoice')
    op.drop_table('frequency')
    op.drop_table('employee')
    op.drop_table('customer')
    # ### end Alembic commands ###
