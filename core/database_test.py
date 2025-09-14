from sqlalchemy import create_engine, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker,declarative_base, relationship
from sqlalchemy  import Boolean, Column, Integer, String, Text, Boolean, UniqueConstraint, Table
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"
# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# for postgres or other relational databases
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver:5432/db"
# SQLALCHEMY_DATABASE_URL = "mysql://username:password@localhost/db_name"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False # only for sqlite
}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# create base class for declaring tables
Base = declarative_base()

enrollments = Table("enrollments", Base.metadata,
                    Column("id", Integer, primary_key=True),
                    Column("users_id", Integer, ForeignKey("users.id")),
                    Column("course_id", Integer, ForeignKey("courses.id")),
                    Column("enrolled_date", DateTime(), default=datetime.now()),
                    UniqueConstraint("users_id","course_id",name="unique_user_courses_enrolled")
                    )


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    title = Column(String,nullable=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    
    addresses = relationship("Address", backref="user")
    comments = relationship("Comment", backref="user")
    posts = relationship("Post", backref="user")
    courses = relationship("Course", secondary=enrollments,back_populates="attendees")


    @property
    def get_fullname(self):
        first = self.first_name or ""
        last = self.last_name or ""
        return f"{first} {last}".strip()
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r}, fullname={self.get_fullname!r})"

class Address(Base):
    __tablename__ = "addresses"
    
    id = Column(Integer,autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    

    @property
    def get_fullname(self):
        first = self.first_name or ""
        last = self.last_name or ""
        return f"{first} {last}".strip()
    
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, user_id={self.user_id}, city={self.city!r})"



class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer,autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    content = Column(Text())
    created_data = Column(DateTime(), default=datetime.now())
    updated_data = Column(DateTime(), default=datetime.now(), onupdate=datetime.now())

    comments = relationship("Comment", backref="post", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Post(id={self.id},user_id={self.user_id}, contnet={self.content})"


class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer,autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    parent_id = Column(Integer, ForeignKey("comments.id"),nullable=True)
    content = Column(Text())
    created_data = Column(DateTime(), default=datetime.now())
    is_accepted = Column(Boolean,default=True)

    parent = relationship("Comment", remote_side=[id], back_populates="children")
    children = relationship("Comment", back_populates="parent")
    def __repr__(self):
        return f"Commnet(id={self.id}, post_id={self.post_id}, user_id={self.user_id})"

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer,autoincrement=True, primary_key=True)
    title = Column(String)
    description = Column(Text())
    created_data = Column(DateTime(), default=datetime.now())

    attendees = relationship("User", secondary=enrollments, back_populates="courses")

    def __repr__(self):
        return f"Course(id={self.id}, title={self.title})"


# to create tables and database
Base.metadata.create_all(bind = engine)

session = SessionLocal()

# narges = User(first_name="narges",last_name="HKH",  age=2)
# session.add(narges)
# session.commit()


# reyhaneh = User(first_name="reyhaneh",last_name="rgh",  age=27)
# iman = User(first_name="iman",last_name="HKH",  age=31)
# session.add_all([reyhaneh, iman])
# session.commit()

# user = session.query(User).filter_by(id=1).all()
# user[0].email="narges1404@gmail.com"
# session.commit()
# print(user)

# session.delete(user[0])
# session.commit()

# ************************* one-to-many **************************

# session.add(User(first_name="reyhaneh",last_name="rgh",  age=27))
# session.commit()

user = session.query(User).filter_by(first_name="reyhaneh").one_or_none()
# print(user)

# addresses = [Address(user_id=1,city="yazd",state="yazd",zip_code="123"), Address(user_id=1,city="tehran",state="tehran",zip_code="123")]
# session.add_all(addresses)
# session.commit()

addr = session.query(Address).filter_by(user_id=user.id).all()
print(addr)
session.commit()

# session.add(Post(user_id=user.id,title="AI", content="this is AI post"))
# session.commit()
post = user.posts[0]

# session.add(Comment(user_id=user.id,post_id=posts[0].id, content="this is comment 1"))
# session.commit()

# print(post.comments)
parent_comment = post.comments[0]

# session.add(Comment(user_id=user.id, post_id=post.id,parent_id=parent_comment.id, content="this is reply 1"))
# session.add(Comment(user_id=user.id, post_id=post.id,parent_id=parent_comment.id, content="this is reply 2"))
# session.commit()


print(parent_comment.children)

reply = parent_comment.children[0]
print(reply.parent)


# ************************* many-to-many **************************

# session.add(Course(title="python", description="this is python course"))
# session.add(Course(title="java", description="this is java course"))
# session.add(Course(title="react", description="this is react course"))
# session.add(User(first_name="iman",last_name="HKH",  age=31))
# session.commit()


iman = session.query(User).filter_by(first_name="iman").one()
python = session.query(Course).filter_by(title="python").one()
java = session.query(Course).filter_by(title="java").one()
react = session.query(Course).filter_by(title="react").one()

# python.attendees.append(user)
# python.attendees.append(iman)
# java.attendees.append(iman)
# react.attendees.append(user)

print(python.attendees)
print(java.attendees)
print(react.attendees)
print(user.courses)
print(iman.courses)

# del_user = session.query(Course).filter_by(id=9).first()
# # print(del_user)
# session.delete(del_user)
# session.commit()