from dataclasses import dataclass, field
from typing import Literal

def total_cost(tokens: int, price_per_million:float)->float:
    return tokens/1_000_000*price_per_million

scores : list[int] = [90,80]
city: str| None = None
Role = Literal["user","asistant","system"]

@dataclass
class Message:
    role :  Role
    content:  str

@dataclass
class Converstion:
    id: str
    message: list[Message] =  field(default_factory=list)

    def add(self, role: Role, content: str)-> None:
        self.message.append(Message(role,content))

    @property
    def turns(self)-> int:
        return len(self.message)

chat =  Converstion(id="c1")
chat.add("user","What is RAG?")
chat.add("asistant","Retrieval-augmented generation...")
print (chat.turns)
print(chat.message[0])
print(f"{total_cost(250_000,3.0):.2f} USD")

chat.add("bot","hi")
print(chat.turns)
chat.add("user", "Another question")
print(chat.turns)
print(Message("user", "hi") == Message("user", "hi"))
