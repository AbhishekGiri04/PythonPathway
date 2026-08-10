text = input("Enter your comment: ")

if ("make a lot of money" in text or
    "buy now" in text or
    "subscribe this" in text or
    "click this" in text):
    
    print("This is spam")

else:
    print("This is not spam")