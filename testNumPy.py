import numpy as np


def first_subarray(full_array, sub_array):
    n = len(full_array)
    k = len(sub_array)
    matches = np.where([(
        full_array[start_ix] == sub_array[0]
        and full_array[start_ix + 2] == sub_array[2]
        and full_array[start_ix + 3] == sub_array[3]
    ) for start_ix in range(0, n - k + 1)])
    return matches


# arr = [1, 2, 3, 1, 3, 1, 2, 4]
# arr2 = np.array([1, 3, 1])
# indexTemp = np.where( arr[:1] == 3 )
# print(indexTemp)


a = [0, 1, 2, 3, 4, 5, 6, 1, 3, 3, 4]
b = [1, 0, 3, 4]
c = np.append(a, b)
print(c)
print(first_subarray(a, b))
