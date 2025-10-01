from typing import Optional
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship, Mapped, mapped_column, foreign

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=True)


class BaseModel(DeclarativeBase):
    __abstract__ = True 
    __allow_unmapped__ = True

    id: Mapped[int] = mapped_column(primary_key=True)



# one to many relationship between User and Address
class User(BaseModel):
    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=None)

    addresses: Mapped[list["Address"]] = relationship()

    def __repr__(self) -> str:
        return f"<UserModel(id={self.id}, name={self.name})>"
    

class Address(BaseModel):
    __tablename__ = 'addresses'

    city: Mapped[str] = mapped_column(String(50), nullable=False)
    state: Mapped[str] = mapped_column(String(50), nullable=False)
    zip_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, default=None)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="addresses")
    # user = relationship("User", back_populates="addresses")

    def __repr__(self) -> str:
        return f"<AddressModel(id={self.id}, city={self.city})>"



# one to one self-relationship with using association table
nodes_association = Table(
    "nodes_association",
    BaseModel.metadata,
    Column('current_node_id', Integer, ForeignKey("nodes.id"), primary_key=True),
    Column('next_node_id', Integer, ForeignKey("nodes.id"), primary_key=True),
)

class Node(BaseModel):
    __tablename__ = "nodes"

    value: Mapped[int] = mapped_column(nullable=False)

    next_node = relationship(
        "Node",
        secondary=nodes_association,  # the link between Node and Node goes through "nodes_association" table.
        primaryjoin=lambda: foreign(nodes_association.c.current_node_id) == Node.id,  # c is a shorthand for column collection = nodes_association.columns.current_node_id
        # primaryjoin: find rows in nodes_association where current_node_id matches this Node’s id.
        # foreign() marks the column (current_node_id) as the foreign key side.
        secondaryjoin=lambda: foreign(nodes_association.c.next_node_id) == Node.id,
        # secondaryjoin: find rows in nodes_association where next_node_id matches the id of the target Node.
        # lambda is just a function that SQLAlchemy can call later, after the class is fully built.
        # remote_side=[nodes_association.c.current_node_id],
        uselist=False
    )

    def __repr__(self) -> str:
        return f"<NodeModel(value={self.value}, next value={self.next_node.value if self.next_node else None})>"




BaseModel.metadata.drop_all(engine)
BaseModel.metadata.create_all(engine)

sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)



"""
Notes:

    - Mapped[...] = Python typing

        - Tells your editor/type checker what the attribute type is.

    - mapped_column() = SQL column definition

        - Tells DB the column type and constraints.

    - Optional in Python must match nullable in SQL

        - Imported from `typing` model
        - If nullable=True → use Optional[...].
        - If nullable=False → don’t use Optional[...].

    - Shortcuts exist

        - mapped_column(primary_key=True) defaults to Integer.
        - If you want a different PK type (e.g., String), you must specify it explicitly

    - __abstract__ means this model is abstract, don’t create a database table for it, When you want to make a base class with shared columns or logic, but you don’t want it to directly correspond to a table.

    - __allow_unmapped__ = True means allow me to have non-Mapped attributes in this class.

        - Attributes without Mapped[] won’t be mapped to the database (they’re just Python variables).
        - This is useful if you want helper properties, cached values, or data that doesn’t belong in the DB.
        - Ex:   
            class Product(Base):
                __tablename__ = "products"
                __allow_unmapped__ = True  # ✅ SQLAlchemy won’t complain

                id: Mapped[int] = mapped_column(primary_key=True)
                name: str  # now allowed (but not a mapped column)


    - Remote side vs foreign()

        - foreign() → tells SQLAlchemy: this column in the association table is the foreign key side (the child column).
        - remote_side (used in other self-relationships, e.g. without an association table) → tells SQLAlchemy: when both columns are in the same table (like parent_id and id), this one is the “remote” one (the parent).
"""