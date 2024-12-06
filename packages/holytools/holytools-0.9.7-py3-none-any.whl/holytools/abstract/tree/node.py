from __future__ import annotations
from typing import Optional
from abc import abstractmethod, ABC

# -------------------------------------------


class TreeNode(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    # noinspection DuplicatedCode
    def get_tree(self, max_depth : Optional[int] = None, max_size : Optional[int] = None, **kwargs) -> Tree:
        # noinspection DuplicatedCode
        def get_subdict(node : TreeNode, depth : int) -> dict:
            nonlocal root_size
            the_dict = {node : {}}
            root_size += 1

            depth_ok = depth <= max_depth if not max_depth is None else True
            size_ok = root_size <= max_size if not max_size is None else True

            if not depth_ok:
                raise ValueError(f'Exceeded max depth of {max_depth}')
            if not size_ok:
                raise ValueError(f'Exceeded max size of {max_size}')

            child_nodes = node.get_child_nodes(**kwargs)
            for child in child_nodes:
                subtree = get_subdict(node=child, depth=depth+1)
                the_dict[node].update(subtree)
            return the_dict

        root_size = 0
        return Tree(get_subdict(node=self, depth=0))

    # -------------------------------------------
    # descendants

    def get_subnodes(self, *args, **kwargs) -> list[TreeNode]:
        _, __ = args, kwargs
        subnodes = []
        for child in self.get_child_nodes():
            subnodes.append(child)
            subnodes += child.get_subnodes()
        return subnodes

    @abstractmethod
    def get_child_nodes(self, *args, **kwargs) -> list[TreeNode]:
        pass

    # -------------------------------------------
    # ancestors

    def get_ancestors(self) -> list[TreeNode]:
        current = self
        ancestors = []
        while current.get_parent():
            ancestors.append(current.get_parent())
            current = current.get_parent()
        return ancestors

    @abstractmethod
    def get_parent(self) -> Optional[TreeNode]:
        pass

    def get_root(self) -> TreeNode:
        current = self
        while current.get_parent():
            current = current.get_parent()
        return current

    def __str__(self):
        return self.get_name()



class Tree(dict[TreeNode, dict]):
    def as_str(self) -> str:
        return nested_dict_as_str(nested_dict=self)

    def get_size(self) -> int:
        return get_total_elements(nested_dict=self)

    @classmethod
    def join_trees(cls, root : TreeNode, subtrees : list[Tree]):
        the_dict = { root : {}}
        sub_dict = the_dict[root]
        for subtree in subtrees:
            sub_dict.update(subtree)
        return Tree(the_dict)


def nested_dict_as_str(nested_dict: dict, prefix='') -> str:
    output = ''
    for index, (key, value) in enumerate(nested_dict.items()):
        is_last = index == len(nested_dict) - 1
        new_prefix = prefix + ('    ' if is_last else '│   ')
        connector = '└── ' if is_last else '├── '
        output += f'{prefix}{connector}{key}\n'
        output += nested_dict_as_str(nested_dict=value, prefix = new_prefix)
    return output

def get_total_elements(nested_dict : dict) -> int:
    count = 0
    for key, value in nested_dict.items():
        count += 1
        if isinstance(value, dict):
            count += get_total_elements(value)
    return count

