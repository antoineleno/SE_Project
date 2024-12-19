#!/usr/bin/python3
"""DB Storage module"""

import os
import sys
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base, BaseModel
from models.models import User
from models.models import Program
from models.models import Course
from models.models import Project
from models.models import Enrollment
from models.models import Resource
from models.models import Task
#from models import TaskAnswer
from models.models import UserTask
from models.models import Quiz
from models.models import Answer
from models.models import UserQuiz

base_dir = os.path.dirname(__file__)
parent_dir = os.path.join(base_dir, '..', '..')
sys_path = os.path.abspath(parent_dir)

sys.path.append(sys_path)


class DBStorage:
    """DBStorage
    Class to manage objects storage to DB
    """
    __engine = None
    __session = None

    def __init__(self):
        """Contructor method
        """
        env = getenv("EDUPATHWAY_ENV")
        db = 'edupathway_db'

        if env == 'test':
            db = 'edupathway_test_db'

        self.__engine = create_engine(
                    'mysql+mysqldb://edupathway_user:edupathway_pwd@localhost/{}'.format(db),
                    pool_pre_ping=True)


    def all(self, cls=None):
        """all to retrieve all records from DB

        Args:
            cls (string, optional): Object to return. Defaults to None.

        Returns:
            Dict: All records from a database
        """
        allclasses = {
               'BaseModel': BaseModel, 'User': User, 'Program': Program,
               'Course': Course, 'Project': Project, 'Enrollment': Enrollment,
               'Resource': Resource, 'Task': Task, 'TaskAnswer': TaskAnswer,
               'UserTask': UserTask, 'Quiz': Quiz, 'Answer': Answer, 'UserQuiz': UserQuiz
              }
        obj_result = {}
        cls = cls if not isinstance(cls, str) else allclasses.get(cls)
        if cls is None:
            for cls in allclasses:
                objs = self.__session.query(cls).all()
                for o in objs:
                    obj_result["{}.{}".format(o.name, o.id)] = o
        else:
            objs = self.__session.query(cls).all()
            for o in objs:
                obj_result["{}.{}".format(o.__table__, o.id)] = o
        return obj_result

    def new(self, obj):
        """new : to add an an obj to a session

        Args:
            obj (instance): Obj created to be added
        """
        self.__session.add(obj)

    def save(self):
        """save: method to commit changes to the db
        """
        self.__session.commit()

    def delete(self, obj=None):
        """Method to delete an obj from the db

        Args:
            obj (string): name of the obj. Defaults to None.
        """
        if obj:
            self.__session.delete(obj)
            self.__session.commit()

    def reload(self):
        """create all tables in the database
        """
        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(factory)()

    def close(self):
        """close session
        """
        self.__session.close()

    def drop_all(self):
        """drop the test database"""
        Base.metadata.drop_all(self.__engine)
        self.save()


    def get_object(self, cls, sign=None, all=None, order_by=None,
                   limit=None,
                   count=False, **kwargs):
        """
        Get all objects or only one object based on filters.
        Optionally count the results.

        Args:
            cls: The model class to query.
            sign: The comparison operator for filtering.
            all: If not None, fetches all matching objects.
            order_by: A tuple (column, direction) for sorting
                (e.g., (cls.created_at, 'desc')).
            limit: An integer specifying the maximum number
                of results to return.
            count: If True, returns the count of results based on the filters.
            **kwargs: Key-value pairs for filtering.

        Returns:
            A single object if `all` is None, otherwise a list of objects.
            If `count` is True, returns the count of objects.
        """
        if sign is None:
            sign = '=='

        query = self.__session.query(cls)

        operators = {
            '==': lambda key, value: key == value,
            '!=': lambda key, value: key != value,
            '<': lambda key, value: key < value,
            '<=': lambda key, value: key <= value,
            '>': lambda key, value: key > value,
            '>=': lambda key, value: key >= value
        }

        if kwargs:
            for key, value in kwargs.items():
                if sign in operators:
                    query = query.filter(operators[sign](getattr(cls, key),
                                                         value))
                else:
                    raise ValueError(f"Invalid comparison operator: {sign}")
        if count:
            if (
                "room_id" in kwargs and
                "user_id" in kwargs and
                "read_status" in kwargs
            ):
                query = self.__session.query(cls).filter(
                    cls.room_id == kwargs.get("room_id"),
                    cls.user_id != kwargs.get("user_id"),
                    cls.read_status == False
                )

                return query.count()
        if order_by:
            column, direction = order_by
            if direction.lower() == 'desc':
                query = query.order_by(column.desc())
            elif direction.lower() == 'asc':
                query = query.order_by(column)
            else:
                raise ValueError("Invalid direction for order_by")

        if limit is not None:
            query = query.limit(limit)
        if all is not None:
            return query.all()
        return query.first()
