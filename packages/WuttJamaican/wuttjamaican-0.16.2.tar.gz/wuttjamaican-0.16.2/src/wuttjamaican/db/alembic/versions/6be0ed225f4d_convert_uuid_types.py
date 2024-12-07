"""convert uuid types

Revision ID: 6be0ed225f4d
Revises: 6bf900765500
Create Date: 2024-11-30 17:03:08.930050

"""
import uuid as _uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import wuttjamaican.db.util


# revision identifiers, used by Alembic.
revision: str = '6be0ed225f4d'
down_revision: Union[str, None] = '6bf900765500'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # upgrade (convert uuid)
    op.add_column('upgrade', sa.Column('uuid_true', wuttjamaican.db.util.UUID(), nullable=True))
    upgrade = sa.sql.table('upgrade',
                           sa.sql.column('uuid'),
                           sa.sql.column('uuid_true'))

    engine = op.get_bind()
    cursor = engine.execute(upgrade.select())
    for row in cursor.fetchall():
        if row['uuid']:
            uuid_true = _uuid.UUID(row['uuid'])
            engine.execute(upgrade.update()\
                           .where(upgrade.c.uuid == row['uuid'])\
                           .values({'uuid_true': uuid_true}))

    op.drop_constraint('pk_upgrade', 'upgrade', type_='primary')
    op.drop_column('upgrade', 'uuid')
    op.alter_column('upgrade', 'uuid_true', new_column_name='uuid')
    op.create_primary_key('pk_upgrade', 'upgrade', ['uuid'])


def downgrade() -> None:

    # upgrade (convert uuid)
    op.add_column('upgrade', sa.Column('uuid_str', sa.VARCHAR(length=32), nullable=True))
    upgrade = sa.sql.table('upgrade',
                           sa.sql.column('uuid'),
                           sa.sql.column('uuid_str'))

    engine = op.get_bind()
    cursor = engine.execute(upgrade.select())
    for row in cursor.fetchall():
        if row['uuid']:
            uuid_str = row['uuid'].hex
            engine.execute(upgrade.update()\
                           .where(upgrade.c.uuid == row['uuid'])\
                           .values({'uuid_str': uuid_str}))

    op.drop_constraint('pk_upgrade', 'upgrade', type_='primary')
    op.drop_column('upgrade', 'uuid')
    op.alter_column('upgrade', 'uuid_str', new_column_name='uuid')
    op.create_primary_key('pk_upgrade', 'upgrade', ['uuid'])
