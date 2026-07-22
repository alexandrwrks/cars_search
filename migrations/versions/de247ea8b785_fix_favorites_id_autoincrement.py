"""fix favorites id autoincrement

Revision ID: de247ea8b785
Revises: dd4ddf4ad9a6
Create Date: 2026-07-21 20:38:43.934806

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'de247ea8b785'
down_revision: Union[str, Sequence[str], None] = 'dd4ddf4ad9a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
            CREATE SEQUENCE IF NOT EXISTS favorites_id_seq;
        """)

    op.execute("""
            ALTER TABLE favorites
            ALTER COLUMN id
            SET DEFAULT nextval('favorites_id_seq');
        """)

    op.execute("""
            SELECT setval(
                'favorites_id_seq',
                COALESCE((SELECT MAX(id) FROM favorites), 1)
            );
        """)
    op.drop_constraint(
        "favorites_car_id_fkey",
        "favorites",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "favorites_car_id_fkey",
        "favorites",
        "cars",
        ["car_id"],      # столбец в favorites
        ["car_id"],      # столбец в cars
    )

def downgrade():
    op.execute("""
           ALTER TABLE favorites
           ALTER COLUMN id
           DROP DEFAULT;
       """)

    op.execute("""
           DROP SEQUENCE IF EXISTS favorites_id_seq;
       """)
    op.drop_constraint(
        "favorites_car_id_fkey",
        "favorites",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "favorites_car_id_fkey",
        "favorites",
        "cars",
        ["car_id"],
        ["id"],
    )
