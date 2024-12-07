def remove_duplicates(input_list):
    return list(set(input_list))

def flat_list(nested_list):
    result_list = []
    for item in nested_list:
        if isinstance(item, list):
            result_list.extend(flat_list(item))
        else:
            result_list.append(item)
    return result_list


from list_operations import remove_duplicates, flat_list

number = [10,10,20,30,30,40,50,50]
my_nested = [[1,[2, 3]], [4, 5, 6], [7,[8],9]]

print("remove_duplicate:", remove_duplicates(number))
print("Flatten_list:", flat_list(my_nested))
