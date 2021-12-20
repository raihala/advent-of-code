def enhance_once(image, enhancement_key):
    height = len(image)
    width = len(image[0])

    # determine whether the infinite grid should be
    # filled with 0s or 1s
    if image[0][0] == 0:
        border = enhancement_key[0]
    else:
        border = enhancement_key[-1]

    res = [[border] * width]
    for i in range(1, height-1):
        res_row = [border]
        for j in range(1, width-1):
            index = (image[i-1][j-1] * 256 + image[i-1][j] * 128 + image[i-1][j+1] * 64 +
                     image[i][j-1] * 32 + image[i][j] * 16 + image[i][j+1] * 8 +
                     image[i+1][j-1] * 4 + image[i+1][j] * 2 + image[i+1][j+1])
            res_row.append(enhancement_key[index])
        res_row.append(border)
        res.append(res_row)

    res.append([border] * width)
    return res


def enhance(image, n, enhancement_key):
    width = len(image[0])

    res = [[0] * (width + 2*n + 2)] * (n + 1)
    for row in image:
        res.append([0] * (n + 1) + row + [0] * (n + 1))
    res.extend([[0] * (width + 2*n + 2)] * (n + 1))

    for _ in range(n):
        res = enhance_once(res, enhancement_key)

    return res


with open('input') as f:
    enhancement_key = [0 if c == '.' else 1 for c in next(f).strip()]
    next(f)
    image = []
    for line in f:
        image_row = [0 if c == '.' else 1 for c in line.strip()]
        image.append(image_row)

part_1_image = enhance(image, 2, enhancement_key)
part_1_res = sum([sum(row) for row in part_1_image])
print(part_1_res)

part_2_image = enhance(image, 50, enhancement_key)
part_2_res = sum([sum(row) for row in part_2_image])
print(part_2_res)
