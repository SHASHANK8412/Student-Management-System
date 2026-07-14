"""add student identity fields

Revision ID: 0002_add_student_identity_fields
Revises: 0001_initial
Create Date: 2026-07-11
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision = "0002_add_student_identity_fields"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    existing_columns = {column["name"] for column in inspector.get_columns("students")}
    existing_indexes = {index["name"] for index in inspector.get_indexes("students")}

    columns_to_add = [
        ("parent_name", sa.String(length=200)),
        ("aadhar_number", sa.String(length=20)),
        ("pen_number", sa.String(length=30)),
        ("caste", sa.String(length=100)),
        ("sub_caste", sa.String(length=100)),
    ]

    for column_name, column_type in columns_to_add:
        if column_name not in existing_columns:
            op.add_column("students", sa.Column(column_name, column_type, nullable=True))

    indexes_to_add = [
        (op.f("ix_students_parent_name"), ["parent_name"]),
        (op.f("ix_students_aadhar_number"), ["aadhar_number"]),
        (op.f("ix_students_pen_number"), ["pen_number"]),
        (op.f("ix_students_caste"), ["caste"]),
        (op.f("ix_students_sub_caste"), ["sub_caste"]),
    ]

    for index_name, index_columns in indexes_to_add:
        if index_name not in existing_indexes:
            op.create_index(index_name, "students", index_columns, unique=False)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    existing_columns = {column["name"] for column in inspector.get_columns("students")}
    existing_indexes = {index["name"] for index in inspector.get_indexes("students")}

    indexes_to_drop = [
        op.f("ix_students_sub_caste"),
        op.f("ix_students_caste"),
        op.f("ix_students_pen_number"),
        op.f("ix_students_aadhar_number"),
        op.f("ix_students_parent_name"),
    ]
    for index_name in indexes_to_drop:
        if index_name in existing_indexes:
            op.drop_index(index_name, table_name="students")

    columns_to_drop = ["sub_caste", "caste", "pen_number", "aadhar_number", "parent_name"]
    for column_name in columns_to_drop:
        if column_name in existing_columns:
            op.drop_column("students", column_name)