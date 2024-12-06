# depth [item] = [dist_from_root]
def get_dict_depth(the_dict : dict, dist_from_root = 0) -> int:
    max_dist = 0
    for value in the_dict.values():
        item_dist = get_dict_depth(value, dist_from_root=dist_from_root+1) if isinstance(value, dict) else dist_from_root+1
        max_dist = max(item_dist, max_dist)
    return max_dist