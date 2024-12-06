import datetime
import sys
from decimal import Decimal

import pytest
import pytest_mysql.factories
import pytest_postgresql.factories
import sqlalchemy.dialects.mysql as sa_mysql
import sqlalchemy.dialects.postgresql as sa_pg
import sqlalchemy.orm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass
from sqlalchemy.orm.exc import FlushError

from iker.common.utils.dbutils import ConnectionMaker
from iker.common.utils.dbutils import mysql_insert_ignore, postgresql_insert_on_conflict_do_nothing
from iker.common.utils.dbutils import orm_clone
from iker.common.utils.funcutils import unique_returns
from iker.common.utils.randutils import randomizer
from iker.common.utils.testutils import nested_approx

fixture_mysql_test_proc = pytest_mysql.factories.mysql_proc(host="localhost", user="root")
fixture_mysql_test = pytest_mysql.factories.mysql("fixture_mysql_test_proc", dbname="test")

fixture_postgresql_test_proc = pytest_postgresql.factories.postgresql_proc(host="localhost", user="postgres")
fixture_postgresql_test = pytest_postgresql.factories.postgresql("fixture_postgresql_test_proc", dbname="test")


class MysqlBaseModel(MappedAsDataclass, DeclarativeBase):
    pass


class PostgresqlBaseModel(MappedAsDataclass, DeclarativeBase):
    pass


class MysqlDummyRecord(MysqlBaseModel):
    __tablename__ = "mysql_dummy_record"

    dummy_id: Mapped[int] = sqlalchemy.orm.mapped_column(sa_mysql.BIGINT,
                                                         primary_key=True,
                                                         autoincrement=True,
                                                         index=True,
                                                         unique=True,
                                                         init=False)
    dummy_char: Mapped[str] = sqlalchemy.orm.mapped_column(sa_mysql.CHAR(31))
    dummy_varchar: Mapped[str] = sqlalchemy.orm.mapped_column(sa_mysql.VARCHAR(31))
    dummy_text: Mapped[str] = sqlalchemy.orm.mapped_column(sa_mysql.TEXT)
    dummy_boolean: Mapped[bool] = sqlalchemy.orm.mapped_column(sa_mysql.BOOLEAN)
    dummy_smallint: Mapped[int] = sqlalchemy.orm.mapped_column(sa_mysql.SMALLINT)
    dummy_integer: Mapped[int] = sqlalchemy.orm.mapped_column(sa_mysql.INTEGER)
    dummy_bigint: Mapped[int] = sqlalchemy.orm.mapped_column(sa_mysql.BIGINT)
    dummy_float: Mapped[float] = sqlalchemy.orm.mapped_column(sa_mysql.FLOAT)
    dummy_double: Mapped[Decimal] = sqlalchemy.orm.mapped_column(sa_mysql.DOUBLE)
    dummy_date: Mapped[datetime.date] = sqlalchemy.orm.mapped_column(sa_mysql.DATE)
    dummy_time: Mapped[datetime.time] = sqlalchemy.orm.mapped_column(sa_mysql.TIME)
    dummy_datetime: Mapped[datetime.datetime] = sqlalchemy.orm.mapped_column(sa_mysql.DATETIME)
    dummy_json: Mapped[object] = sqlalchemy.orm.mapped_column(sa_mysql.JSON)
    dummy_unique_string: Mapped[str] = sqlalchemy.orm.mapped_column(sa_mysql.VARCHAR(15), unique=True)

    __table_args__ = (
        sqlalchemy.Index("index_mysql_dummy_record",
                         dummy_boolean,
                         dummy_smallint,
                         dummy_integer,
                         dummy_bigint,
                         unique=True),
    )


class PostgresqlDummyRecord(PostgresqlBaseModel):
    __tablename__ = "postgresql_dummy_record"

    dummy_id: Mapped[int] = sqlalchemy.orm.mapped_column(sa_pg.BIGINT,
                                                         primary_key=True,
                                                         autoincrement=True,
                                                         index=True,
                                                         unique=True,
                                                         init=False)
    dummy_char: Mapped[str] = sqlalchemy.orm.mapped_column(sa_pg.CHAR(31))
    dummy_varchar: Mapped[str] = sqlalchemy.orm.mapped_column(sa_pg.VARCHAR(31))
    dummy_text: Mapped[str] = sqlalchemy.orm.mapped_column(sa_pg.TEXT)
    dummy_boolean: Mapped[bool] = sqlalchemy.orm.mapped_column(sa_pg.BOOLEAN)
    dummy_smallint: Mapped[int] = sqlalchemy.orm.mapped_column(sa_pg.SMALLINT)
    dummy_integer: Mapped[int] = sqlalchemy.orm.mapped_column(sa_pg.INTEGER)
    dummy_bigint: Mapped[int] = sqlalchemy.orm.mapped_column(sa_pg.BIGINT)
    dummy_float: Mapped[float] = sqlalchemy.orm.mapped_column(sa_pg.FLOAT)
    dummy_double_precision: Mapped[float] = sqlalchemy.orm.mapped_column(sa_pg.DOUBLE_PRECISION)
    dummy_date: Mapped[datetime.date] = sqlalchemy.orm.mapped_column(sa_pg.DATE)
    dummy_time: Mapped[datetime.time] = sqlalchemy.orm.mapped_column(sa_pg.TIME)
    dummy_time_tz: Mapped[datetime.time] = sqlalchemy.orm.mapped_column(sa_pg.TIME(timezone=True))
    dummy_timestamp: Mapped[datetime.datetime] = sqlalchemy.orm.mapped_column(sa_pg.TIMESTAMP)
    dummy_timestamp_tz: Mapped[datetime.datetime] = sqlalchemy.orm.mapped_column(sa_pg.TIMESTAMP(timezone=True))
    dummy_array_varchar: Mapped[list[str]] = sqlalchemy.orm.mapped_column(sa_pg.ARRAY(sa_pg.VARCHAR(31)))
    dummy_jsonb: Mapped[object] = sqlalchemy.orm.mapped_column(sa_pg.JSONB)
    dummy_json: Mapped[object] = sqlalchemy.orm.mapped_column(sa_pg.JSON)
    dummy_unique_string: Mapped[str] = sqlalchemy.orm.mapped_column(sa_pg.VARCHAR(15), unique=True)

    __table_args__ = (
        sqlalchemy.Index("index_postgresql_dummy_record",
                         dummy_boolean,
                         dummy_smallint,
                         dummy_integer,
                         dummy_bigint,
                         unique=True),
    )


@pytest.mark.skipif(sys.platform == "win32", reason="Test not applicable on Windows")
def test_mysql_connection_maker(fixture_mysql_test_proc, fixture_mysql_test):
    maker = ConnectionMaker(ConnectionMaker.Drivers.Mysql,
                            "127.0.0.1",
                            fixture_mysql_test_proc.port,
                            fixture_mysql_test_proc.user,
                            None,
                            "test",
                            session_opts=dict(
                                expire_on_commit=False,
                            ))

    maker.create_model(MysqlBaseModel)

    rng = randomizer()

    @unique_returns(max_trials=1000)
    def dummy_unique_string() -> str:
        return rng.random_ascii(rng.next_int(0, 16)).lower()

    def random_record():
        return MysqlDummyRecord(
            dummy_char=rng.random_ascii(31),
            dummy_varchar=rng.random_ascii(rng.next_int(0, 32)),
            dummy_text=rng.random_ascii(rng.next_int(0, 1024)),
            dummy_boolean=rng.next_bool(),
            dummy_smallint=rng.next_int(0, 2 ** 15),
            dummy_integer=rng.next_int(0, 2 ** 31),
            dummy_bigint=rng.next_int(0, 2 ** 63),
            dummy_float=rng.next_fixed(6),
            dummy_double=Decimal(rng.next_fixed(10)),
            dummy_date=rng.random_date(),
            dummy_time=rng.random_time().replace(microsecond=0, tzinfo=None),
            dummy_datetime=rng.random_datetime().replace(microsecond=0, tzinfo=None),
            dummy_json=rng.random_json_object(max_depth=5),
            dummy_unique_string=dummy_unique_string(),
        )

    with maker.make_session() as session:
        original_records = [random_record() for _ in range(0, 1000)]
        session.bulk_save_objects(original_records, return_defaults=True)
        session.commit()

    with maker.make_session() as session:
        count = session.query(sqlalchemy.func.count()).select_from(MysqlDummyRecord).scalar()

    assert count == 1000

    with maker.make_session() as session:
        delete_rows = session.query(MysqlDummyRecord).order_by(MysqlDummyRecord.dummy_id).offset(500).all()
        for delete_row in delete_rows:
            session.delete(delete_row)
        session.commit()

    with maker.make_session() as session:
        count = session.query(sqlalchemy.func.count()).select_from(MysqlDummyRecord).scalar()

    assert count == 500

    with maker.make_session() as session:
        records = session.query(MysqlDummyRecord).order_by(MysqlDummyRecord.dummy_id).all()

    for expect, actual in zip(original_records[:count], records[:count]):
        assert actual.dummy_id == nested_approx(expect.dummy_id)
        assert actual.dummy_char == nested_approx(expect.dummy_char)
        assert actual.dummy_varchar == nested_approx(expect.dummy_varchar)
        assert actual.dummy_text == nested_approx(expect.dummy_text)
        assert actual.dummy_boolean == nested_approx(expect.dummy_boolean)
        assert actual.dummy_smallint == nested_approx(expect.dummy_smallint)
        assert actual.dummy_integer == nested_approx(expect.dummy_integer)
        assert actual.dummy_bigint == nested_approx(expect.dummy_bigint)
        assert actual.dummy_float == nested_approx(expect.dummy_float)
        assert actual.dummy_double == nested_approx(expect.dummy_double)
        assert actual.dummy_date == nested_approx(expect.dummy_date)
        assert actual.dummy_time == nested_approx(expect.dummy_time)
        assert actual.dummy_datetime == nested_approx(expect.dummy_datetime)
        assert actual.dummy_json == nested_approx(expect.dummy_json)
        assert actual.dummy_unique_string == nested_approx(expect.dummy_unique_string)

    result = records[0]

    mysql_insert_ignore()

    with maker.make_session() as session:
        # PK violation, but suppressed by the compiler plugin
        session.add(orm_clone(result))
        session.commit()

    with maker.make_session() as session:
        # Unique index violation, but suppressed by the plugin
        # Unlike the Postgresql implementation, MySQL will not raise a 'FlushError'.
        # Instead, it will fill the auto increment column with zero
        session.add(orm_clone(result, no_autoincrement=True))
        session.commit()

    mysql_insert_ignore(enabled=False)

    with maker.make_session() as session:
        # PK violation, which causes 'IntegrityError'
        with pytest.raises(IntegrityError):
            session.add(orm_clone(result))
            session.commit()

    with maker.make_session() as session:
        # Unique index violation, which causes 'IntegrityError'
        with pytest.raises(IntegrityError):
            session.add(orm_clone(result, no_autoincrement=True))
            session.commit()

    maker.drop_model(MysqlBaseModel)


@pytest.mark.skipif(sys.platform == "win32", reason="Test not applicable on Windows")
def test_postgresql_connection_maker(fixture_postgresql_test_proc, fixture_postgresql_test):
    maker = ConnectionMaker(ConnectionMaker.Drivers.Postgresql,
                            fixture_postgresql_test.info.host,
                            fixture_postgresql_test.info.port,
                            fixture_postgresql_test.info.user,
                            None,
                            fixture_postgresql_test.info.dbname,
                            session_opts=dict(
                                expire_on_commit=False,
                            ))

    maker.create_model(PostgresqlBaseModel)

    rng = randomizer()

    @unique_returns(max_trials=1000)
    def dummy_unique_string() -> str:
        return rng.random_ascii(rng.next_int(0, 16)).lower()

    def random_record():
        return PostgresqlDummyRecord(
            dummy_char=rng.random_ascii(31),
            dummy_varchar=rng.random_ascii(rng.next_int(0, 32)),
            dummy_text=rng.random_ascii(rng.next_int(0, 1024)),
            dummy_boolean=rng.next_bool(),
            dummy_smallint=rng.next_int(0, 2 ** 15),
            dummy_integer=rng.next_int(0, 2 ** 31),
            dummy_bigint=rng.next_int(0, 2 ** 63),
            dummy_float=rng.next_fixed(6),
            dummy_double_precision=rng.next_float(),
            dummy_date=rng.random_date(),
            dummy_time=rng.random_time().replace(microsecond=0, tzinfo=None),
            dummy_time_tz=rng.random_time().replace(microsecond=0),
            dummy_timestamp=rng.random_datetime().replace(microsecond=0, tzinfo=None),
            dummy_timestamp_tz=rng.random_datetime().replace(microsecond=0),
            dummy_array_varchar=list(rng.random_ascii(rng.next_int(0, 10)) for _ in range(rng.next_int(0, 10))),
            dummy_jsonb=rng.random_json_object(max_depth=5),
            dummy_json=rng.random_json_object(max_depth=5),
            dummy_unique_string=dummy_unique_string(),
        )

    with maker.make_session() as session:
        original_records = [random_record() for _ in range(0, 1000)]
        session.bulk_save_objects(original_records, return_defaults=True)
        session.commit()

    with maker.make_session() as session:
        count = session.query(sqlalchemy.func.count()).select_from(PostgresqlDummyRecord).scalar()

    assert count == 1000

    with maker.make_session() as session:
        delete_rows = session.query(PostgresqlDummyRecord).order_by(PostgresqlDummyRecord.dummy_id).offset(500).all()
        for delete_row in delete_rows:
            session.delete(delete_row)
        session.commit()

    with maker.make_session() as session:
        count = session.query(sqlalchemy.func.count()).select_from(PostgresqlDummyRecord).scalar()

    assert count == 500

    with maker.make_session() as session:
        records = session.query(PostgresqlDummyRecord).order_by(PostgresqlDummyRecord.dummy_id).all()

    for expect, actual in zip(original_records[:count], records[:count]):
        assert actual.dummy_id == nested_approx(expect.dummy_id)
        assert actual.dummy_char == nested_approx(expect.dummy_char)
        assert actual.dummy_varchar == nested_approx(expect.dummy_varchar)
        assert actual.dummy_text == nested_approx(expect.dummy_text)
        assert actual.dummy_boolean == nested_approx(expect.dummy_boolean)
        assert actual.dummy_smallint == nested_approx(expect.dummy_smallint)
        assert actual.dummy_integer == nested_approx(expect.dummy_integer)
        assert actual.dummy_bigint == nested_approx(expect.dummy_bigint)
        assert actual.dummy_float == nested_approx(expect.dummy_float)
        assert actual.dummy_double_precision == nested_approx(expect.dummy_double_precision)
        assert actual.dummy_date == nested_approx(expect.dummy_date)
        assert actual.dummy_time == nested_approx(expect.dummy_time)
        assert actual.dummy_time_tz == nested_approx(expect.dummy_time_tz)
        assert actual.dummy_timestamp == nested_approx(expect.dummy_timestamp)
        assert actual.dummy_timestamp_tz == nested_approx(expect.dummy_timestamp_tz)
        assert actual.dummy_array_varchar == nested_approx(expect.dummy_array_varchar)
        assert actual.dummy_jsonb == nested_approx(expect.dummy_jsonb)
        assert actual.dummy_json == nested_approx(expect.dummy_json)
        assert actual.dummy_unique_string == nested_approx(expect.dummy_unique_string)

    result = records[0]

    postgresql_insert_on_conflict_do_nothing()

    with maker.make_session() as session:
        # PK violation, but suppressed by the compiler plugin
        session.add(orm_clone(result))
        session.commit()

    with maker.make_session() as session:
        # Unique index violation, but suppressed by the plugin
        # However, since insertion is not performed, it fails to return and
        # flush the auto-generated primary key of the ORM, which raises 'FlushError'
        with pytest.raises(FlushError):
            session.add(orm_clone(result, no_autoincrement=True))
            session.commit()

    postgresql_insert_on_conflict_do_nothing(enabled=False)

    with maker.make_session() as session:
        # PK violation, which causes 'IntegrityError'
        with pytest.raises(IntegrityError):
            session.add(orm_clone(result))
            session.commit()

    with maker.make_session() as session:
        # Unique index violation, which causes 'IntegrityError'
        with pytest.raises(IntegrityError):
            session.add(orm_clone(result, no_autoincrement=True))
            session.commit()

    maker.drop_model(PostgresqlBaseModel)
