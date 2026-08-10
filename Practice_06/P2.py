a = int(input("Enter marks for subject 1: "))
b = int(input("Enter marks for subject 2: "))
c = int(input("Enter marks for subject 3: "))

percentage = ((a + b + c) / 300) * 100

if percentage >= 40 and a >= 33 and b >= 33 and c >= 33:
    print("Pass")

elif a < 33 and b < 33 and c < 33:
    print("Fail due to marks less than 33 in all subjects")

elif a < 33 or b < 33 or c < 33:
    print("Fail due to marks less than 33")

else:
    print("Fail due to percentage less than 40%")