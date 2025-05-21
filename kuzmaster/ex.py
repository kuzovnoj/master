def linear(nested_lists):
    sp1 = []
    def recurs(nested_lists):
        if isinstance(nested_lists, int):
            sp1.append(nested_lists)
        else:
            for i in nested_lists:
                if isinstance(i, int):
                    sp1.append(i)
                else:
                    recurs(i)

    recurs(nested_lists)            
    return sp1

my_list = [1, [4, 4], 2, [1, [2, 10]]]

print(recursive_sum(my_list))
