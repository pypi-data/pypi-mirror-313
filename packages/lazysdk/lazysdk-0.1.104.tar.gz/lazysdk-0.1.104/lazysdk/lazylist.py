

def split(
        list_in: list,
        split_gap: int
):
    """
    将输入的list按照split_gap进行分割
    """
    list_out = list()
    split_num = 0
    for i in range(len(list_in)):
        if i % split_gap == 0:
            list_out.append(list())
            split_num += 1
        list_out[split_num-1].append(list_in[i])
    return list_out
