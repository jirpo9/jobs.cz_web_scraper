"""numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Hledáme první číslo, které je dělitelné 3
for num in numbers:
    remainder = num % 3  # Vypočítáme zbytek po dělení 3
    if remainder == 0:
        print(f"Found a number divisible by 3: {num}")
        break



for num in numbers:
    if (result := num) % 3 == 0:
        print(f"První číslo dělitelné třema: {num}")
        break
"""
"""
numbers = [2, 4, 6, 8, 10, 15, 20]

# Najdi první číslo větší než 10
for num in numbers:
    if num > 10:
        print(f"Found: {num}")
        break

for num in numbers:
    if (result := num) > 10:
        print(f"Toto je první číslo větší než 10: {num}")
        break
"""
"""
names = ["Alice", "Bob", "Charlie", "Dave"]

# Najdi první jméno, které má více než 4 znaky
for name in names:
    if len(name) > 4:
        print(f"Found: {name}")
        break

for name in names:
    if len(result := name) > 4:
        print(f"Found: {name}")
        break
"""

# První sudé číslo větší než 10


numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
for number in numbers:
    if number > 10 and number % 2 == 0:
        print(f"First even number greater than 10 is:{number}")
        break

for number in numbers:
    if (result := number) > 10 and number % 2 == 0:
        print(f"First even number greater than 10 is:{number}")
        break

