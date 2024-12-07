import unittest

import ddt

from iker.common.utils.dtutils import dt_utc
from iker.common.utils.strutils import is_blank, is_empty, is_none
from iker.common.utils.strutils import parse_bool, parse_float_or, parse_int_or
from iker.common.utils.strutils import parse_params_string
from iker.common.utils.strutils import str_conv
from iker.common.utils.strutils import strip_margin
from iker.common.utils.strutils import trim_to_empty, trim_to_none


@ddt.ddt
class StrUtilsTest(unittest.TestCase):

    @ddt.data(
        (None, True),
        ("", False),
        (" ", False),
        ("\t", False),
        ("dummy", False),
    )
    @ddt.unpack
    def test_is_none(self, data, expect):
        self.assertEqual(expect, is_none(data))

    @ddt.data(
        (None, True),
        ("", True),
        (" ", False),
        ("\t", False),
        ("dummy", False),
    )
    @ddt.unpack
    def test_is_empty(self, data, expect):
        self.assertEqual(expect, is_empty(data))

    @ddt.data(
        (None, True),
        ("", True),
        (" ", True),
        ("  ", True),
        ("\t", True),
        ("\n", True),
        ("dummy", False),
    )
    @ddt.unpack
    def test_is_blank(self, data, expect):
        self.assertEqual(expect, is_blank(data))

    @ddt.data(
        (None, None, None),
        ("", None, None),
        (" ", None, None),
        ("\n", None, None),
        ("\t", None, None),
        (" dummy!", None, "dummy!"),
        ("dummy! ", None, "dummy!"),
        (" dummy!", "!", " dummy"),
        ("dummy! ", "!", "dummy! "),
    )
    @ddt.unpack
    def test_trim_to_none(self, data, chars, expect):
        self.assertEqual(expect, trim_to_none(data, chars))

    @ddt.data(
        (None, None, ""),
        ("", None, ""),
        (" ", None, ""),
        ("\n", None, ""),
        ("\t", None, ""),
        (" dummy!", None, "dummy!"),
        ("dummy! ", None, "dummy!"),
        (" dummy!", "!", " dummy"),
        ("dummy! ", "!", "dummy! "),
    )
    @ddt.unpack
    def test_trim_to_empty(self, data, chars, expect):
        self.assertEqual(expect, trim_to_empty(data, chars))

    @ddt.data(
        (None, False),
        (0, False),
        (1, True),
        (2, True),
        (0.0, False),
        (1.0, True),
        (2.0, True),
        ("", False),
        ("true", True),
        ("True", True),
        ("TRUE", True),
        ("yes", True),
        ("Yes", True),
        ("YES", True),
        ("on", True),
        ("On", True),
        ("ON", True),
        ("1", True),
        ("y", True),
        ("Y", True),
        ("false", False),
        ("False", False),
        ("FALSE", False),
        ("no", False),
        ("No", False),
        ("NO", False),
        ("off", False),
        ("Off", False),
        ("OFF", False),
        ("0", False),
        ("n", False),
        ("N", False),
        (True, True),
        (False, False),
    )
    @ddt.unpack
    def test_parse_bool(self, data, expect):
        self.assertEqual(expect, parse_bool(data))

    @ddt.data(
        (False, 0),
        (True, 1),
        (0, 0),
        (1, 1),
        (-1, -1),
        (0.0, 0),
        (1.0, 1),
        (-1.0, -1),
        (0.0e0, 0),
        (+1.0e+0, 1),
        (-1.0e-0, -1),
        ("0", 0),
        ("1", 1),
        ("-1", -1),
        ("0xFF", 0xFF),
        ("0xF0", 0xF0),
        ("0o77", 0o77),
        ("0o70", 0o70),
        ("0b11", 0b11),
        ("0b10", 0b10),
    )
    @ddt.unpack
    def test_parse_int_or(self, data, expect):
        self.assertEqual(expect, parse_int_or(data))

    @ddt.data(
        (False, 0.0),
        (True, 1.0),
        (0, 0.0),
        (1, 1.0),
        (-1, -1.0),
        (0.0, 0.0),
        (1.0, 1.0),
        (-1.0, -1.0),
        (0.0e0, 0.0),
        (+1.0e+0, 1.0),
        (-1.0e-0, -1.0),
        ("0", 0.0),
        ("1", 1.0),
        ("-1", -1.0),
        ("0.0", 0.0),
        ("1.0", 1.0),
        ("-1.0", -1.0),
        ("0.0e0", 0.0),
        ("+1.0e+0", 1.0),
        ("-1.0e-0", -1.0),
    )
    @ddt.unpack
    def test_parse_float_or(self, data, expect):
        self.assertEqual(expect, parse_float_or(data))

    @ddt.data(
        (1, 1),
        (0, 0),
        (-1, -1),
        (1.0, 1.0),
        (1.0e10, 1.0e10),
        (0.0, 0.0),
        (-1.0e-10, -1.0e-10),
        (True, True),
        (False, False),
        (dt_utc(1970, 1, 1, 0, 0, 0), dt_utc(1970, 1, 1, 0, 0, 0)),
        (dt_utc(2020, 12, 31, 23, 59, 59), dt_utc(2020, 12, 31, 23, 59, 59)),
        ("1", 1),
        ("0", 0),
        ("-1", -1),
        ("1.0", 1.0),
        ("1.0e10", 1.0e10),
        ("0.0", 0.0),
        ("-1.0", -1.0),
        ("-1.0e-10", -1.0e-10),
        ("True", True),
        ("False", False),
        ("1970-01-01T00:00:00", dt_utc(1970, 1, 1, 0, 0, 0)),
        ("2020-12-31T23:59:59", dt_utc(2020, 12, 31, 23, 59, 59)),
        ("dummy", "dummy"),
    )
    @ddt.unpack
    def test_str_conv(self, data, expect):
        self.assertEqual(expect, str_conv(data))

    @ddt.data(
        ("", {}),
        (" \t", {}),
        ("foo=bar", {"foo": "bar"}),
        (
            "dummy_key_1=dummy_value_1,dummy_key_2=dummy_value_2",
            {"dummy_key_1": "dummy_value_1", "dummy_key_2": "dummy_value_2"},
        ),
        (
            "dummy_key_1=dummy_value_1,dummy_key_2=dummy_value_2,dummy_key_3",
            {"dummy_key_1": "dummy_value_1", "dummy_key_2": "dummy_value_2", "dummy_key_3": "True"},
        ),
        (
            "dummy_key_1=dummy_value_1,dummy_key_2=dummy_value_2,dummy_key_3=do not use spaces in strings CLI",
            {
                "dummy_key_1": "dummy_value_1",
                "dummy_key_2": "dummy_value_2",
                "dummy_key_3": "do not use spaces in strings CLI",
            },
        ),
        (
            "dummy_key_1=dummy_value_1_key=dummy_value_1_value,dummy_key_2=dummy_value_2_key=dummy_value_2_value",
            {
                "dummy_key_1": "dummy_value_1_key=dummy_value_1_value",
                "dummy_key_2": "dummy_value_2_key=dummy_value_2_value",
            },
        ),
    )
    @ddt.unpack
    def test_parse_params_string(self, s, params_dict):
        self.assertDictEqual(params_dict, parse_params_string(s))

    @ddt.data(
        (
            """""",
            [
                "",
            ]
        ),
        (
            """|""",
            [
                "",
            ]
        ),
        (
            """||""",
            [
                "|",
            ]
        ),
        (
            """| |""",
            [
                " |",
            ]
        ),
        (
            """Lorem ipsum dolor sit amet, consectetur adipiscing elit.""",
            [
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            ]
        ),
        (
            """   Lorem ipsum dolor sit amet, consectetur adipiscing elit.   """,
            [
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit.   ",
            ]
        ),
        (
            """|   Lorem ipsum dolor sit amet, consectetur adipiscing elit.""",
            [
                "   Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            ]
        ),
        (
            """   |   Lorem ipsum dolor sit amet, consectetur adipiscing elit.""",
            [
                "   Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            ]
        ),
        (
            """
            """,
            [
                "",
                "",
            ]
        ),
        (
            """
            |""",
            [
                "",
                "",
            ]
        ),
        (
            """
            |
            """,
            [
                "",
                "",
                "",
            ]
        ),
        (
            """
            |
            ||
            |||
            ||||
            |||||
            """,
            [
                "",
                "| || ||| ||||",
                "",
            ]
        ),
        (
            """
                |
               ||
              |||
             ||||
            |||||
            """,
            [
                "",
                "| || ||| ||||",
                "",
            ]
        ),
        (
            """
            |Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam consectetur cursus purus sed dictum. Mauris
            |dui nibh, ullamcorper ac consequat nec, venenatis a tortor. Sed est arcu, aliquam at vestibulum quis,
            |tincidunt ac urna. Nullam lectus ipsum, tincidunt sodales porttitor vitae, feugiat sed risus. Vivamus
            |sollicitudin suscipit condimentum. Vestibulum odio tellus, suscipit at ipsum quis, molestie placerat quam.
            |Etiam accumsan, purus eu tristique hendrerit, magna urna lobortis neque, sed imperdiet mi sapien id diam.
            |Donec suscipit pretium finibus. Maecenas vel placerat sem.
            |
            |
            |Etiam a dapibus velit. Fusce porttitor vestibulum ultricies. Donec gravida ipsum ac dictum pretium. Mauris
            |vitae sem a diam condimentum hendrerit. Donec ut tristique neque, id pretium leo. Nulla lobortis tortor ut
            |convallis consequat. Maecenas ut ligula laoreet, feugiat arcu at, interdum ipsum. Pellentesque ornare leo
            |augue. Phasellus scelerisque ex ac pellentesque interdum.
            |
            |
            |Donec et erat vel mi dapibus lobortis. Suspendisse in fringilla nunc. Fusce venenatis, ex nec aliquam
            |faucibus, dolor mi dignissim nulla, vel dictum massa dolor vitae purus. Ut ullamcorper arcu non nulla
            |eleifend malesuada. Curabitur massa est, volutpat ornare pulvinar ut, elementum in felis. Interdum et
            |malesuada fames ac ante ipsum primis in faucibus. Integer magna erat, ullamcorper eget tristique eu,
            |interdum vitae nulla. Nulla facilisi.""",
            [
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam consectetur cursus purus sed dictum. Mauris dui nibh, ullamcorper ac consequat nec, venenatis a tortor. Sed est arcu, aliquam at vestibulum quis, tincidunt ac urna. Nullam lectus ipsum, tincidunt sodales porttitor vitae, feugiat sed risus. Vivamus sollicitudin suscipit condimentum. Vestibulum odio tellus, suscipit at ipsum quis, molestie placerat quam. Etiam accumsan, purus eu tristique hendrerit, magna urna lobortis neque, sed imperdiet mi sapien id diam. Donec suscipit pretium finibus. Maecenas vel placerat sem.",
                "",
                "Etiam a dapibus velit. Fusce porttitor vestibulum ultricies. Donec gravida ipsum ac dictum pretium. Mauris vitae sem a diam condimentum hendrerit. Donec ut tristique neque, id pretium leo. Nulla lobortis tortor ut convallis consequat. Maecenas ut ligula laoreet, feugiat arcu at, interdum ipsum. Pellentesque ornare leo augue. Phasellus scelerisque ex ac pellentesque interdum.",
                "",
                "Donec et erat vel mi dapibus lobortis. Suspendisse in fringilla nunc. Fusce venenatis, ex nec aliquam faucibus, dolor mi dignissim nulla, vel dictum massa dolor vitae purus. Ut ullamcorper arcu non nulla eleifend malesuada. Curabitur massa est, volutpat ornare pulvinar ut, elementum in felis. Interdum et malesuada fames ac ante ipsum primis in faucibus. Integer magna erat, ullamcorper eget tristique eu, interdum vitae nulla. Nulla facilisi.",
            ]
        ),
        (
            """
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam consectetur cursus purus sed dictum. Mauris
            dui nibh, ullamcorper ac consequat nec, venenatis a tortor. Sed est arcu, aliquam at vestibulum quis,
            tincidunt ac urna. Nullam lectus ipsum, tincidunt sodales porttitor vitae, feugiat sed risus. Vivamus
            sollicitudin suscipit condimentum. Vestibulum odio tellus, suscipit at ipsum quis, molestie placerat quam.
            Etiam accumsan, purus eu tristique hendrerit, magna urna lobortis neque, sed imperdiet mi sapien id diam.
            Donec suscipit pretium finibus. Maecenas vel placerat sem.


            Etiam a dapibus velit. Fusce porttitor vestibulum ultricies. Donec gravida ipsum ac dictum pretium. Mauris
            vitae sem a diam condimentum hendrerit. Donec ut tristique neque, id pretium leo. Nulla lobortis tortor ut
            convallis consequat. Maecenas ut ligula laoreet, feugiat arcu at, interdum ipsum. Pellentesque ornare leo
            augue. Phasellus scelerisque ex ac pellentesque interdum.


            Donec et erat vel mi dapibus lobortis. Suspendisse in fringilla nunc. Fusce venenatis, ex nec aliquam
            faucibus, dolor mi dignissim nulla, vel dictum massa dolor vitae purus. Ut ullamcorper arcu non nulla
            eleifend malesuada. Curabitur massa est, volutpat ornare pulvinar ut, elementum in felis. Interdum et
            malesuada fames ac ante ipsum primis in faucibus. Integer magna erat, ullamcorper eget tristique eu,
            interdum vitae nulla. Nulla facilisi.""",
            [
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam consectetur cursus purus sed dictum. Mauris dui nibh, ullamcorper ac consequat nec, venenatis a tortor. Sed est arcu, aliquam at vestibulum quis, tincidunt ac urna. Nullam lectus ipsum, tincidunt sodales porttitor vitae, feugiat sed risus. Vivamus sollicitudin suscipit condimentum. Vestibulum odio tellus, suscipit at ipsum quis, molestie placerat quam. Etiam accumsan, purus eu tristique hendrerit, magna urna lobortis neque, sed imperdiet mi sapien id diam. Donec suscipit pretium finibus. Maecenas vel placerat sem.",
                "",
                "Etiam a dapibus velit. Fusce porttitor vestibulum ultricies. Donec gravida ipsum ac dictum pretium. Mauris vitae sem a diam condimentum hendrerit. Donec ut tristique neque, id pretium leo. Nulla lobortis tortor ut convallis consequat. Maecenas ut ligula laoreet, feugiat arcu at, interdum ipsum. Pellentesque ornare leo augue. Phasellus scelerisque ex ac pellentesque interdum.",
                "",
                "Donec et erat vel mi dapibus lobortis. Suspendisse in fringilla nunc. Fusce venenatis, ex nec aliquam faucibus, dolor mi dignissim nulla, vel dictum massa dolor vitae purus. Ut ullamcorper arcu non nulla eleifend malesuada. Curabitur massa est, volutpat ornare pulvinar ut, elementum in felis. Interdum et malesuada fames ac ante ipsum primis in faucibus. Integer magna erat, ullamcorper eget tristique eu, interdum vitae nulla. Nulla facilisi.",
            ]
        ),
    )
    @ddt.unpack
    def test_strip_margin(self, data, expect):
        self.assertEqual(strip_margin(data), "\n".join(expect))
