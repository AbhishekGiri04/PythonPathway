a={
    1:'one',
    2:'two',
    3:'three',
    "one":"Abhishek",
    "two":"Rohit",
    "arr":[1,2,3,4,5]
}

b={}
print(a)
print(type(a))
print(a[1])
print(a["arr"])

# Dictionary Methods
print(a.items())
print(a.keys())
a.update({"two": "Rahul"})
print(a)
print(a.get("name"))
print(a.get("one"))