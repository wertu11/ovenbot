from create_bot import logger
from .base import connection
from .models import User, Note
# from .models import User, Vfcselection
from sqlalchemy import select
from typing import List, Dict, Any, Optional
from sqlalchemy.exc import SQLAlchemyError


@connection
async def set_user(session, tg_id: int, username: str, full_name: str) -> Optional[User]:
    try:
        user = await session.scalar(select(User).filter_by(id=tg_id))

        if not user:
            new_user = User(id=tg_id, username=username, full_name=full_name)
            session.add(new_user)
            await session.commit()
            logger.info(f"Зарегистрировал пользователя с ID {tg_id}!")
            return None
        else:
            logger.info(f"Пользователь с ID {tg_id} найден!")
            return user
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении пользователя: {e}")
        await session.rollback()


@connection
async def add_note(session, user_id: int, content_type: str,
                   content_text: Optional[str] = None, file_id: Optional[str] = None) -> Optional[Note]:
    try:
        user = await session.scalar(select(User).filter_by(id=user_id))
        if not user:
            logger.error(f"Пользователь с ID {user_id} не найден.")
            return None

        new_note = Note(
            user_id=user_id,
            content_type=content_type,
            content_text=content_text,
            file_id=file_id
        )

        session.add(new_note)
        await session.commit()
        logger.info(f"Заметка для пользователя с ID {user_id} успешно добавлена!")
        return new_note
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении заметки: {e}")
        await session.rollback()

@connection
async def add_vfc(session, user_id: int, vfc_order: dict):
    try:
        user = await session.scalar(select(User).filter_by(id=user_id))
        if not user:
            logger.error(f"Пользователь с ID {user_id} не найден.")
            return None

        new_note = Note(
            user_id=user_id,
            voltage=vfc_order['voltage'],
            vfc1=vfc_order['vfc1'],
            vfc3=vfc_order['vfc3'],
            engine_power = vfc_order['engine_power'],
            encoder_to_resolver_replacement = vfc_order['encoder_to_resolver_replacement'],
            prom_protocol = vfc_order['prom_protocol'],
            extra_IO_or_temperature_sensor = vfc_order['extra_IO_or_temperature_sensor'],
            plata = vfc_order['plata'],
            industrial_protocols_support = vfc_order['industrial_protocols_support'],
            nominal_out_vfc_power = vfc_order['nominal_out_vfc_power'],
            res_type = vfc_order['res_type'],
            encoder_support=vfc_order['encoder_support'],
            resolver_connection=vfc_order['resolver_connection'],
            vfc_power=vfc_order['vfc_power'],
            vfc_model_selected=vfc_order['vfc_model_selected']["Модификация"].values[0],
            distance_to_engine=vfc_order['distance_to_engine'],
            is_shielded=vfc_order['is_shielded'],
            rmt_model=vfc_order['rmt_model'],
            lpo=vfc_order['lpo'],
            pvv1=vfc_order['pvv1']
        )

        session.add(new_note)
        await session.commit()
        logger.info(f"Подобран ПЧВ для пользователя с ID {user_id}!")
        return new_note
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении записи: {e}")
        await session.rollback()



@connection
async def update_text_note(session, note_id: int, content_text: str) -> Optional[Note]:
    try:
        note = await session.scalar(select(Note).filter_by(id=note_id))
        if not note:
            logger.error(f"Заметка с ID {note_id} не найдена.")
            return None

        note.content_text = content_text
        await session.commit()
        logger.info(f"Заметка с ID {note_id} успешно обновлена!")
        return note
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при обновлении заметки: {e}")
        await session.rollback()
