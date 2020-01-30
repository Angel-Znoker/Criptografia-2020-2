import fileinput

numbers = []

for line in fileinput.input():
	numbers.append(float(line))

result = sum(numbers)

if result % 1 == 0:
	print(int(result))
else:
	print(result)
