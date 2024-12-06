import argparse
import unittest

import ddt
import pytest

from iker.common.utils.argutils import ParserTree


def dummy_parser_tree():
    parser_tree = ParserTree(argparse.ArgumentParser(description="dummy argument parser", exit_on_error=False))

    for command_chain in [
        [],
        ["foo"],
        ["foo", "bar"],
        ["foo", "baz"],
        ["bar"],
        ["bar", "foo"],
        ["bar", "baz"],
        ["baz", "foo"],
        ["baz", "bar"],
        ["baz", "bar", "foo"],
    ]:
        parser = parser_tree.add_subcommand_parser(command_chain, exit_on_error=False)

        option_infix = "-".join(command_chain)
        if len(option_infix) == 0:
            option_infix = "x"

        parser.add_argument(f"--option-{option_infix}-str", type=str, default="")
        parser.add_argument(f"--option-{option_infix}-int", type=int, default=0)
        parser.add_argument(f"--option-{option_infix}-float", type=float, default=0.0)
        parser.add_argument(f"--option-{option_infix}-switch", action="store_true")
        parser.add_argument(f"--option-{option_infix}-nargs", type=str, action="append", default=[])

    return parser_tree


@ddt.ddt
class ArgUtilsTest(unittest.TestCase):

    @ddt.data(
        (
            [],
            [],
            [
                ("option_x_str", ""),
                ("option_x_int", 0),
                ("option_x_float", 0.0),
                ("option_x_switch", False),
                ("option_x_nargs", []),
            ],
        ),
        (
            [
                "--option-x-str", "dummy",
                "--option-x-int", "1",
                "--option-x-float", "1e6",
                "--option-x-switch",
                "--option-x-nargs", "dummy_1",
                "--option-x-nargs", "dummy_2",
            ],
            [],
            [
                ("option_x_str", "dummy"),
                ("option_x_int", 1),
                ("option_x_float", 1e6),
                ("option_x_switch", True),
                ("option_x_nargs", ["dummy_1", "dummy_2"]),
            ],
        ),
        (
            ["foo"],
            ["foo"],
            [
                ("option_foo_str", ""),
                ("option_foo_int", 0),
                ("option_foo_float", 0.0),
                ("option_foo_switch", False),
                ("option_foo_nargs", []),
            ],
        ),
        (
            [
                "foo", "baz",
                "--option-foo-baz-str", "dummy",
                "--option-foo-baz-int", "1",
                "--option-foo-baz-float", "1e6",
                "--option-foo-baz-switch",
                "--option-foo-baz-nargs", "dummy_1",
                "--option-foo-baz-nargs", "dummy_2",
            ],
            ["foo", "baz"],
            [
                ("option_foo_baz_str", "dummy"),
                ("option_foo_baz_int", 1),
                ("option_foo_baz_float", 1e6),
                ("option_foo_baz_switch", True),
                ("option_foo_baz_nargs", ["dummy_1", "dummy_2"]),
            ],
        ),
        (
            [
                "baz", "foo",
                "--option-baz-foo-str", "dummy",
                "--option-baz-foo-int", "1",
                "--option-baz-foo-float", "1e6",
                "--option-baz-foo-switch",
                "--option-baz-foo-nargs", "dummy_1",
                "--option-baz-foo-nargs", "dummy_2",
            ],
            ["baz", "foo"],
            [
                ("option_baz_foo_str", "dummy"),
                ("option_baz_foo_int", 1),
                ("option_baz_foo_float", 1e6),
                ("option_baz_foo_switch", True),
                ("option_baz_foo_nargs", ["dummy_1", "dummy_2"]),
            ],
        ),
        (
            [
                "baz", "bar", "foo",
                "--option-baz-bar-foo-str", "dummy",
                "--option-baz-bar-foo-int", "1",
                "--option-baz-bar-foo-float", "1e6",
                "--option-baz-bar-foo-switch",
                "--option-baz-bar-foo-nargs", "dummy_1",
                "--option-baz-bar-foo-nargs", "dummy_2",
            ],
            ["baz", "bar", "foo"],
            [
                ("option_baz_bar_foo_str", "dummy"),
                ("option_baz_bar_foo_int", 1),
                ("option_baz_bar_foo_float", 1e6),
                ("option_baz_bar_foo_switch", True),
                ("option_baz_bar_foo_nargs", ["dummy_1", "dummy_2"]),
            ],
        ),
    )
    @ddt.unpack
    def test_parser_tree(self, args, expect_commands, expect_options):
        commands, args = dummy_parser_tree().parse_args(args)
        self.assertEqual(commands, expect_commands)
        for key, value in expect_options:
            self.assertEqual(getattr(args, key), value)

    @ddt.data(
        (["foo", "foo"],),
        (["foo", "--option-x-switch"],),
        (["foo", "bar", "--option-bar-foo-switch"],),
        (["baz", "foo", "bar"],),
    )
    @ddt.unpack
    def test_parser_tree__exception(self, args):
        with pytest.raises(argparse.ArgumentError):
            dummy_parser_tree().parse_args(args)
