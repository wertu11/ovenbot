from sqlalchemy import BigInteger, Integer, Text, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base


# Модель для таблицы пользователей
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    full_name: Mapped[str] = mapped_column(String, nullable=True)

    # Связи с заметками и напоминаниями
    notes: Mapped[list["Note"]] = relationship("Note", back_populates="user", cascade="all, delete-orphan")


# Модель для таблицы заметок
class Note(Base):
    __tablename__ = 'vfcselection'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    voltage: Mapped[str] = mapped_column(String, nullable=True)
    vfc1: Mapped[str] = mapped_column(String, nullable=True)
    vfc3: Mapped[str] = mapped_column(String, nullable=True)
    encoder_support: Mapped[str] = mapped_column(String, nullable=True)
    resolver_connection: Mapped[str] = mapped_column(String, nullable=True)
    vfc_power: Mapped[str] = mapped_column(String, nullable=True)
    vfc1_model: Mapped[str] = mapped_column(String, nullable=True)
    vfc3_model: Mapped[str] = mapped_column(String, nullable=True)

    engine_power: Mapped[str] = mapped_column(String, nullable=True)
    encoder_to_resolver_replacement: Mapped[str] = mapped_column(String, nullable=True)
    prom_protocol: Mapped[str] = mapped_column(String, nullable=True)
    extra_IO_or_temperature_sensor: Mapped[str] = mapped_column(String, nullable=True)
    plata: Mapped[str] = mapped_column(String, nullable=True)
    industrial_protocols_support: Mapped[str] = mapped_column(String, nullable=True)
    nominal_out_vfc_power: Mapped[str] = mapped_column(String, nullable=True)
    res_type: Mapped[str] = mapped_column(String, nullable=True)
    vfc_model_selected: Mapped[str] = mapped_column(String, nullable=True)
    distance_to_engine: Mapped[str] = mapped_column(String, nullable=True)
    
    is_shielded: Mapped[str] = mapped_column(String, nullable=True)
    rmt_model: Mapped[str] = mapped_column(String, nullable=True)
    lpo: Mapped[str] = mapped_column(String, nullable=True)
    pvv1: Mapped[str] = mapped_column(String, nullable=True)


    file_id: Mapped[str] = mapped_column(String, nullable=True)
    user: Mapped["User"] = relationship("User", back_populates="notes")
