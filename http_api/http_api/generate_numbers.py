import random


def get_random_number():
    return int(random.random() * 100)


with open("numbers.txt", "w") as file:
    for _ in range(1, 500):
        file.write(str(get_random_number()) + " ")
