from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel): 
  email: EmailStr
  password: str

class UserOut(BaseModel): 
  id: int
  email: str 
  is_active: bool
  role: str
  class Config:
    from_atributes = True 

class Token(BaseModel):
  access_token: str
  token_type: str = "bearer"