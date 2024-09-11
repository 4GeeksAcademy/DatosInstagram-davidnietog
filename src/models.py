import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Enum, create_engine
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import PrimaryKeyConstraint
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False, unique=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(User)

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    author = relationship(User)
    post = relationship(Post)

class Follower(Base):
    __tablename__ = 'follower'
    user_FROM_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user_TO_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    __table_args__ = (
        PrimaryKeyConstraint('user_FROM_id', 'user_TO_id'),
    )
    user_from = relationship(User, foreign_keys=[user_FROM_id])
    user_to = relationship(User, foreign_keys=[user_TO_id])

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(Enum('image', 'video', 'audio', name='media_type'))
    url = Column(Text, nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    post = relationship(Post)

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e