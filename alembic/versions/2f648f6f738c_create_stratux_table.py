"""create traffic table

Revision ID: 2f648f6f738c
Revises: 
Create Date: 2018-04-25 20:54:56.571121

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '2f648f6f738c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # {
    #   "Icao_addr": 1065986,
    #   "Reg": "",
    #   "Tail": "",
    #   "Emitter_category": 0,
    #   "OnGround": true,
    #   "Addr_type": 4,
    #   "TargetType": 0,
    #   "SignalLevel": -43.09803919971486,
    #   "Squawk": 0,
    #   "Position_valid": true,
    #   "Lat": -89.64273,
    #   "Lng": 4.265485,
    #   "Alt": 35850,
    #   "GnssDiffFromBaroAlt": 0,
    #   "AltIsGNSS": false,
    #   "NIC": 8,
    #   "NACp": 0,
    #   "Track": 0,
    #   "Speed": 357,
    #   "Speed_valid": true,
    #   "Vvel": 0,
    #   "Timestamp": "2016-02-27T22:52:53.910258947Z",
    #   "PriorityStatus": 0,
    #   "Age": 0,
    #   "AgeLastAlt": 0,
    #   "Last_seen": "0001-01-01T23:29:11.63Z",
    #   "Last_alt": "0001-01-01T23:29:11.63Z",
    #   "Last_GnssDiff": "0001-01-01T00:00:00Z",
    #   "Last_GnssDiffAlt": 0,
    #   "Last_speed": "0001-01-01T23:29:11.63Z",
    #   "Last_source": 2,
    #   "ExtrapolatedPosition": false,
    #   "BearingDist_valid": false,
    #   "Bearing": 0,
    #   "Distance": 0
    # }

    op.create_table(
        'traffic',
        sa.Column('id', UUID, primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column('icao_addr', sa.String, nullable=True),
        sa.Column('reg', sa.String, nullable=True),
        sa.Column('tail', sa.String, nullable=True),
        sa.Column('emitter_category', sa.Integer, nullable=True),
        sa.Column('onground', sa.Boolean, nullable=True),
        sa.Column('addr_type', sa.Integer, nullable=True),
        sa.Column('targettype', sa.Integer, nullable=True),
        sa.Column('signallevel', sa.Float, nullable=True),
        sa.Column('squawk', sa.Integer, nullable=True),
        sa.Column('position_valid', sa.Boolean, nullable=True),
        sa.Column('lat', sa.Float, nullable=True),
        sa.Column('lng', sa.Float, nullable=True),
        sa.Column('alt', sa.Integer, nullable=True),
        sa.Column('gnssdifffrombaroalt', sa.Integer, nullable=True),
        sa.Column('altisgnss', sa.String, nullable=True),
        sa.Column('nic', sa.Integer, nullable=True),
        sa.Column('nacp', sa.Integer, nullable=True),
        sa.Column('track', sa.Integer, nullable=True),
        sa.Column('speed', sa.Integer, nullable=True),
        sa.Column('speed_valid', sa.Boolean, nullable=True),
        sa.Column('vvel', sa.Float, nullable=True),
        sa.Column('timestamp', sa.DateTime, nullable=True),
        sa.Column('prioritystatus', sa.Boolean, nullable=True),
        sa.Column('age', sa.Float, nullable=True),
        sa.Column('agelastalt', sa.Float, nullable=True),
        sa.Column('last_seen', sa.DateTime, nullable=True),
        sa.Column('last_alt', sa.DateTime, nullable=True),
        sa.Column('last_gnssdiff', sa.DateTime, nullable=True),
        sa.Column('last_gnssdiffalt', sa.Integer, nullable=True),
        sa.Column('last_speed', sa.DateTime, nullable=True),
        sa.Column('last_source', sa.Integer, nullable=True),
        sa.Column('extrapolatedposition', sa.Boolean, nullable=True),
        sa.Column('bearingdist_valid', sa.Boolean, nullable=True),
        sa.Column('bearing', sa.Integer, nullable=True),
        sa.Column('distance', sa.Integer, nullable=True)
    )


def downgrade():
    op.drop_table('traffic')
