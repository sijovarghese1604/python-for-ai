import ollama
from pydantic import BaseModel

MODEL = "llama3.2"

class Person(BaseModel):
    name: str
    city: str
    years_experience: int

text = "Hi, I'm Sijo from Bengaluru. I've been building frontends for about 12 years."

response = ollama.chat(
    model=MODEL,
    messages=[{"role": "user", "content": f"Extract the person's details from this text:\n{text}"}],
    format=Person.model_json_schema(),      # <-- the JSON shape the model must follow
    options={"temperature": 0},
)

raw = response.message.content or ""
print("RAW TEXT FROM MODEL:", raw)

person = Person.model_validate_json(raw)    # string -> validated Python object
print("PYTHON OBJECT:", person)
print("Years + 1 =", person.years_experience + 1)   # it's a real int now