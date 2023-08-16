from datetime import datetime

from database.databases import User, Session, Base, engine, Bots, Settings

Base.metadata.create_all(engine)


def check_user(user_id: int) -> bool:
    with Session() as session:
        result = session.query(User).filter_by(user_id=int(user_id)).first()
        return bool(result)


def get_all_admins() -> list[User]:
    with Session() as session:
        result = session.query(User).filter(User.is_admin != 0).all()
        return result


def check_admin(user_id: int) -> bool:
    with Session() as session:
        result = session.query(User).filter_by(user_id=int(user_id)).filter(User.is_admin != 0).first()
        return bool(result)


def add_admin(user_id: int, owner_id: int):
    with Session() as session:
        session.query(User).filter(User.user_id == user_id).update({'is_admin': owner_id},
                                                                   synchronize_session="fetch")
        session.commit()


async def add_user(user_id: int, lang: str, first_name, last_name, username, ref_id=None) -> User:
    with Session() as session:
        result = session.query(User).filter_by(user_id=int(user_id)).first()
        if result is None:
            new_user = User(user_id=user_id, first_name=first_name, last_name=last_name, username=username,
                            ref_id=ref_id, lang=lang, register_datetime=datetime.now())
            session.add(new_user)
            session.commit()
        return result


def edit_user_info(user_id: int, setting: str, new_value: str):
    with Session() as session:
        session.query(User).filter(User.user_id == user_id).update({setting: new_value},
                                                                   synchronize_session="fetch")
        session.commit()


def get_user_by_user_id(user_id: int) -> User:
    with Session() as session:
        result = session.query(User).filter_by(user_id=int(user_id)).first()
        return result


def get_user_by_id(id_user: int) -> User:
    with Session() as session:
        result = session.query(User).filter_by(id=id_user).first()
        return result


def get_all_users() -> list[User]:
    with Session() as session:
        result = session.query(User).all()
        return result


def add_balance(user_id, summ):
    with Session() as session:
        user_info = session.query(User).filter_by(user_id=int(user_id)).first()
        session.query(User).filter(User.user_id == user_id).update({"balance": user_info.balance + summ},
                                                                   synchronize_session="fetch")
        session.commit()


def add_bot(user_id: int, bot_id: int, token: str, title: str, username: str) -> Bots:
    with Session() as session:
        result = session.query(Bots).filter_by(user_id=user_id, token=token).first()
        if result is None:
            new_bot = Bots(user_id=user_id, bot_id=bot_id, token=token, title=title, username=username)
            new_setting = Settings(user_id=user_id, bot_id=bot_id)
            session.add(new_bot)
            session.add(new_setting)
            session.commit()
        return result


def get_bot_by_bot_id(bot_id: int) -> Bots:
    with Session() as session:
        result = session.query(Bots).filter_by(bot_id=bot_id).first()
        return result


def get_all_bots() -> list[Bots]:
    with Session() as session:
        result = session.query(Bots).all()
        return result


def remove_bot_by_bot_id(user_id: int, bot_id: int) -> None:
    with Session() as session:
        result = session.query(Bots).filter(Bots.user_id == user_id, Bots.bot_id == bot_id)
        result_setting = session.query(Settings).filter(Settings.user_id == user_id, Settings.bot_id == bot_id)
        result.delete(synchronize_session=False)
        result_setting.delete(synchronize_session=False)
        session.commit()
