#!/usr/bin/python3
"""User module"""
from versions.v1.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Boolean, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel, Base, UserMixin):
    """Mapping class for user table"""
    __tablename__ = "user"
    name = Column(String(224), nullable=False)
    email = Column(String(224), nullable=False, unique=True)
    password_hash = Column(String(1024), nullable=False)
    role = Column(String(10), nullable=False)
    profile_image = Column(String(65), nullable=False)

    enrollments = relationship("Enrollment",
                               back_populates="user",
                               cascade="all, delete")
    courses = relationship("Course",
                           back_populates="user",
                           cascade="all, delete")
    user_tasks = relationship('UserTask',
                              back_populates='user')
    user_quizzes = relationship("UserQuiz", back_populates="user",
                                cascade="all, delete")

    @property
    def password(self):
        raise AttributeError('Password is not a readable Attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password=password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password=password)

    def __str__(self):
        return f'<User {self.id}>'


class Program(BaseModel, Base):
    """Mapping class for Program table"""
    __tablename__ = "program"
    name = Column(String(45), nullable=False, unique=True)
    opened = Column(Boolean, default=False)
    description = Column(Text, nullable=False)
    enrollments = relationship("Enrollment", back_populates="program",
                               cascade="all, delete")
    courses = relationship("Course", back_populates="program",
                           cascade="all, delete")


class Enrollment(BaseModel, Base):
    """Mapping class for Enrollment table"""
    __tablename__ = "enrollment"
    user_id = Column(String(60), ForeignKey('user.id', ondelete="CASCADE"),
                     nullable=False)
    program_id = Column(String(60),
                        ForeignKey('program.id', ondelete="CASCADE"),
                        nullable=False)
    user = relationship("User", back_populates="enrollments")
    program = relationship("Program", back_populates="enrollments")


class Course(BaseModel, Base):
    """Mapping class for Course table"""
    __tablename__ = "course"
    name = Column(String(45), nullable=False)
    opened = Column(Boolean, default=False)
    description = Column(Text, nullable=False)
    user_id = Column(String(60), ForeignKey('user.id', ondelete="CASCADE"),
                     nullable=False)
    program_id = Column(String(60),
                        ForeignKey('program.id', ondelete="CASCADE"),
                        nullable=False)
    user = relationship("User", back_populates="courses")
    program = relationship("Program", back_populates="courses")
    resources = relationship("Resource", back_populates="course",
                             cascade="all, delete")
    quizzes = relationship("Quiz", back_populates="course",
                           cascade="all, delete")
    projects = relationship("Project", back_populates="course",
                            cascade="all, delete")


class Resource(BaseModel, Base):
    """Mapping class for Resource table"""
    __tablename__ = "resource"
    title = Column(String(45), nullable=False)
    link = Column(String(255), nullable=False)
    course_id = Column(String(60), ForeignKey('course.id', ondelete="CASCADE"),
                       nullable=False)
    course = relationship("Course", back_populates="resources")


class Project(BaseModel, Base):
    """Mapping class for Project table"""
    __tablename__ = "project"
    title = Column(String(45), nullable=False)
    course_id = Column(String(60), ForeignKey('course.id', ondelete="CASCADE"),
                       nullable=False)
    course = relationship("Course", back_populates="projects")
    tasks = relationship("Task", back_populates="project",
                         cascade="all, delete")


class Task(BaseModel, Base):
    """Mapping class for Task table"""
    __tablename__ = "task"
    title = Column(String(45), nullable=False)
    instruction = Column(Text, nullable=False)
    project_id = Column(String(60),
                        ForeignKey('project.id', ondelete="CASCADE"),
                        nullable=False)
    project = relationship("Project", back_populates="tasks")
    task_answers = relationship("TaskAnswer", back_populates="task",
                                cascade="all, delete")
    user_tasks = relationship("UserTask", back_populates="task",
                              cascade="all, delete")


class TaskAnswer(BaseModel, Base):
    """Mapping class for Task Answer"""
    __tablename__ = "task_answer"
    task_id = Column(String(60), ForeignKey('task.id', ondelete="CASCADE"),
                     nullable=False)
    link = Column(String(500), nullable=False)
    task = relationship("Task", back_populates="task_answers")


class UserTask(BaseModel, Base):
    """Mapping class for User Task"""
    __tablename__ = "user_task"
    user_id = Column(String(60), ForeignKey('user.id', ondelete="CASCADE"),
                     nullable=False)
    task_id = Column(String(60), ForeignKey('task.id', ondelete="CASCADE"),
                     nullable=False)
    score = Column(Integer, nullable=False)
    task = relationship("Task", back_populates="user_tasks")
    user = relationship("User", back_populates="user_tasks")


class Quiz(BaseModel, Base):
    """Mapping class for Quiz table"""
    __tablename__ = "quiz"
    title = Column(String(45), nullable=False)
    question = Column(Text, nullable=False)
    duration = Column(Integer, nullable=False)
    course_id = Column(String(60), ForeignKey('course.id', ondelete="CASCADE"),
                       nullable=False)
    course = relationship("Course", back_populates="quizzes")
    answers = relationship("Answer", back_populates="quiz",
                           cascade="all, delete")
    user_quizzes = relationship("UserQuiz", back_populates="quiz",
                                cascade="all, delete")


class Answer(BaseModel, Base):
    """Mapping class for Quiz Answer"""
    __tablename__ = "answer"
    answer = Column(String(500), nullable=False)
    quiz_id = Column(String(60), ForeignKey('quiz.id', ondelete="CASCADE"),
                     nullable=True)
    quiz = relationship("Quiz", back_populates="answers")


class UserQuiz(BaseModel, Base):
    """Mapping class for User Quiz"""
    __tablename__ = "user_quiz"
    user_id = Column(String(60), ForeignKey('user.id', ondelete="CASCADE"),
                     nullable=False)
    quiz_id = Column(String(60), ForeignKey('quiz.id', ondelete="CASCADE"),
                     nullable=False)
    score = Column(Integer, nullable=False)
    user = relationship("User", back_populates="user_quizzes")
    quiz = relationship("Quiz", back_populates="user_quizzes")
