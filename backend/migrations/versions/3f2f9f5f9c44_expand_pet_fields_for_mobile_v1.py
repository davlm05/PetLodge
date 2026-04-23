"""Expand pet fields for mobile v1

Revision ID: 3f2f9f5f9c44
Revises: 01caa8f69935
Create Date: 2026-04-11 16:20:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3f2f9f5f9c44"
down_revision = "01caa8f69935"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("pets", schema=None) as batch_op:
        batch_op.add_column(sa.Column("sex", sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column("size", sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column("vaccinated", sa.Boolean(), nullable=True))
        batch_op.add_column(
            sa.Column("vaccination_notes", sa.Text(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("has_medical_conditions", sa.Boolean(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("medical_conditions_notes", sa.Text(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("veterinarian_name", sa.String(length=150), nullable=True)
        )
        batch_op.add_column(
            sa.Column("veterinarian_phone", sa.String(length=20), nullable=True)
        )

    op.execute(
        sa.text(
            """
            UPDATE pets
            SET has_medical_conditions = CASE
                WHEN medical_notes IS NOT NULL AND TRIM(medical_notes) <> '' THEN TRUE
                ELSE FALSE
            END,
            medical_conditions_notes = medical_notes
            """
        )
    )

    with op.batch_alter_table("pets", schema=None) as batch_op:
        batch_op.drop_column("weight_kg")
        batch_op.drop_column("medical_notes")


def downgrade():
    with op.batch_alter_table("pets", schema=None) as batch_op:
        batch_op.add_column(sa.Column("medical_notes", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("weight_kg", sa.Float(), nullable=True))

    op.execute(
        sa.text(
            """
            UPDATE pets
            SET medical_notes = CASE
                WHEN medical_conditions_notes IS NOT NULL AND TRIM(medical_conditions_notes) <> ''
                    THEN medical_conditions_notes
                ELSE NULL
            END
            """
        )
    )

    with op.batch_alter_table("pets", schema=None) as batch_op:
        batch_op.drop_column("veterinarian_phone")
        batch_op.drop_column("veterinarian_name")
        batch_op.drop_column("medical_conditions_notes")
        batch_op.drop_column("has_medical_conditions")
        batch_op.drop_column("vaccination_notes")
        batch_op.drop_column("vaccinated")
        batch_op.drop_column("size")
        batch_op.drop_column("sex")
