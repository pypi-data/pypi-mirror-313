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


