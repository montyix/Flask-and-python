from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Creating the database engine
engine = create_engine('postgresql://username:password@localhost/Monty')

# Creating a base class
Base = declarative_base()

# Defining the People table
class People(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Person(name='{self.name}')>"

# Defining the Things table
class Things(Base):
    __tablename__ = 'things'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey('people.id'))
    owner = relationship("People", back_populates="things")

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner

    def __repr__(self):
        return f"<Thing(name='{self.name}', owner='{self.owner.name}')>"

# Creating the tables in the database
Base.metadata.create_all(engine)

# Creating a sessionmaker
Session = sessionmaker(bind=engine)

# Creating a session
session = Session()

# Adding sample data
person1 = People(name='Alice')
person2 = People(name='Bob')

thing1 = Things(name='Book', owner=person1)
thing2 = Things(name='Laptop', owner=person2)

# Adding data to the session
session.add_all([person1, person2, thing1, thing2])

# Committing the session to persist the data in the database
session.commit()

# Querying the data to verify it was inserted successfully
people = session.query(People).all()
things = session.query(Things).all()

for person in people:
    print(person)

for thing in things:
    print(thing)
