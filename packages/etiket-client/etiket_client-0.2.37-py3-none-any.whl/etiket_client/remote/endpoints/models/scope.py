from etiket_client.remote.endpoints.models.utility import convert_time_from_utc_to_local

from etiket_client.remote.endpoints.models.S3 import S3BucketInfo
from etiket_client.remote.endpoints.models.schema_base import SchemaRead
from etiket_client.remote.endpoints.models.user_base import UserRead
from etiket_client.remote.endpoints.models.types import scopestr

from typing import Optional, List
from pydantic import BaseModel, Field, field_validator

import datetime, uuid



class ScopeBase(BaseModel):
    name : scopestr
    uuid : uuid.UUID
    description: str

class ScopeCreate(ScopeBase):
    bucket_uuid : uuid.UUID

class ScopeReadNoSchema(ScopeBase):
    archived: bool

class ScopeRead(ScopeReadNoSchema):    
    created: datetime.datetime
    modified: datetime.datetime
    
    bucket : S3BucketInfo
    schema_: Optional["SchemaRead"] = Field(alias="schema")
    
    @field_validator('created', mode='before')
    @classmethod
    def convert_created_time_utc_to_local(cls, created : datetime.datetime):
        return convert_time_from_utc_to_local(created)
    
    @field_validator('modified', mode='before')
    @classmethod
    def convert_modified_time_utc_to_local(cls, modified : datetime.datetime):
        return convert_time_from_utc_to_local(modified)
    

class ScopeReadWithUsers(ScopeRead):
    users : List["UserRead"]

class ScopeUpdate(BaseModel):
    name : Optional[scopestr] = Field(default = None)
    description: Optional[str] = Field(default = None)
    archived: Optional[bool] = Field(default = None)

class ScopeDelete(BaseModel):
    uuid : uuid.UUID