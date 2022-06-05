from databases import Database
import sqlalchemy as sa

from environment import settings

database = Database(settings.db_url)
metadata = sa.MetaData()
