import collections
from typing import Any

from slickconf.builder import import_to_str
from slickconf.constants import INIT_KEY, FN_KEY, TARGET_KEY


def traverse(node):
    if isinstance(node, collections.abc.Sequence) and not isinstance(node, str):
        for n in node:
            yield from traverse(n)

    elif isinstance(node, collections.abc.Mapping):
        for v in node.values():
            yield from traverse(v)

        yield node


class NodeSelection:
    def __init__(self, node, fn_or_cls):
        self.node = node
        self.fn_or_cls = import_to_str(fn_or_cls)

    def __iter__(self):
        for node in traverse(self.node):
            if INIT_KEY in node:
                target = node[INIT_KEY]

            elif FN_KEY in node:
                target = node[FN_KEY]

            else:
                target = node[TARGET_KEY]

            if target == self.fn_or_cls:
                yield node

    def replace(self, target):
        new_fn_or_cls = import_to_str(target)

        for node in self:
            if INIT_KEY in node:
                node[INIT_KEY] = new_fn_or_cls

            elif FN_KEY in node:
                node[FN_KEY] = new_fn_or_cls

            else:
                node[TARGET_KEY] = new_fn_or_cls

    def set(self, **kwargs):
        for node in self:
            for key, value in kwargs.items():
                node[key] = value

    def set_args(self, args: dict[int, Any]):
        for node in self:
            if "__args" not in node:
                continue

            for k, v in args.items():
                node["__args"][k] = v

    def get(self, key):
        for node in self:
            if key in node:
                yield node[key]

    def get_args(self, index=None):
        for node in self:
            if "__args" not in node:
                continue

            if index is None:
                yield node["__args"]

            else:
                yield node["__args"][index]


class TagSelection:
    def __init__(self, node, tag):
        self.node = node
        self.tag = tag

    def __iter__(self):
        tag_key = "__tag"

        for node in traverse(self.node):
            for key, value in node.items():
                if isinstance(value, collections.abc.Mapping) and tag_key in value:
                    if value[tag_key] == self.tag:
                        yield node, key, None

                elif isinstance(value, collections.abc.Sequence):
                    for index, elem in enumerate(value):
                        if (
                            isinstance(elem, collections.abc.Mapping)
                            and tag_key in elem
                        ):
                            if elem[tag_key] == self.tag:
                                yield node, key, index

    def replace(self, value):
        for node, key, index in self:
            if index is None:
                node[key] = value

            else:
                node[key][index] = value


def select(node, fn_or_cls=None, tag=None):
    assert (
        fn_or_cls is None or tag is None
    ), "fn_or_cls and tag cannot be both specified"

    if fn_or_cls is not None:
        return NodeSelection(node, fn_or_cls)

    else:
        return TagSelection(node, tag)
