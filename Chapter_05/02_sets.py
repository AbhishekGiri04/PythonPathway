s1=set()

print(s1)
print(type(s1))

# Sets Methods
s = {1,8,2,3}
print(s)
print(len(s))
s.remove(8)
print(s)
s.pop()
print(s)
s.clear()
print(s)

set1={1,2,3,4,5}
set2={11,2,34,4,5}
print(set1.union(set2))
print(set1.intersection(set2))