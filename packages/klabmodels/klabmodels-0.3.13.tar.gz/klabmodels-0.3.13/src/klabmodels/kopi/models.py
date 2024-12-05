from typing import Dict, List
from redis_om import JsonModel, EmbeddedJsonModel, Field
from pydantic import BaseModel, Extra, ValidationError
from enum import Enum
from datetime import date

class Application(str, Enum):
    kopi = 'kopi'
    kiwi = 'kiwi'
    pickey = 'pickey'
    a_team = 'a-team'
    lumina = 'lumina'


# Top Level entity
class Tenant(JsonModel):
    name: str = Field(index=True)
    api_key: str = Field(index=True)
    logo: bytes | None = None
    active: bool = True
    max_users: int = 10
    apps: List[Application] = [Application.kopi]



class User(JsonModel):
    username: str = Field(index=True)
    email: str = Field(index=True)
    tenant: str = Field(index=True)
    full_name: str | None = None
    disabled: bool | None = None
    #companies: List[str] | None = None  # companies the user has access to
    scopes: List[str] = []
    hashed_password: str = None

    def __str__(self):    
        return '\n'.join({f"{k.upper()} : {v}" for k,v in self.dict().items() if v and k not in ('pk', 'hashed_password')})
    
    def details(self):
        return {k:v for k,v in self.dict().items() if v and k not in ('pk', 'hashed_password')}
    


class Employee(User, extra=Extra.allow):
    company: str
    started_on: date
    job_title: str
    active: bool = True
    ended_on: date | None = None
    as_candidate: str | None = None

    


