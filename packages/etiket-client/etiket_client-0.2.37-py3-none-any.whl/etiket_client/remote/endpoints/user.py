from etiket_client.remote.client import client
from etiket_client.remote.endpoints.models.user import UserReadWithScopes, UserRead, UserCreate, UserType, UserUpdate, UserUpdateMe

from typing import List

def create_user(data: UserCreate):
    client.post("/user/", json_data=data.model_dump(mode="json"))
    
def read_user(username : str) -> UserReadWithScopes:
    response = client.get("/user/", params={"username": username})
    return UserReadWithScopes.model_validate(response)

def read_users(name_query : str = None, user_type : UserType = None) -> List[UserRead]:
    response = client.get("/users/", params={"name":name_query, "user_type": user_type})
    return [UserRead.model_validate(user) for user in response]

def user_read_me() -> UserReadWithScopes:
    response = client.get("/user/me/")
    return UserReadWithScopes.model_validate(response)

def user_update_me(username : str, data: UserUpdateMe):
    client.patch("/user/me", params = {"username": username},json_data=data.model_dump(mode="json"))

def update_user(username : str, data: UserUpdate):
    client.patch("/user", params = {"username": username},  json_data=data.model_dump(mode="json"))
    
def delete_user(username : str):
    client.delete("/user/", params={"username": username})