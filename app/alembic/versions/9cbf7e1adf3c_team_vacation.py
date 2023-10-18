"""team_vacation

Revision ID: 9cbf7e1adf3c
Revises: 27bf2aa3b8c7
Create Date: 2023-10-18 11:36:03.830422

"""
from uuid import uuid4

import sqlalchemy as sa
from alembic import op

from app.model.base import CustomUUID

# revision identifiers, used by Alembic.
revision = '9cbf7e1adf3c'
down_revision = '27bf2aa3b8c7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('team',
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('id', CustomUUID(), nullable=False, default=uuid4()),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_team_id'), 'team', ['id'], unique=False)
    op.create_table('vacation',
        sa.Column('employee_id', sa.UUID(), nullable=False),
        sa.Column('start_date', sa.DateTime(), nullable=False),
        sa.Column('end_date', sa.DateTime(), nullable=False),
        sa.Column('type', sa.Enum('paid', 'unpaid', name='vacationtypeenum'), nullable=False),
        sa.Column('id', CustomUUID(), nullable=False),
        sa.ForeignKeyConstraint(['employee_id'], ['employee.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_vacation_employee_id'), 'vacation', ['employee_id'], unique=False)
    op.create_index(op.f('ix_vacation_id'), 'vacation', ['id'], unique=False)
    op.add_column('employee', sa.Column('team_id', sa.UUID(), nullable=False))
    op.create_foreign_key(None, 'employee', 'team', ['team_id'], ['id'])


def downgrade():
    op.drop_constraint(None, 'employee', type_='foreignkey')
    op.drop_column('employee', 'team_id')
    op.drop_index(op.f('ix_vacation_id'), table_name='vacation')
    op.drop_index(op.f('ix_vacation_employee_id'), table_name='vacation')
    op.drop_table('vacation')
    op.drop_index(op.f('ix_team_id'), table_name='team')
    op.drop_table('team')
