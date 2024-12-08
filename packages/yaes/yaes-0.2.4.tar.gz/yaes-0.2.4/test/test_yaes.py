import unittest
import sphinxter.unittest

import yaes


class TestEngine(sphinxter.unittest.TestCase):

    maxDiff = None

    def setUp(self):

        self.engine = yaes.Engine()

    def test___init__(self):

        init = yaes.Engine("yep")

        self.assertEqual(init.env, "yep")

    def test_transform(self):

        self.assertEqual('1', self.engine.transform("{{ a }}", {"a": 1}))
        self.assertEqual(['1'], self.engine.transform(["{{ a }}"], {"a": 1}))
        self.assertEqual({"b": '1'}, self.engine.transform({"b": "{{ a }}"}, {"a": 1}))
        self.assertEqual('True', self.engine.transform("{{ a == 1 }}", {"a": 1}))
        self.assertEqual('False', self.engine.transform("{{ a != 1 }}", {"a": 1}))
        self.assertEqual(True, self.engine.transform(True, {}))
        self.assertEqual(False, self.engine.transform(False, {}))
        self.assertEqual(True, self.engine.transform("{? 1 == 1 ?}", {}))
        self.assertEqual(False, self.engine.transform("{? 1 == 0 ?}", {}))
        self.assertEqual(None, self.engine.transform("{[ a__b ]}", {}))
        self.assertEqual(3, self.engine.transform("{[ a__b-c ]}", {"a": {"b-c": 3}}))
        self.assertEqual(3, self.engine.transform("{[ {{ first }}__{{ second }} ]}", {"first": "a", "second": "b-c", "a": {"b-c": 3}}))

        self.assertSphinxter(yaes.Engine.transform)

    def test_require(self):

        self.assertTrue(self.engine.requires({}, {}))

        block = {
            "requires": "a"
        }

        self.assertTrue(self.engine.requires(block, {"a": 1}))
        self.assertFalse(self.engine.requires(block, {}))

        block = {
            "requires": ["a__b", "{[ a__b ]}"]
        }

        self.assertFalse(self.engine.requires(block, {}))
        self.assertFalse(self.engine.requires(block, {"a": {"b": "c"}}))
        self.assertTrue(self.engine.requires(block, {"a": {"b": "c"}, "c": "yep"}))

        self.assertSphinxter(yaes.Engine.requires)

    def test_transpose(self):

        self.assertEqual({"b": 1}, self.engine.transpose({"transpose": {"b": "a"}}, {"a": 1}))

        self.assertSphinxter(yaes.Engine.transpose)

    def test_iterate(self):

        values = {
            "a": 1,
            "cs": [2, 3],
            "ds": "nuts"
        }

        self.assertEqual(self.engine.iterate({}, values), [{}])

        block = {
            "transpose": {
                "b": "a"
            },
            "iterate": {
                "c": "cs",
                "d": "ds"
            }
        }

        self.assertEqual(self.engine.iterate(block, values), [
            {"b": 1, "c": 2, "d": "n"},
            {"b": 1, "c": 2, "d": "u"},
            {"b": 1, "c": 2, "d": "t"},
            {"b": 1, "c": 2, "d": "s"},
            {"b": 1, "c": 3, "d": "n"},
            {"b": 1, "c": 3, "d": "u"},
            {"b": 1, "c": 3, "d": "t"},
            {"b": 1, "c": 3, "d": "s"}
        ])

        self.assertSphinxter(yaes.Engine.iterate)

    def test_condition(self):

        self.assertTrue(self.engine.condition({}, {}))

        block = {
            "condition": "{{ a == 1 }}"
        }

        self.assertTrue(self.engine.condition(block, {"a": 1}))
        self.assertFalse(self.engine.condition(block, {"a": 2}))

        block = {
            "condition": "{? a == 1 ?}"
        }

        self.assertTrue(self.engine.condition(block, {"a": 1}))
        self.assertFalse(self.engine.condition(block, {"a": 2}))

        self.assertSphinxter(yaes.Engine.condition)

    def test_clean(self):

        block = {
            "ya": "sure",
            "requires": "a",
            "transpose": {
                "b": "a"
            },
            "iterate": {
                "c": "cs",
                "d": "ds"
            },
            "condition": "{{ c != 3 and d != 't' }}",
            "blocks": [1,2, 3],
            "values": {"L": "{{ c + 5 }}"}
        }

        self.assertEqual(self.engine.clean(block), {"ya": "sure"})

        self.assertSphinxter(yaes.Engine.clean)

    def test_blocks(self):

        block = {
            "ya": "sure",
            "requires": "a",
            "transpose": {
                "b": "a"
            },
            "iterate": {
                "c": "cs",
                "d": "ds"
            },
            "condition": "{{ c != 3 and d != 't' }}",
            "values": {"L": "{{ c + 5 }}"}
        }

        self.assertEqual(list(self.engine.blocks(block, {})), [({"ya": "sure"}, {})])

        values = {
            "a": 1,
            "cs": [2, 3],
            "ds": "nuts"
        }

        block = {
            "ya": "sure",
            "blocks": [
                {
                    "ya": "whatever"
                },
                {
                    "ya": "ofcourse",
                    "requires": "a",
                    "transpose": {
                        "b": "a"
                    },
                    "iterate": {
                        "c": "cs",
                        "d": "ds"
                    },
                    "condition": "{{ c != 3 and d != 't' }}",
                    "values": {"L": "{{ c + 5 }}"},
                }
            ]
        }

        self.assertEqual(list(self.engine.blocks(block, values)), [
            ({"ya": "whatever"}, {"a": 1, "cs": [2, 3], "ds": "nuts"}),
            ({"ya": "ofcourse"}, {"a": 1, "cs": [2, 3], "ds": "nuts", "b": 1, "c": 2, "d": "n", "L": "7"}),
            ({"ya": "ofcourse"}, {"a": 1, "cs": [2, 3], "ds": "nuts", "b": 1, "c": 2, "d": "u", "L": "7"}),
            ({"ya": "ofcourse"}, {"a": 1, "cs": [2, 3], "ds": "nuts", "b": 1, "c": 2, "d": "s", "L": "7"})
        ])

        self.assertSphinxter(yaes.Engine.blocks)

    def test_each(self):

        values = {
            "a": 1,
            "cs": [2, 3],
            "ds": "nuts"
        }

        block = {
            "ya": "sure",
            "transpose": {
                "b": "a"
            },
            "iterate": {
                "c": "cs",
                "d": "ds"
            },
            "condition": "{{ c != 3 and d != 't' }}",
            "values": {"L": "{{ c + 5 }}"},
            "blocks": [
                {},
                {
                    "ya": "ofcourse",
                    "condition": "{{ d == 'u' }}",
                }
            ]
        }

        self.assertEqual(list(self.engine.each(block, values)), [
            ({"ya": "sure"}, {"a": 1, "cs": [2, 3], "ds": "nuts", "b": 1, "c": 2, "d": "n", "L": "7"}),
            ({"ya": "sure"}, {"a": 1, "cs": [2, 3], "ds": "nuts", "b": 1, "c": 2, "d": "u", "L": "7"}),
            ({"ya": "ofcourse"}, {"a": 1, "cs": [2, 3], "ds": "nuts", "b": 1, "c": 2, "d": "u", "L": "7"}),
            ({"ya": "sure"}, {"a": 1, "cs": [2, 3], "ds": "nuts", "b": 1, "c": 2, "d": "s", "L": "7"})
        ])

        block = {
            "requires": "a",
        }

        self.assertEqual(list(self.engine.each(block, {})), [])

        self.assertSphinxter(yaes.Engine.each)

class TestYeas(sphinxter.unittest.TestCase):

    def test_module(self):

        self.assertSphinxter(yaes)

    def test_each(self):

        values = {
            "a": 1,
            "cs": [2, 3],
            "ds": "nuts"
        }

        block = {
            "ya": "sure",
            "transpose": {
                "b": "a"
            },
            "iterate": {
                "c": "cs",
                "d": "ds"
            },
            "condition": "{{ c != 3 and d != 't' }}",
            "values": {"L": "{{ c + 5 }}"},
            "blocks": [
                {},
                {
                    "ya": "ofcourse",
                    "condition": "{{ d == 'u' }}",
                }
            ]
        }

        self.assertEqual(list(yaes.each(block, values)), [
            ({"ya": "sure"}, {"a": 1, "cs": [2, 3], "ds": "nuts", "b": 1, "c": 2, "d": "n", "L": "7"}),
            ({"ya": "sure"}, {"a": 1, "cs": [2, 3], "ds": "nuts", "b": 1, "c": 2, "d": "u", "L": "7"}),
            ({"ya": "ofcourse"}, {"a": 1, "cs": [2, 3], "ds": "nuts", "b": 1, "c": 2, "d": "u", "L": "7"}),
            ({"ya": "sure"}, {"a": 1, "cs": [2, 3], "ds": "nuts", "b": 1, "c": 2, "d": "s", "L": "7"})
        ])

        self.assertSphinxter(yaes.each)
