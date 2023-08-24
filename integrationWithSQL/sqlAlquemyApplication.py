import sqlalchemy
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"
    # Atributos
    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(String)

    fullname = Column(String)

    address = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, fullname={self.fullname})"


class Address(Base):
    __tablename__ = "address"
    # atributos
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    email_address = Column(
        String(30),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("user_account.id"),
        nullable=False
    )

    user = relationship("User", back_populates="address")

    def __repr__(self):
        return f"Address(id={self.id}, email_address={self.email_adress})"


# Conexão com o banco de dados.
engine = create_engine("sqlite://")

# Criando as classes como tabelas no banco de dados.
Base.metadata.create_all(engine)
# Investiga o esquema do banco de dados.
inspetor_engine = inspect(engine)
print(inspetor_engine.has_table("user_account"))
print(inspetor_engine.get_table_names())
print(inspetor_engine.default_schema_name)

with Session(engine) as session:
    guilherme = User(
        name='guilherme',
        fullname='Guilherme Duarte',
        address=[Address(email_address='guilherme@email.com')]
    )

    miguel = User(
        name='miguel',
        fullname='Miguel Duarte',
        address=[Address(email_address='miguel@email.com'),
                Address(email_address='miguelduarte@email.com')]
    )

    pedro = User(
        name='pedro',
        fullname='Pedro Duarte'
    )

    # Enviando para o BD (Persistencia de dados)
    session.add_all([guilherme, miguel, pedro])

    session.commit()
