from pydantic import BaseModel, Field
from datetime import datetime


class AuthDetails(BaseModel):
	username: str = Field(..., min_length=3, max_length=50)
	password: str = Field(..., min_length=6)


class UserResponse(BaseModel):
	id: int
	username: str
	created_at: datetime

	class Config:
		from_attributes = True


class TokenResponse(BaseModel):
	access_token: str
	token_type: str = "bearer"
