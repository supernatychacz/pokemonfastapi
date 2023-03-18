from pydantic import BaseModel, EmailStr, validator
from typing import Optional


class UserSignInModel(BaseModel):
    email: EmailStr
    password: str

    @validator('password')
    def passwordLength(cls, v):
        if len(v) < 6 and len(v) > 16: 
            raise ValueError('Password must be between 6 and 16 characters')
        return v

class UserSignUpModel(UserSignInModel):
    name: str
  

class UserResponseModel(BaseModel):
    name: str
    email: EmailStr
    token: Optional[str] = None

    class Config:
        orm_mode = True


class PokemonStatsResponseModel(BaseModel):
    height_m: Optional[float] = None
    weight_kg: Optional[float] = None
    attack: Optional[int] = None

    class Config:
        orm_mode = True

class PokemonResponseModel(BaseModel):
    name: str
    classification: str
    type1: str
    type2: str
    generation: int
    stats: PokemonStatsResponseModel

    class Config:
        orm_mode = True