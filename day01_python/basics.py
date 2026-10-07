# Variabes and f-strings
name = "Sijo"
years = 12
print(f"{name} has {years} years of experience")

# Lists and dicts
skills = ["React","Typescript","Java"]
skills.append("Python")
profile={"name":name,"skills":skills}
print(profile["skills"][-1])
print(profile.get("city","Bengaluru"))

# Comprehensions
upper =  [s.upper() for s in skills]
long_ones =  [s for s in skills if len(s)>5]
print(upper,long_ones)

for i, skill in enumerate(skills):  # index + value
    print(i,skill)

# Functions: default and keyword arguments
def greet(name: str, role: str="engineer")->str:
    return f"Hi {name}, the role {role}"

print(greet("Sijo"))
print(greet(role="AI-Engineer", name="Sijo"))

# Destructing and spread
first, *rest = skills
merged = {**profile,"city":"Bengaluru"}
print(first,rest,merged["city"])

# Truthiness: None, [], "", {}, 0 are all falsy
value = None
if not value:
    print("empty")

# Comprehension that returns only the skills containing the letter "a", in lowercase
filtered_skills =  [s.lower() for s in skills if "a" in s.lower()]
print(filtered_skills)