from sqlalchemy import Column, Enum, Integer, String
from src.schemas.EmpSchema import EmployeeType
from src.repositories.database import Base

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    user_type = Column(Enum(EmployeeType))  # Could be 'admin' or 'client' corresponding to EmployeeType    