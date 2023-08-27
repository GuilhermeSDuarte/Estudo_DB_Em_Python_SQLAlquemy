import sqlalchemy
from sqlalchemy import Column, func
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import select
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
        return f"Address(id={self.id}, email_address={self.email_address})"


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

stmt = select(User).where(User.name.in_(['pedro', 'guilherme']))
# Recuperando as informações de usuario.
print("\nSelect para recuperar usuario:\n")
for user in session.scalars(stmt):
    print(user)

stmt_address = select(Address).where(Address.user_id.in_([1]))
# Recuperando os e-mails do usuario a partir de uma consulta pelo id.
print("\nSelect para recuperar endereço de e-mail:\n")
for address in session.scalars(stmt_address):
    print(address)

#print(select(User).order_by(User.fullname.desc()))

order = select(User).order_by(User.fullname.desc())
# Recupera as informações pela ordem que o usuario definir.
print("\nSelect para recuperar usuario em ordem decrescente:\n")
for user in session.scalars(order):
    print(user)

stmt_join = select(User.fullname, Address.email_address).join_from(Address, User)
print("\nSelect para recuperar os usuarios que existem/possuem informação dentro da tabela address:\n")
for result in session.scalars(stmt_join):
    print(result)

connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("\nExecuttando statement a partir da conmnection:\n")
for result in results:
    print(result)

#print(select(func.count('*')).select_from(User))
stmt_count = select(func.count('*')).select_from(User)
print("\nConta a quantidade de registros da tabela:\n")
for result in session.scalars(stmt_count):
    print(result)
