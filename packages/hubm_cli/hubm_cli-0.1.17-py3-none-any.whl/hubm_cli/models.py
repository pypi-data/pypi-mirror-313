from sqlalchemy import ARRAY, BigInteger, Boolean, CheckConstraint, Computed, Date, DateTime, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, Sequence, SmallInteger, String, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import INET, INTERVAL, TIMESTAMP
from typing import Any, List, Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class Callback(Base):
    __tablename__ = 'callback'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='callback_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    data: Mapped[Optional[str]] = mapped_column(Text)


class Servers(Base):
    __tablename__ = 'servers'
    __table_args__ = (
        CheckConstraint('tcp_port >= 20 AND tcp_port <= 65535', name='tcp_port_range'),
        PrimaryKeyConstraint('id', name='servers_pkey'),
        UniqueConstraint('name', name='name_uniq'),
        UniqueConstraint('tcp_port', name='tcp_port_uniq')
    )

    id: Mapped[int] = mapped_column(Integer, Sequence('servers_server_id_seq'), primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    tcp_port: Mapped[int] = mapped_column(Integer)
    ip_check: Mapped[bool] = mapped_column(Boolean, server_default=text('false'))
    login: Mapped[str] = mapped_column(String(50), Computed('name', persisted=True))
    password: Mapped[str] = mapped_column(String(50), server_default=text('substr(md5((random())::text), 1, 10)'))
    ip: Mapped[Any] = mapped_column(INET, server_default=text("'10.10.8.161'::inet"))
    pid: Mapped[Optional[int]] = mapped_column(Integer)

    saved_session_user: Mapped[List['SavedSessionUser']] = relationship('SavedSessionUser', back_populates='server')
    usb_ports: Mapped[List['UsbPorts']] = relationship('UsbPorts', back_populates='server')
    user_server_relation: Mapped[List['UserServerRelation']] = relationship('UserServerRelation', back_populates='server')
    logs: Mapped[List['Logs']] = relationship('Logs', back_populates='server')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        CheckConstraint("email::text ~ '^[a-zA-Z0-9.!#$%%&''*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'::text", name='valid_email'),
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('name', name='username_uniq')
    )

    id: Mapped[int] = mapped_column(Integer, Sequence('users_user_id_seq'), primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    cn: Mapped[str] = mapped_column(String(50), server_default=text("'Incorrect common name!'::character varying"))
    ip: Mapped[Any] = mapped_column(INET)
    active: Mapped[bool] = mapped_column(Boolean, server_default=text('true'))
    password: Mapped[Optional[str]] = mapped_column(String(50), server_default=text('substr(md5((random())::text), 1, 10)'))
    email: Mapped[Optional[str]] = mapped_column(String(60))
    comment: Mapped[Optional[str]] = mapped_column(String(100))
    tg_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    tg_code: Mapped[Optional[str]] = mapped_column(String(30), server_default=text('substr(md5((random())::text), 1, 10)'))

    saved_session_user: Mapped[List['SavedSessionUser']] = relationship('SavedSessionUser', back_populates='user')
    user_server_relation: Mapped[List['UserServerRelation']] = relationship('UserServerRelation', back_populates='user')
    logs: Mapped[List['Logs']] = relationship('Logs', back_populates='user')
    user_usb_relation: Mapped[List['UserUsbRelation']] = relationship('UserUsbRelation', back_populates='user')


class SavedSessionUser(Base):
    __tablename__ = 'saved_session_user'
    __table_args__ = (
        ForeignKeyConstraint(['server_id'], ['servers.id'], name='server_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='user_id_fkey'),
        PrimaryKeyConstraint('id', name='saved_session_user_pkey'),
        Index('fki_server_id_fkey', 'server_id'),
        Index('fki_user_id_fkey', 'user_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    server_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer)
    date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    timeout: Mapped[Optional[datetime.timedelta]] = mapped_column(INTERVAL)
    user_ip: Mapped[Optional[Any]] = mapped_column(INET)

    server: Mapped['Servers'] = relationship('Servers', back_populates='saved_session_user')
    user: Mapped['Users'] = relationship('Users', back_populates='saved_session_user')


class UsbPorts(Base):
    __tablename__ = 'usb_ports'
    __table_args__ = (
        ForeignKeyConstraint(['server_id'], ['servers.id'], name='usb_ports_server_id_fkey'),
        PrimaryKeyConstraint('id', name='usb_ports_pkey'),
        UniqueConstraint('bus', name='bus_uniq'),
        UniqueConstraint('virtual_port', name='virtual_port_uniq')
    )

    id: Mapped[int] = mapped_column(Integer, Sequence('usb_ports_port_id_seq'), primary_key=True)
    bus: Mapped[str] = mapped_column(String(30))
    active: Mapped[bool] = mapped_column(Boolean, server_default=text('true'))
    server_id: Mapped[Optional[int]] = mapped_column(Integer)
    virtual_port: Mapped[Optional[str]] = mapped_column(String(50), comment='Виртуальный номер порта используемый для управления')
    name: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("'undefined'::character varying"))

    server: Mapped['Servers'] = relationship('Servers', back_populates='usb_ports')
    logs: Mapped[List['Logs']] = relationship('Logs', back_populates='usb_port')
    user_usb_relation: Mapped[List['UserUsbRelation']] = relationship('UserUsbRelation', back_populates='port')


class UserServerRelation(Base):
    __tablename__ = 'user_server_relation'
    __table_args__ = (
        ForeignKeyConstraint(['server_id'], ['servers.id'], name='user_server_relation_server_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='user_server_relation_user_id_fkey'),
        PrimaryKeyConstraint('id', name='user_server_relation_pkey'),
        UniqueConstraint('user_id', 'server_id', name='server_for_user_uniq')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    server_id: Mapped[int] = mapped_column(Integer)
    auth_method: Mapped[int] = mapped_column(SmallInteger, server_default=text('2'), comment='0 - только пароль\n1 - пароль и временный OTP-код\n2 - временный OTP-код\n3 - LDAP\n4 - TG_BOT')
    otp_secret: Mapped[str] = mapped_column(String(50), server_default=text("'undefined'::character varying"))
    access: Mapped[bool] = mapped_column(Boolean, server_default=text('true'))
    usb_filter: Mapped[bool] = mapped_column(Boolean, server_default=text('true'))
    until: Mapped[datetime.date] = mapped_column(Date, server_default=text("'2040-01-01'::date"))
    kick: Mapped[bool] = mapped_column(Boolean, server_default=text('false'))
    kickable: Mapped[bool] = mapped_column(Boolean, server_default=text('true'))
    ip: Mapped[Any] = mapped_column(INET)
    timeout_session: Mapped[datetime.timedelta] = mapped_column(INTERVAL, server_default=text("'00:30:00'::interval"))
    login_use: Mapped[bool] = mapped_column(Boolean, server_default=text('false'))
    password: Mapped[Optional[str]] = mapped_column(String(50), server_default=text('substr(md5((random())::text), 1, 10)'))
    handle: Mapped[Optional[int]] = mapped_column(Integer)
    ips: Mapped[Optional[list]] = mapped_column(ARRAY(INET()))
    name: Mapped[Optional[str]] = mapped_column(Text)

    server: Mapped['Servers'] = relationship('Servers', back_populates='user_server_relation')
    user: Mapped['Users'] = relationship('Users', back_populates='user_server_relation')


class Logs(Base):
    __tablename__ = 'logs'
    __table_args__ = (
        ForeignKeyConstraint(['server_id'], ['servers.id'], name='logs_server_id'),
        ForeignKeyConstraint(['usb-port_id'], ['usb_ports.id'], name='logs_usb-port_id'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='logs_user_id'),
        PrimaryKeyConstraint('id', name='logs_pkey'),
        Index('fki_logs_server_id', 'server_id'),
        Index('fki_logs_usb-port_id', 'usb-port_id'),
        Index('fki_logs_user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    date: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(True, 3))
    code: Mapped[int] = mapped_column(Integer)
    message: Mapped[str] = mapped_column(String)
    server_id: Mapped[Optional[int]] = mapped_column(Integer)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    usb_port_id: Mapped[Optional[int]] = mapped_column('usb-port_id', Integer)

    server: Mapped['Servers'] = relationship('Servers', back_populates='logs')
    usb_port: Mapped['UsbPorts'] = relationship('UsbPorts', back_populates='logs')
    user: Mapped['Users'] = relationship('Users', back_populates='logs')


class UserUsbRelation(Base):
    __tablename__ = 'user_usb_relation'
    __table_args__ = (
        ForeignKeyConstraint(['port_id'], ['usb_ports.id'], name='user_usb_relation_port_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='user_usb_relation_user_id_fkey'),
        PrimaryKeyConstraint('id', name='user_usb_relation_pkey'),
        UniqueConstraint('user_id', 'port_id', name='user_usb_relation_uniq')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    port_id: Mapped[int] = mapped_column(Integer)

    port: Mapped['UsbPorts'] = relationship('UsbPorts', back_populates='user_usb_relation')
    user: Mapped['Users'] = relationship('Users', back_populates='user_usb_relation')
