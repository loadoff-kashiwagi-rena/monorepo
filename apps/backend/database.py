from sqlalchemy import create_engine, event

engine = create_engine("sqlite:///./app.db", echo=True)

@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
  cursor = dbapi_connection.cursor()
  cursor.execute("PRAGMA foreign_keys=ON")
  cursor.close()