from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


usergroup = Table(
    'usergroup', Base.metadata,
    Column('group_id', Integer, ForeignKey('groups.id'), nullable=False),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False)
)


filegroup = Table(
    'filegroup', Base.metadata,
    Column('group_id', Integer, ForeignKey('groups.id'), nullable=False),
    Column('file_id', Integer, ForeignKey('files.id'), nullable=False)
)


class Role(Base):
    ADMIN = 1
    CLIENT = 2

    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True, nullable=False)
    # relationships
    users = relationship("User", back_populates="role")

    def __repr__(self):
        return "<Role(id='{id}', name='{name}')>".format(
            name=self.name, id=self.id
        )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    # relationships
    tokens = relationship("Token", cascade="delete", back_populates="user")
    files = relationship("File", cascade="delete", back_populates="owner")
    groups = relationship("Group", back_populates="users", secondary=usergroup)
    role = relationship("Role", back_populates="users")

    def __repr__(self):
        return "<User(id='{id}', name='{name}')>".format(
            name=self.name, id=self.id
        )

    @staticmethod
    def get_by_token(session, token):
        user = session.query(User).join(Token).filter(Token.code == token).one_or_none()
        return user


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True, nullable=False)
    # relationships
    users = relationship("User", back_populates="groups", secondary=usergroup)
    files = relationship("File", back_populates="groups", secondary=filegroup)

    def __repr__(self):
        return "<Group(id='{id}', name='{name}')>".format(
            name=self.name, id=self.id
        )

    @staticmethod
    def get_by_name(session, name):
        return session.query(Group).filter(
            Group.name == name
        ).one_or_none()


class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)

    code = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    # relationships
    user = relationship("User", back_populates="tokens")

    def __repr__(self):
        return "<Token(id='{id}', code='{code}', user='{user}')>".format(
            code=self.code, id=self.id, user=self.user
        )


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)

    uri = Column(String, unique=True, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    # relationships
    owner = relationship("User", back_populates="files")
    groups = relationship("Group", back_populates="files", secondary=filegroup)

    def __repr__(self):
        return "<File(id='{id}', uri='{uri}', owner='{owner}')>".format(
            id=self.id, uri=self.uri, owner=self.owner
        )

    @staticmethod
    def is_exists(session, uri):
        return session.query(File).filter(
            File.uri == uri
        ).count() > 0

    @staticmethod
    def is_token_of_owner(session, uri, token):
        return session.query(File).join(User).join(Token).filter(
            File.uri == uri,
            Token.code == token
        ).count() > 0

    @staticmethod
    def is_token_of_accessed_group(session, uri, token):
        return session.query(File).join(Group, File.groups).join(User, Group.users).join(Token).filter(
            File.uri == uri,
            Token.code == token
        ).count() > 0

    @staticmethod
    def is_available_to_token(session, uri, token):
        return File.is_token_of_owner(session, uri, token) or File.is_token_of_accessed_group(session, uri, token)
