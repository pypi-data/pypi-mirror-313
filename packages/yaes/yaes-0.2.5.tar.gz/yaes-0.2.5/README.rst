yaes
====

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

If a values keyword is present, it'll merge those values into teh values emitted::

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
