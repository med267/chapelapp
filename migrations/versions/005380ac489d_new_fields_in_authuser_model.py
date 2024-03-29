"""new fields in AuthUser model

Revision ID: 005380ac489d
Revises: d75436453c95
Create Date: 2019-07-06 02:29:10.877050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '005380ac489d'
down_revision = 'd75436453c95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('authuser', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('authuser', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('authuser', 'last_seen')
    op.drop_column('authuser', 'about_me')
    # ### end Alembic commands ###
