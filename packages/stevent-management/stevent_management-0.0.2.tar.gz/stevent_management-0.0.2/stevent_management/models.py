from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel, Field, field_validator
from uuid import uuid4
import os
from enum import Enum
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

from typing import Optional
from stevent_management.db import counters_collection


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
my_secret = os.getenv("JWT_SECRET", "your-secret-key")

ALGORITHM = "HS256"



def generate_id(event_name: str) -> int:
    # Use a separate counter for each event
    result = counters_collection.find_one_and_update(
        {"_id": f"seat_number_{event_name}"},  # Scope by event
        {"$inc": {"sequence_value": 1}},       # Increment the `sequence_value` field
        upsert=True,                           # Create the document if it doesn't exist
        return_document=True                   # Return the updated document
    )
    return result["sequence_value"]            #function returns the value of the document sequence_value field





class Ticket(str, Enum):
    regular = "regular"
    VIP ="VIP"
    VVIP = "VVIP"




# Event_Manager Model
class EventManager(BaseModel):
    username: str
    password: str
     
    @staticmethod
    def hash_password(password: str):
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password (plain_password: str, hashed_password:str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)



    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
        if not my_secret:
            raise ValueError("JWT_SECRET is not set.")
        payload = data.copy()
        payload["exp"] = datetime.utcnow() + expires_delta
        return jwt.encode(payload, my_secret, algorithm=ALGORITHM)

    @staticmethod
    def decode_access_token(token: str):
        if not my_secret:
            raise ValueError("JWT_SECRET is not set.")
        try:
            decoded_token = jwt.decode(token, my_secret, algorithms=[ALGORITHM])
            return decoded_token if decoded_token["exp"] >= datetime.utcnow().timestamp() else None
        except jwt.PyJWTError:
            return None



class Event(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid4()))  # Generate UUID for event_id
    event_name: str
    description: str
    event_date: str
    age_range:str
    

    @property
    def age_min(self) -> int:
        return int(self.age_range.split("-")[0])

    @property
    def age_max(self) -> int:
        return int(self.age_range.split("-")[1])

    @field_validator("age_range")
    def validate_age_range(cls, v):
        """ Ensure age_range follows the pattern 'min-max' like '18-25' """
        if not v or "-" not in v:
            raise ValueError("Age range must be in the format 'min-max'.")
        age_min, age_max = v.split("-")
        if not age_min.isdigit() or not age_max.isdigit():
            raise ValueError("Both age_min and age_max must be integers.")
        if int(age_min) > int(age_max):
            raise ValueError("Age min cannot be greater than age max.")
        return v


class Profiler(BaseModel):
    id: int = Field(default_factory=lambda: abs(hash(uuid4())) % 10**8)
    seat_number: Optional[int] = None  
    username: str
    age: int
    ticket: Ticket
    gender: str
    event: Event  # Nested Event object


    def __init__(self, **data): #additional customization for Profiler model
        # Initialize BaseModel in usual pydantic model manner, since BaseModel is Parent
        super().__init__(**data)

        # Dynamically generate seat_number scoped by event_name
        self.seat_number = generate_id(self.event.event_name)

        # Validate the guest's age
        self.validate_age(self.age, self.event)


    @classmethod
    def validate_age(cls, age: int, event: Event):
        """Ensure that the guest's age falls within the event's age range."""
        if not (event.age_min <= age <= event.age_max):
            raise ValueError(
                f"Guest age {age} is not within the allowed range ({event.age_min}-{event.age_max}) for the event '{event.event_name}'."
            )
        return age





