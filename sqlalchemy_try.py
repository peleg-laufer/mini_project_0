from sqlalchemy import create_engine, Integer, String, Column
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine("sqlite:///try.db", echo=True)
Base = declarative_base()
global Session_maker
Session_maker = sessionmaker(bind=engine)

def add_task(str):
    """
    adds a Task to the db
    assumes there is a tasks table
    :param str: string of task
    :param engine: engine connected to db
    :return: None
    """
    new_task = Task(task_str=str)
    with Session_maker() as session:
        session.add(new_task)

def get_tasks():
    """
    returns list of all tasks.
    :param engine: the engine connected to db
    :return: list of Task type
    """
    with Session_maker() as session:
        res = session.query(Task).all()

    return res

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    task_str = Column(String, nullable=False)

    def __repr__(self) -> str:
        """

        :return: str representation
        """
        return f"{self.id}. {self.task_str}"

Base.metadata.create_all(engine)
add_task("clean up")
tasks = get_tasks()
for task in tasks:
    print(task)


