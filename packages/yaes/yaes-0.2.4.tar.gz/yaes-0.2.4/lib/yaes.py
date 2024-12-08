"""
description: |
    Yet Another Expansion Syntax (pronounced 'Yasssss Kweeeeen') for expanding complex data (YAML / JSON) with Jinja2 templating

    If a block has no control keywords, everything is emitted as is::

        import yaes

        block = {
            "ya": "{{ a }}"
        }

        values = {
            "a": "sure"
        }

        list(yaes.each(block, values))
        # [
        #     ({"ya": "{{ a }}"}, {"a": "sure"})
        # ]

    The behavior is the same if you send a list of blocks::

        list(yaes.each([block], values))
        # [
        #     ({"ya": "{{ a }}"}, {"a": "sure"})
        # ]

    requires
    --------

    If a requires keyword is present, all the keys listed must be in values for the block to emitted::

        blocks = [
            {
                "name": "one",
                "requires": "a"
            },
            {
                "name": "twp",
                "requires": ["a", "b"]
            }
        ]

        values = {
            "a": "sure"
        }

        list(yaes.each(blocks, values))
        # [
        #     ({"name": "one"}, {"a": "sure"})
        # ]

    .. note::

        requires can be a str or list of str.

    This is useful for modules like opengui, where we don't want to evaluate the conditions on some fields
    unless other fields in those conditions actually have values.

    transpose
    ---------

    If a transpose keyword is present, it'll use the key pairs to transpose the values::

        blocks = [
            {
                "name": "one",
                "transpose": {
                    "b": "a"
                }
            }
        ]

        values = {
            "a": "sure"
        }

        list(yaes.each(blocks, values))
        # [
        #     ({"name": "one"}, {"a": "sure", "b": "sure"})
        # ]

    .. note::

        you can have multiple values to transpose

    This is useful if you're re-using a template that uses veriables and you want to replace
    them with your usage's specific variables.

    iterate
    -------

    If a iterate keyword is present, it'll use the key pairs to iterate new values::

        blocks = [
            {
                "name": "{{ fruit }}",
                "iterate": {
                    "fruit": "fruits"
                }
            }
        ]

        values = {
            "fruits": [
                "apple",
                "pear",
                "orange"
            ]
        }

        list(yaes.each(blocks, values))
        # [
        #     (
        #         {
        #             "name": "{{ fruit }}"
        #         },
        #         {
        #             "fruit": "apple",
        #             "fruits": [
        #                 "apple",
        #                 "pear",
        #                 "orange"
        #             ]
        #         }
        #     ),
        #     (
        #         {
        #             "name": "{{ fruit }}"
        #         },
        #         {
        #             "fruit": "pear",
        #             "fruits": [
        #                 "apple",
        #                 "pear",
        #                 "orange"
        #             ]
        #         }
        #     ),
        #     (
        #         {
        #             "name": "{{ fruit }}"
        #         },
        #         {
        #             "fruit": "orange",
        #             "fruits": [
        #                 "apple",
        #                 "pear",
        #                 "orange"
        #             ]
        #         }
        #     )
        # ]

    .. note::

        you can have multiple values to iterate, and it'll iterate over the different
        pairs alphabetically by key

    This is useful with opengui as you can take the values of a multi option field and
    use those values to create a new field for each option selected.

    condition
    ---------

    If a condition keyword is present, it'll only emit the block if the condition evaluates True::

        blocks = [
            {
                "name": "one",
                "condition": "{? a == 1 ?}"
            },
            {
                "name": "two",
                "condition": "{? a == 2 ?}"
            }
        ]

        values = {
            "a": 1
        }

        list(yaes.each(blocks, values))
        # [
        #     ({"name": "one"}, {"a": 1})
        # ]

    .. note::

        make sure you use '{?' and '?}' in the condition so it renders as a boolean.

    This is useful if you only want to use a block under certain conditions.

    blocks
    ------

    If a blocks keyword is present, it'll expand those blocks, using the parent block as a base::

        blocks = [
            {
                "base": "value",
                "blocks": [
                    {
                        "name": "one"
                    },
                    {
                        "name": "two",
                        "base": "override"
                    }
                ]
            }
        ]

        values = {
            "a": 1
        }

        list(yaes.each(blocks, values))
        # [
        #     (
        #         {
        #             "base": "value",
        #             "name": "one"
        #         },
        #         {
        #             "a": 1
        #         }
        #     ),
        #     (
        #         {
        #             "base": "override",
        #             "name": "two"
        #         },
        #         {
        #             "a": 1
        #         }
        #     )
        # ]

    .. note::

        blocks within blocks with control keywords will have those keywords evaluated

    This is useful if you have a condition or iterate that you want to apply to multiple
    block without having to use those keywords on each block.

    values
    ------

    If a values keyword is present, it'll merge those values into the values emitted::

        blocks = [
            {
                "name": "one"
            },
            {
                "name": "two",
                "values": {
                    "a": 2,
                    "c": "{{ b }}sah"
                }
            }
        ]

        values = {
            "a": 1,
            "b": "yes"
        }

        list(yaes.each(blocks, values))
        # [
        #     (
        #         {
        #             "name": "one"
        #         },
        #         {
        #             "a": 1,
        #             "b": "yes"
        #         }
        #     ),
        #     (
        #         {
        #             "name": "two"
        #         },
        #         {
        #             "a": 2,
        #             "b": "yes",
        #             "c": "yessah"
        #         }
        #     )
        # ]

    .. note::

        you can have multiple pairs in values

    This is useful if you want to override the existing values but at this point I don't
    think even I've ever used it.
"""

# pylint: disable=consider-using-f-string

import copy
import jinja2
import overscore


class Engine:
    """
    Class for expanding complex data (YAML / JSON) with Jinja2 templating
    """

    CONTROLS = [
        "requires",
        "transpose",
        "iterate",
        "condition",
        "blocks",
        "values"
    ] # list of control keywords

    env = None  # Jinja2 environment
    "type: jinja2.Environment"

    def __init__(self,
        env=None    # optional jinja2 Environment to use with transform
    ):
        """
        parameters:
            env:
                type: jinja2.Environment
        """

        self.env = env if env else jinja2.Environment()

    def transform(self,
        template,   # template to use
        values:dict # values to use with the template
    ):
        """
        description: |
            Renders a Jinja2 template using values sent

            If the template is a str and is enclosed by '{?' and '?}', it will render the template but evaluate as a bool.

            If the template is a str and is enclosed by '{[' and ']}', it will lookup the value in valuue using overscore notation.

            Else if the tempalte is a str, it will render the template in the standard Jinja2 way.

            If the template is a list, it will recurse and render each item.

            If the template is a dict, it will recurse each key and render each item.

            Else return the template as is.
        parameters:
            template:
                type:
                - bool
                - str
                - list
                - dict
        return: The rendered value
        usage: |
            ::

                import yaes

                engine = yaes.Engine()

                engine.transform("{{ a }}", {"a": 1})
                # '1'

                engine.transform(["{{ a }}"], {"a": 1})
                # ['1']

                engine.transform({"b": "{{ a }}"}, {"a": 1})
                # {"b": '1'}

                engine.transform("{{ a == 1 }}", {"a": 1})
                # 'True'

                engine.transform("{{ a != 1 }}", {"a": 1})
                # 'False'

                engine.transform(True, {})
                # True

                engine.transform(False, {})
                # False

                engine.transform("{? 1 == 1 ?}", {})
                # True

                engine.transform("{? 1 == 0 ?}", {})
                # False

                engine.transform("{[ a__b ]}", {})
                # None

                engine.transform("{[ a__b-c ]}", {"a": {"b-c": 3}})
                # 3

                engine.transform("{[ {{ first }}__{{ second }} ]}", {"first": "a", "second": "b-c", "a": {"b-c": 3}})
                # 3

        """

        if isinstance(template, str):
            if len(template) > 4 and template[:2] == "{?" and template[-2:] == "?}":
                return self.env.from_string("{{%s}}" % template[2:-3]).render(**values) == "True"
            if len(template) > 4 and template[:2] == "{[" and template[-2:] == "]}":
                return overscore.get(values, self.transform(template[2:-3].strip(), values))
            return self.env.from_string(template).render(**values)
        if isinstance(template, list):
            return [self.transform(item, values) for item in template]
        if isinstance(template, dict):
            return {key: self.transform(item, values) for key, item in template.items()}

        return template

    def requires(self,
        block:dict, # block to evaulate
        values:dict # values to evaluate with
    )->bool:
        """
        description: |
            Determines whether values are set to process a block
        usage: |
            ::

                import yaes

                engine = yaes.Engine()

                engine.requires({}, {})
                # True

                block = {
                    "requires": "a"
                }

                engine.requires(block, {"a": 1})
                # True

                engine.requires(block, {})
                # False

                block = {
                    "requires": ["a__b", "{[ a__b ]}"]
                }

                engine.requires(block, {})
                # False

                engine.requires(block, {"a": {"b": "c"}})
                # False

                engine.requires(block, {"a": {"b": "c"}, "c": "yep"})
                # True
        """

        if "requires" not in block:
            return True

        requires = block["requires"]

        if not isinstance(requires, list):
            requires = [requires]

        for path in requires:
            if not overscore.has(values, self.transform(path, values)):
                return False

        return True

    @staticmethod
    def transpose(
        block:dict, # block to evaulate
        values:dict # values to evaluate with
    )->dict:
        """
        description: Transposes values, allows for the same value under a different name
        usage: |
            ::

                import yaes

                engine = yaes.Engine()

                engine.transpose({"transpose": {"b": "a"}}, {"a": 1})
                # {"b": 1}
        return: The new values block transposed
        """

        transpose = block.get("transpose", {})

        return {derivative: values[original] for derivative, original in transpose.items() if original in values}

    def iterate(self,
        block:dict, # block to evaulate
        values:dict # values to evaluate with
    )->list:
        """
        description: Iterates values with transposition
        return: The list of blocks iterated
        usage: |
            ::

                import yaes

                engine = yaes.Engine()

                values = {
                    "a": 1,
                    "cs": [2, 3],
                    "ds": "nuts"
                }

                engine.iterate({}, values)
                # [{}]

                block = {
                    "transpose": {
                        "b": "a"
                    },
                    "iterate": {
                        "c": "cs",
                        "d": "ds"
                    }
                }

                engine.iterate(block, values)
                # [
                #     {
                #         "b": 1,
                #         "c": 2,
                #         "d": "n"
                #     },
                #     {
                #         "b": 1,
                #         "c": 2,
                #         "d": "u"
                #     },
                #     {
                #         "b": 1,
                #         "c": 2,
                #         "d": "t"
                #     },
                #     {
                #         "b": 1,
                #         "c": 2,
                #         "d": "s"
                #     },
                #     {
                #         "b": 1,
                #         "c": 3,
                #         "d": "n"
                #     },
                #     {
                #         "b": 1,
                #         "c": 3,
                #         "d": "u"
                #     },
                #     {
                #         "b": 1,
                #         "c": 3,
                #         "d": "t"
                #     },
                #     {
                #         "b": 1,
                #         "c": 3,
                #         "d": "s"
                #     }
                # ]
        """

        iterate_values = [self.transpose(block, values)]

        iterate = block.get("iterate", {})

        for one in sorted(iterate.keys()):
            many_values = []
            for many_value in iterate_values:
                for value in values[iterate[one]]:
                    many_values.append({**many_value, one: value})
            iterate_values = many_values

        return iterate_values

    def condition(self,
        block:dict, # block to evaulate
        values:dict # values to evaluate with
    )->bool:
        """
        description: |
            Evaludates condition in values

            It's best to use '{?' and '?}' as conditions with straight Jinja2 with '{{' and '}}' will be deprecated.
        return: The evaluated condition
        usage: |
            ::

                import yaes

                engine = yaes.Engine()

                engine.condition({}, {})
                # True

                block = {
                    "condition": "{{ a == 1 }}"
                }

                engine.condition(block, {"a": 1})
                # True

                engine.condition(block, {"a": 2})
                # False

                block = {
                    "condition": "{? a == 1 ?}"
                }

                engine.condition(block, {"a": 1})
                # True

                engine.condition(block, {"a": 2})
                # False
        """

        if "condition" not in block:
            return True

        value = self.transform(block["condition"], values)

        if isinstance(value, bool):
            return value

        return value == "True"

    @classmethod
    def clean(cls,
        block:dict  # Block to clean
    )->dict:
        """
        desciption: Returns a deep copy of a block without control keys
        usage: |
            ::

                import yaes

                engine = yaes.Engine()

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
                    "values": {"L": 7}
                }

                engine.clean(block)
                # {"ya": "sure"}
        """

        return {key: copy.deepcopy(block[key]) for key in block.keys() if key not in cls.CONTROLS}

    def blocks(self,
        block:dict, # block to evaulate
        values:dict # values to evaluate with
    ):
        """
        desciption: Expands child blocks (if present) to override parent block
        return:
            description: Merged (child on top of parent) blocks
            type: Iterator
        usage: |
            If just a regular block, returns a cleaned copy::

                import yaes

                engine = yaes.Engine()

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

                list(engine.blocks(block, {}))
                # [({"ya": "sure"}, {})]

            If the block has blocks, it'll merge them onto top of the parent block after processing them::

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

                list(engine.blocks(block, values))
                # [
                #     ({"ya": "whatever"}, {"a": 1, "cs": [2, 3], "ds": "nuts"}),
                #     ({"ya": "ofcourse"}, {"a": 1, "cs": [2, 3], "ds": "nuts", "b": 1, "c": 2, "d": "n", "L": "7"}),
                #     ({"ya": "ofcourse"}, {"a": 1, "cs": [2, 3], "ds": "nuts", "b": 1, "c": 2, "d": "u", "L": "7"}),
                #     ({"ya": "ofcourse"}, {"a": 1, "cs": [2, 3], "ds": "nuts", "b": 1, "c": 2, "d": "s", "L": "7"})
                # ]
        """

        if "blocks" not in block:
            yield self.clean(block), values
        else:
            cleaned = self.clean(block)
            for (blocks_block, blocks_values) in self.each(block["blocks"], values):
                yield {**cleaned, **self.clean(blocks_block)}, blocks_values

    def each(self,
        blocks,     # blocks to evaulate
        values:dict # values to evaluate with
    ):
        """
        description: |
            Iterate over block(s), expanding using control key words

            This is used for hihgly dynamic configurmation. Blacks are assumed to have JKinja2 templating and
            controls for conditions, loops, even whether a block can be evaluated. This determines what's ready
            and will expand blocks based on the control keywords sent.
        parameters:
            blocks:
                type:
                - dict
                - list
        return:
            description: Passing blocks
            type: Iterator
        usage: |
            ::

                import yaes

                engine = yaes.Engine()

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

                list(engine.each(block, values))
                # [
                #     ({"ya": "sure"}, {"a": 1, "cs": [2, 3], "ds": "nuts", "b": 1, "c": 2, "d": "n", "L": "7"}),
                #     ({"ya": "sure"}, {"a": 1, "cs": [2, 3], "ds": "nuts", "b": 1, "c": 2, "d": "u", "L": "7"}),
                #     ({"ya": "ofcourse"}, {"a": 1, "cs": [2, 3], "ds": "nuts", "b": 1, "c": 2, "d": "u", "L": "7"}),
                #     ({"ya": "sure"}, {"a": 1, "cs": [2, 3], "ds": "nuts", "b": 1, "c": 2, "d": "s", "L": "7"})
                # ]

                block = {
                    "requires": "a",
                }

                list(engine.each(block, {}))
                # []
        """

        if isinstance(blocks, dict):
            blocks = [blocks]

        for block in blocks:

            if not self.requires(block, values):
                continue

            for iterate_values in self.iterate(block, values):

                extra_values = self.transform(block.get("values", {}), {**values, **iterate_values})
                block_values = {**values, **iterate_values, **extra_values}

                if not self.condition(block, block_values):
                    continue

                for blocks_block, blocks_values in self.blocks(block, block_values):
                    yield blocks_block, blocks_values

def each(
    blocks,         # blocks to evaulate
    values:dict,    # values to evaluate with
    env=None        # optional Jinja2.Environment to use for transformations
):
    """
    description: |
        Short hand each function for basic usage

        Go through blocks, iterating and checking conditions, yield blocks that pass
    parameters:
        blocks:
            type:
            - dict
            - list
        env:
            type: Jinja2.Environment
    return:
        description: Passing blocks
        type: Iterator
    usage: |
        ::

            import yaes

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

            list(yaes.each(block, values))
            # [
            #     ({"ya": "sure"}, {"a": 1, "cs": [2, 3], "ds": "nuts", "b": 1, "c": 2, "d": "n", "L": "7"}),
            #     ({"ya": "sure"}, {"a": 1, "cs": [2, 3], "ds": "nuts", "b": 1, "c": 2, "d": "u", "L": "7"}),
            #     ({"ya": "ofcourse"}, {"a": 1, "cs": [2, 3], "ds": "nuts", "b": 1, "c": 2, "d": "u", "L": "7"}),
            #     ({"ya": "sure"}, {"a": 1, "cs": [2, 3], "ds": "nuts", "b": 1, "c": 2, "d": "s", "L": "7"})
            # ]

            block = {
                "requires": "a",
            }

            list(yaes.each(block, {}))
            # []
    """

    for block in Engine(env).each(blocks, values):
        yield block
