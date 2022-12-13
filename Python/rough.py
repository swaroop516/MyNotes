import os

print(f"Current working directory {os.getcwd()}")
l = [8, 4, 5, 0, 8, 10, 12]

sum = 0
for i in l:
    sum += i

print(f"sum of the list {sum}")
