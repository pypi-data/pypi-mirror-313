import argparse

__all__ = [
    "ParserTreeNode",
    "ParserTree",
]


class ParserTreeNode(object):
    def __init__(self, command: str, parser: argparse.ArgumentParser):
        self.command = command
        self.parser = parser
        self.subparsers = None
        self.child_nodes: list[ParserTreeNode] = []


def construct_parser_tree(
    root_node: ParserTreeNode,
    command_chain: list[str],
    command_key_prefix: str,
    **kwargs,
) -> list[ParserTreeNode]:
    node_path = [root_node]
    if len(command_chain) == 0:
        return node_path

    node = root_node
    for depth, command in enumerate(command_chain):
        if node.subparsers is None:
            node.subparsers = node.parser.add_subparsers(dest=f"{command_key_prefix}:{depth}")
        for child_node in node.child_nodes:
            if child_node.command == command:
                node = child_node
                break
        else:
            if depth == len(command_chain) - 1:
                child_parser = node.subparsers.add_parser(command, **kwargs)
            else:
                child_parser = node.subparsers.add_parser(command)
            child_node = ParserTreeNode(command, child_parser)
            node.child_nodes.append(child_node)
            node = child_node
        node_path.append(node)

    return node_path


class ParserTree(object):
    def __init__(self, root_parser: argparse.ArgumentParser, command_key_prefix: str = "command"):
        self.root_node = ParserTreeNode("", root_parser)
        self.command_key_prefix = command_key_prefix

    def add_subcommand_parser(self, command_chain: list[str], **kwargs) -> argparse.ArgumentParser:
        *_, last_node = construct_parser_tree(self.root_node, command_chain, self.command_key_prefix, **kwargs)
        return last_node.parser

    def parse_args(self, args: list[str] | None = None) -> tuple[list[str], argparse.Namespace]:
        # Before Python 3.12 the 'exit_on_error' attribute does not take effect properly
        # if unknown arguments encountered. We have to employ this workaround
        # TODO: remove this workaround when bumping the Python versions to above Python 3.12
        if self.root_node.parser.exit_on_error:
            known_args_namespace = self.root_node.parser.parse_args(args)
        else:
            known_args_namespace, unknown_args = self.root_node.parser.parse_known_args(args)
            if len(unknown_args or []) > 0:
                raise argparse.ArgumentError(None, "unrecognized arguments: %s" % " ".join(unknown_args))

        command_pairs = []
        namespace = argparse.Namespace()
        for key, value in dict(vars(known_args_namespace)).items():
            if key.startswith(self.command_key_prefix) and value is not None:
                command_pairs.append((key, value))
            else:
                setattr(namespace, key, value)

        return list(command for _, command in sorted(command_pairs)), namespace
