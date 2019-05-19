fruitPrices = {"apples": 2.00, "oranges": 5.00, "pears":3.00}

def calcPrice(fruit, numPounds):
    if fruit not in fruitPrices:
        print 'we don''t have %s' % (fruit)
    else:
        price = fruitPrices[fruit] * numPounds
        print 'That''ll be $%s' % (price)

def quickSort(list, start, end):
    if (start >= end):
        return list

    pivot = list[0]
    i = start + 1
    j = end - 1
    while (i <= j & list[i] < pivot):
        i = i + 1

    while (j >= i & list[j] > pivot):
        j = j + 1

    temp = list[j]
    list[j] = list[0]
    list[0] = temp


    return quickSort(list, 0, j - 1)
    return quickSort(list, j + 1, len(list))



# Main Function
if __name__ == '__main__':
    x = [9, 8, 7, 5, 13, 18]
    print quickSort(x, 0, len(x))

