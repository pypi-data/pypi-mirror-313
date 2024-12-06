from __future__ import annotations
import os
from typing import Optional
from holytools.fsys.resource import FsysResource, is_hidden
# -------------------------------------------

class FsysNode(FsysResource):
    def __init__(self, path : str, parent : Optional[FsysNode] = None):
        super().__init__(path=path)
        self._cached_children : Optional[list[FsysNode]] = None
        self._cached_parent : Optional[FsysNode] = parent

    # -------------------------------------------
    # descendants

    def add_child(self, path : str) -> FsysNode:
        if self._cached_children is None:
            self._cached_children = []
        child = FsysNode(path=path, parent=self)
        self._cached_children.append(child)
        return child

    # noinspection DuplicatedCode
    def get_tree(self, max_depth : Optional[int] = None, max_size : Optional[int] = None, **kwargs) -> FsysTree:
        # noinspection DuplicatedCode
        def get_subdict(node : FsysNode, depth : int) -> dict:
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
        return FsysTree(get_subdict(node=self, depth=0))


    def get_file_subnodes(self, select_formats: Optional[list[str]] = None) -> list[FsysNode]:
        file_subnodes = [des for des in self.get_subnodes() if des.is_file()]
        if select_formats is not None:
            fmts_without_dots = [fmt.replace('.', '') for fmt in select_formats]
            file_subnodes = [node for node in file_subnodes if node.get_suffix() in fmts_without_dots]
        return file_subnodes


    def get_subnodes(self, follow_symlinks: bool = True) -> list[FsysNode]:
        path_to_node = {self.get_path(): self}

        for root, dirs, files in os.walk(self.get_path(), followlinks=follow_symlinks):
            parent_node = path_to_node.get(root)
            for name in dirs+files:
                path = os.path.join(root, name)

                is_resource = os.path.isfile(path) or os.path.isdir(path)
                if path in path_to_node or not is_resource:
                    continue
                try:
                    path_to_node[path] = parent_node.add_child(path)
                except FileNotFoundError:
                    continue

        return list(path_to_node.values())


    def get_child_nodes(self, exclude_hidden : bool = False) -> list[FsysNode]:
        if not self._cached_children is None:
            return self._cached_children
        self._cached_children = []
        if not self.is_dir():
            return self._cached_children

        child_paths = [os.path.join(self.get_path(), name) for name in os.listdir(path=self.get_path())]
        for path in child_paths:
            if exclude_hidden and is_hidden(path):
                continue
            try:
                self.add_child(path=path)
            except:
                continue

        return self._cached_children

    # -------------------------------------------
    # ancestors

    def get_parent(self) -> Optional[FsysNode]:
        if self.is_root():
            return None

        if self._cached_parent is None:
            self._cached_parent = FsysNode(path=str(self._path_wrapper.parent))
        return self._cached_parent

    def is_root(self):
        return self._path_wrapper.parent == self._path_wrapper


    def __str__(self):
        return self.get_name()

# noinspection DuplicatedCode
class FsysTree(dict[FsysNode, dict]):
    def as_str(self) -> str:
        return nested_dict_as_str(nested_dict=self)

    def get_size(self) -> int:
        return get_total_elements(nested_dict=self)

    @classmethod
    def join_trees(cls, root : FsysNode, subtrees : list[FsysTree]):
        the_dict = { root : {}}
        sub_dict = the_dict[root]
        for subtree in subtrees:
            sub_dict.update(subtree)
        return FsysTree(the_dict)

# noinspection DuplicatedCode
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