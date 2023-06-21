
f = open("airport-codes-part.csv", "r")
for line in f:
    line = line.strip()
    if line:
        print(line.strip())
