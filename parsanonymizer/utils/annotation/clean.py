import tqdm

names = []

with open('./W_CITY.txt', 'r', encoding='utf-8') as f:
    line = f.readline()
    while line:
        names.append(line)
        line = f.readline()

print(len(names))

with open('W_CITY_CLEANED.txt', 'w', encoding='utf-8') as f:
    for city in sorted(list(set(names))):
        f.write(f'{city}')