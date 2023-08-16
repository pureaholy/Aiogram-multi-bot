from sqlalchemy import create_engine, Column, BigInteger, Text, Integer, Float, DateTime, update, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship

from config import Config

Base = declarative_base()
engine = create_engine(Config.create_engine)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(BigInteger)
    first_name = Column(Text)
    last_name = Column(Text)
    username = Column(Text)
    ref_id = Column(BigInteger, default=None)
    balance = Column(Float, default=0)
    lang = Column(Text)
    is_admin = Column(BigInteger, default=0)
    lvl = Column(Integer, default=1)
    last_task = Column(BigInteger, default=0)
    register_datetime = Column(DateTime)
    bots = relationship('Bots', back_populates='user', lazy='joined')

    def edit_info(self, column_name, new_value):
        with Session() as session:
            table = self.__table__

            # Создаем объект запроса для обновления записи
            update_query = (
                update(table)
                .where(table.c.user_id == self.user_id)
                .values({column_name: new_value})
            )

            # Выполняем запрос к базе данных
            session.execute(update_query)
            session.commit()

    def toggle_admin(self):
        with Session() as session:
            self.is_admin = not self.is_admin
            session.add(self)
            session.commit()
            return self.is_admin

    def add_balance(self, summ: int):
        with Session() as session:
            self.balance += summ
            session.add(self)
            session.commit()


class Bots(Base):
    __tablename__ = "bots"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('user.user_id'))
    bot_id = Column(BigInteger)
    token = Column(Text)
    title = Column(Text)
    username = Column(Text)
    user = relationship('User', back_populates='bots')

    def delete(self):
        with Session() as session:
            session.delete(self)
            session.commit()
            return self


class Settings(Base):
    __tablename__ = "settings"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(BigInteger)
    bot_id = Column(BigInteger)
