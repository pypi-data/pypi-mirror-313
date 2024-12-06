from compextAI.api.api import APIClient
from datetime import datetime

class Message:
    message_id: str
    thread_id: str
    content: any
    role: str
    metadata: dict
    created_at: datetime
    updated_at: datetime

    def __init__(self,content:any, role:str, message_id:str='', thread_id:str='', metadata:dict={}, created_at:datetime=None, updated_at:datetime=None):
        self.message_id = message_id
        self.thread_id = thread_id
        self.content = content
        self.role = role
        self.metadata = metadata
        self.created_at = created_at
        self.updated_at = updated_at

    def __str__(self):
        return f"Message(message_id={self.message_id}, thread_id={self.thread_id}, content={self.content}, role={self.role}, metadata={self.metadata})"
    
    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "role": self.role,
            "metadata": self.metadata,
            "message_id": self.message_id,
            "thread_id": self.thread_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

def get_message_object_from_dict(data:dict) -> Message:
    return Message(data["content"], data["role"], data["identifier"], data["thread_id"], data["metadata"], data["created_at"], data["updated_at"])

def list_all(client:APIClient, thread_id:str) -> list[Message]:
    response = client.get(f"/message/thread/{thread_id}")

    status_code: int = response["status"]
    data: dict = response["data"]
    
    if status_code != 200:
        raise Exception(f"Failed to list messages, status code: {status_code}, response: {data}")
    
    return [get_message_object_from_dict(message) for message in data]

def retrieve(client:APIClient, message_id:str) -> Message:
    response = client.get(f"/message/{message_id}")

    status_code: int = response["status"]
    data: dict = response["data"]
    
    if status_code != 200:
        raise Exception(f"Failed to retrieve message, status code: {status_code}, response: {data}")
    
    return get_message_object_from_dict(data)

def create(client:APIClient, thread_id:str, messages:list[Message]) -> list[Message]:
    response = client.post(f"/message/thread/{thread_id}", data={"messages": [message.to_dict() for message in messages]})

    status_code: int = response["status"]
    data: dict = response["data"]
    
    if status_code != 200:
        raise Exception(f"Failed to create message, status code: {status_code}, response: {data}")
    
    return [get_message_object_from_dict(message) for message in data]

def update(client:APIClient, message_id:str, content:any, role:str, metadata:dict={}) -> Message:
    response = client.put(f"/message/{message_id}", data={"content": content, "role": role, "metadata": metadata})

    status_code: int = response["status"]
    data: dict = response["data"]
    
    if status_code != 200:
        raise Exception(f"Failed to update message, status code: {status_code}, response: {data}")
    
    return get_message_object_from_dict(data)

def delete(client:APIClient, message_id:str) -> bool:
    response = client.delete(f"/message/{message_id}")
    return response["status"] == 204
