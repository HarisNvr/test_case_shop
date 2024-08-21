def sec(n):
    sequence = ''
    count = 1
    while count <= n and len(sequence) <= n:
        sequence += (str(count)*count)
        count += 1

    return sequence[:n]


print(sec(20))
