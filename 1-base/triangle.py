size = 6

print('正三角, size(', size, ')')
for i in range(size):
    row = ''
    for j in range(i+1):
        row += '*'
    print(row)

print('\n倒三角, size(', size, ')')

for i in range(size):
    row = ''
    for j in range(size - i):
        row += '*'
    print(row)