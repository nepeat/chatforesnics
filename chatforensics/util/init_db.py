#!/usr/bin/python
import os

from alembic.config import Config
from alembic import command
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.orm.exc import NoResultFound

from chatforensics.model import Base, engine, sm, ChatUser
from chatforensics.model.types import BackendType

def init_db():
    print(os.path.dirname(os.path.realpath(__file__)) + "/../../alembic.ini")

    inspector = Inspector.from_engine(engine)
    if "alembic_version" in inspector.get_table_names():
        raise Exception("Database has already been initialised. Use \"alembic upgrade head\" instead.")

    engine.echo = True
    Base.metadata.create_all(bind=engine)

    alembic_cfg = Config(os.path.dirname(os.path.realpath(__file__)) + "/../../alembic.ini")
    command.stamp(alembic_cfg, "head")

    # Create self user
    db = sm()
    db.add(ChatUser(
        backend_type=BackendType.internal,
        backend_uid="self",
        friendly_name="Self"
    ))
    db.commit()

if __name__ == "__main__":
    init_db()
