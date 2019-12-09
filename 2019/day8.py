WIDTH = 25
HEIGHT = 6

with open('day-8-input.txt') as f:
    data = f.readline().strip()

layers = [data[x:x+(WIDTH*HEIGHT)] for x in range(0, len(data), WIDTH*HEIGHT)]

# Part 1
layer = min(layers, key=lambda x: x.count('0'))
checksum = layer.count('1') * layer.count('2')
print(checksum)

# Part 2
pixels = []
for i in range(WIDTH*HEIGHT):
    for layer in layers:
        pixel = layer[i]
        if pixel == '0':  # black
            pixels.append('.')
            break
        elif pixel == '1':  # white
            pixels.append('X')
            break

rows = [pixels[x:x+WIDTH] for x in range(0, WIDTH*HEIGHT, WIDTH)]
for row in rows:
    print(''.join(row))
