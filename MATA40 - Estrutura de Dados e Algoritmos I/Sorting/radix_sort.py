def radix_sort(vector, max_, range_):
    for digit in range(max_ - 1, -1, -1):
        aux_vector = [list() for i in range(range_)]
        
        for element in vector:
            value = ord(element[digit])
            index = value - (48 if value < 65 else 55)

            aux_vector[index].append(element)

        vector = []

        for elements in aux_vector:
            for element in elements:
                vector.append(element)
    return vector
