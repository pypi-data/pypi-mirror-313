import re
from collections import OrderedDict
from typing import Any


def parse_did_filter_from_string_fe(
        input_string: str,
        name: str = '*',
        type: str = 'collection',
        omit_name: bool = False
) -> tuple[list[dict[str, Any]], str]:
    """
    Parse DID filter string for the filter engine (fe).

    Should adhere to the following conventions:
    - ';' represents the logical OR operator
    - ',' represents the logical AND operator
    - all operators belong to set of (<=, >=, ==, !=, >, <, =)
    - there should be no duplicate key+operator criteria.

    One sided and compound inequalities are supported.

    Sanity checking of input is left to the filter engine.

    :param input_string: String containing the filter options.
    :param name: DID name.
    :param type: The type of the did: all(container, dataset, file), collection(dataset or container), dataset, container.
    :param omit_name: omit addition of name to filters.
    :return: list of dictionaries with each dictionary as a separate OR expression.
    """
    # lookup table unifying all comprehended operators to a nominal suffix.
    # note that the order matters as the regex engine is eager, e.g. don't want to evaluate '<=' as '<' and '='.
    operators_suffix_LUT = OrderedDict({
        '<=': 'lte',
        '>=': 'gte',
        '==': '',
        '!=': 'ne',
        '>': 'gt',
        '<': 'lt',
        '=': ''
    })

    # lookup table mapping operator opposites, used to reverse compound inequalities.
    operator_opposites_LUT = {
        'lt': 'gt',
        'lte': 'gte'
    }
    operator_opposites_LUT.update({op2: op1 for op1, op2 in operator_opposites_LUT.items()})

    filters = []
    if input_string:
        or_groups = list(filter(None, input_string.split(';')))     # split <input_string> into OR clauses
        for or_group in or_groups:
            or_group = or_group.strip()
            and_groups = list(filter(None, or_group.split(',')))    # split <or_group> into AND clauses
            and_group_filters = {}
            for and_group in and_groups:
                and_group = and_group.strip()
                # tokenise this AND clause using operators as delimiters.
                tokenisation_regex = "({})".format('|'.join(operators_suffix_LUT.keys()))
                and_group_split_by_operator = list(filter(None, re.split(tokenisation_regex, and_group)))
                if len(and_group_split_by_operator) == 3:       # this is a one-sided inequality or expression
                    key, operator, value = [token.strip() for token in and_group_split_by_operator]

                    # substitute input operator with the nominal operator defined by the LUT, <operators_suffix_LUT>.
                    operator_mapped = operators_suffix_LUT.get(operator)

                    filter_key_full = key
                    if operator_mapped is not None:
                        if operator_mapped:
                            filter_key_full = "{}.{}".format(key, operator_mapped)
                    else:
                        raise SyntaxError("{} operator not understood.".format(operator_mapped))

                    if filter_key_full in and_group_filters:
                        raise DuplicateCriteriaInDIDFilter(filter_key_full)
                    else:
                        and_group_filters[filter_key_full] = value
                elif len(and_group_split_by_operator) == 5:     # this is a compound inequality
                    value1, operator1, key, operator2, value2 = [token.strip() for token in and_group_split_by_operator]

                    # substitute input operator with the nominal operator defined by the LUT, <operators_suffix_LUT>.
                    operator1_mapped = operator_opposites_LUT.get(operators_suffix_LUT.get(operator1))
                    operator2_mapped = operators_suffix_LUT.get(operator2)

                    filter_key1_full = filter_key2_full = key
                    if operator1_mapped is not None and operator2_mapped is not None:
                        if operator1_mapped:    # ignore '' operator (maps from equals)
                            filter_key1_full = "{}.{}".format(key, operator1_mapped)
                        if operator2_mapped:    # ignore '' operator (maps from equals)
                            filter_key2_full = "{}.{}".format(key, operator2_mapped)
                    else:
                        raise SyntaxError("{} operator not understood.".format(operator_mapped))

                    if filter_key1_full in and_group_filters:
                        raise DuplicateCriteriaInDIDFilter(filter_key1_full)
                    else:
                        and_group_filters[filter_key1_full] = value1
                    if filter_key2_full in and_group_filters:
                        raise DuplicateCriteriaInDIDFilter(filter_key2_full)
                    else:
                        and_group_filters[filter_key2_full] = value2
                else:
                    raise SyntaxError(and_group)

            # add name key to each AND clause if it hasn't already been populated from the filter and <omit_name> not set.
            if not omit_name and 'name' not in and_group_filters:
                and_group_filters['name'] = name

            filters.append(and_group_filters)
    else:
        if not omit_name:
            filters.append({
                'name': name
            })
    return filters, type
