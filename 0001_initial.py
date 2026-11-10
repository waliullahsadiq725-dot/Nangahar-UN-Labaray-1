"""Initial NUDL schema."""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    user_role = sa.Enum("admin", "teacher", "student", name="user_role")
    account_status = sa.Enum("pending", "active", "suspended", name="account_status")
    user_role.create(op.get_bind(), checkfirst=True)
    account_status.create(op.get_bind(), checkfirst=True)
    op.create_table("faculties",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name_ps", sa.String(180), nullable=False),
        sa.Column("name_fa", sa.String(180), nullable=False),
        sa.Column("name_en", sa.String(180), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()))
    op.create_table("departments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("faculty_id", sa.Integer(), sa.ForeignKey("faculties.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name_ps", sa.String(180), nullable=False),
        sa.Column("name_fa", sa.String(180), nullable=False),
        sa.Column("name_en", sa.String(180), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()))
    op.create_index("ix_departments_faculty_id", "departments", ["faculty_id"])
    op.create_table("users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("full_name", sa.String(160), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", user_role, nullable=False, server_default="student"),
        sa.Column("status", account_status, nullable=False, server_default="pending"),
        sa.Column("faculty_id", sa.Integer(), nullable=True),
        sa.Column("department_id", sa.Integer(), nullable=True),
        sa.Column("student_number", sa.String(50), nullable=True),
        sa.Column("staff_number", sa.String(50), nullable=True),
        sa.Column("is_email_verified", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("email"), sa.UniqueConstraint("student_number"), sa.UniqueConstraint("staff_number"))
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_id", "users", ["id"])

def downgrade():
    op.drop_index("ix_users_id", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
    op.drop_index("ix_departments_faculty_id", table_name="departments")
    op.drop_table("departments")
    op.drop_table("faculties")
    sa.Enum(name="account_status").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="user_role").drop(op.get_bind(), checkfirst=True)
