# Copyright (c) 2021, 2022 Henix, Henix.fr
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Expressions helpers"""

from typing import Any, Dict, List, NoReturn, Optional, Tuple, Union

import json
import re

from datetime import datetime

## Expressions

EXPRESSIONSYNTAX_MARK = re.compile(r'^\$\{\{.*\}\}$')

STRING = re.compile(r'(\'([^\']*)\')+')
IDENTIFIER = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_-]*')
NUMBER = re.compile(r'^((0x[0-9a-fA-F]+)|(-?\d+(\.\d+)?))')
OPERATOR = re.compile(r'^(==|!=|!|<=|<|>=|>|\[|\]|\(|\)|\.|&&|\|\||~=|,)')

INFIX_OPERATOR = ('==', '!=', '<=', '<', '>', '>=', '~=')

VALUE = 0
KIND = 1

STRING_KIND = 1
IDENTIFIER_KIND = 2
NUMBER_KIND = 3
OPERATOR_KIND = 4
END_KIND = 0

TOKEN_VALUE = Union[str, int, float]
TOKEN = Tuple[Optional[TOKEN_VALUE], int]

DEREFERENCE_TOKEN: TOKEN = ('.', OPERATOR_KIND)
INDEX_TOKEN: TOKEN = ('[', OPERATOR_KIND)
LPAREN_TOKEN: TOKEN = ('(', OPERATOR_KIND)
RPAREN_TOKEN: TOKEN = (')', OPERATOR_KIND)
COMMA_TOKEN: TOKEN = (',', OPERATOR_KIND)
NOT_TOKEN: TOKEN = ('!', OPERATOR_KIND)
AND_TOKEN: TOKEN = ('&&', OPERATOR_KIND)
OR_TOKEN: TOKEN = ('||', OPERATOR_KIND)
END_TOKEN: TOKEN = (None, END_KIND)

WEEKDAYS = (
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday',
)

DATETIME_FUNCTIONS = (
    'week',
    'day',
    'dayOfWeekISO',
    'dayOfWeek',
    'hour',
    'month',
    'year',
    'minute',
    'second',
)

SPECIAL_FUNCTIONS = '__special functions__'

########################################################################
## Tokenizer


def get_token(expr: str) -> Tuple[TOKEN_VALUE, int, str]:
    """Get first token in expr.

    # Required parameters

    - expr: a string

    # Returned value

    A tuple of three elements: `token`, `kind`, `expr`.

    # Raised exceptions

    A _ValueError_ exception is raised if the token is invalid.
    """
    if match := IDENTIFIER.match(expr):
        return match.group(0), IDENTIFIER_KIND, expr[match.end() :].strip()
    if match := STRING.match(expr):
        return (
            match.group(0)[1:-1].replace("''", "'"),
            STRING_KIND,
            expr[match.end() :].strip(),
        )
    if match := NUMBER.match(expr):
        num = match.group(0)
        if num.startswith('0x'):
            num = int(num, 16)
        else:
            num = float(num)
        return num, NUMBER_KIND, expr[match.end() :].strip()
    if match := OPERATOR.match(expr):
        return match.group(0), OPERATOR_KIND, expr[match.end() :].strip()
    raise ValueError(f'Invalid token {expr}')


def tokenize(expr: str) -> List[TOKEN]:
    """Return a list of tokens found in expr.

    # Required parameters

    - expr: a string

    # Returned value

    A list of _tokens_.  Each token is a (value, kind) pair.  The list
    ends with an `(None, END_TOKEN)` pair.

    # Raised exceptions

    A _ValueError_ is raised if `expr` contains an invalid token.
    """
    tokens: List[TOKEN] = []
    while expr:
        token, kind, expr = get_token(expr)
        tokens.append((token, kind))
    tokens.append(END_TOKEN)
    return tokens


########################################################################
## Operators helpers


def _is_infix_operator(token: TOKEN) -> bool:
    return token[KIND] == OPERATOR_KIND and token[VALUE] in INFIX_OPERATOR


def _is_segment_start(token: TOKEN) -> bool:
    return token in (DEREFERENCE_TOKEN, INDEX_TOKEN)


def _is_identifier(token: TOKEN) -> bool:
    return token[KIND] == IDENTIFIER_KIND


def _is_boolean(token: TOKEN) -> bool:
    return (
        _is_identifier(token)
        and isinstance(value := token[VALUE], str)
        and value.lower() in ('true', 'false')
    )


def _is_null(token: TOKEN) -> bool:
    return (
        _is_identifier(token)
        and isinstance(value := token[VALUE], str)
        and value.lower() == 'null'
    )


def _is_string(token: TOKEN) -> bool:
    return token[KIND] == STRING_KIND


def _to_number(val: Any) -> float:
    if val is None or val == '':
        return 0
    if isinstance(val, bool):
        return 1 if val else 0
    if isinstance(val, str):
        try:
            return float(val)
        except ValueError:
            return float('nan')
    if isinstance(val, (int, float)):
        return float(val)
    return float('nan')


def _to_string(val: Any) -> str:
    if val is None:
        return ''
    if isinstance(val, bool):
        return str(val).lower()
    if isinstance(val, float) and float(int(val)) == val:
        return str(int(val))
    return str(val)


########################################################################
## Path helpers


def find_path(tokens: List[TOKEN], start: int) -> int:
    """Find longest path in tokens starting at offset start.

    A _path_ is an identifier, possibly followed by segments.  Segments
    are of the form `.identifier` or `[term]`, where `term` is either a
    path or a string.
    """
    path_len = 1
    while _is_segment_start(tokens[start + path_len]):
        if tokens[start + path_len] == DEREFERENCE_TOKEN:
            if not _is_identifier(tokens[start + path_len + 1]):
                _fail_expecting('identifier', tokens[start + path_len + 1])
            path_len += 2
        else:
            if _is_string(tokens[start + path_len + 1]):
                path_len += 3
            elif _is_identifier(tokens[start + path_len + 1]):
                path_len += 2 + find_path(tokens, start + path_len + 1)
            else:
                _fail_expecting('identifier or string', tokens[start + path_len + 1])
    return path_len


def evaluate_path(
    path: List[TOKEN], contexts: Dict[str, Any]
) -> Union[str, Dict[str, Any]]:
    """Evaluate path using contexts.

    The path is syntactically valid.

    If the final part of `path` does not exist in `contexts`, returns
    an empty string.

    # Raised exceptions

    A _ValueError_ exception is raised if `path` does not start with
    a context available in `contexts`.
    """

    def _evaluate_segments(start: int, value):
        if not _is_segment_start(path[start]):
            return value
        if path[start] == DEREFERENCE_TOKEN:
            if _is_segment_start(path[start + 2]):
                try:
                    return _evaluate_segments(start + 2, value[path[start + 1][VALUE]])
                except AttributeError:
                    raise ValueError(
                        f'{path[start + 1][VALUE]} is not an object.  It does not have a {path[start + 3][VALUE]} entry'
                    )
            return value.get(path[start + 1][VALUE], '')

        if path[start + 1][KIND] == STRING_KIND:
            what = path[start + 1][VALUE]
            if _is_segment_start(path[start + 3]):
                return _evaluate_segments(start + 3, value[what])
        else:
            path_len = find_path(path, start + 1)
            what = evaluate_path(path[start + 1 : start + 1 + path_len + 1], contexts)
            if _is_segment_start(path[start + 1 + path_len + 1]):
                return _evaluate_segments(start + 1 + path_len + 1, value[what])
        return value.get(what, '')

    segment = path[0][VALUE]
    if segment not in contexts:
        raise ValueError(f'Invalid segment {segment} or incorrect function call')

    return _evaluate_segments(1, contexts[segment])


def evaluate_operation(lhs, operator: str, rhs) -> bool:
    """Perform binary operation evaluation.

    Type casting performed as per specification.

    # Required parameters

    - lhs: an object
    - operator: a string
    - rhs: an object

    # Returned value

    A boolean.
    """
    if isinstance(lhs, str) and isinstance(rhs, str):
        lhs = lhs.lower()
        rhs = rhs.lower()
    elif type(lhs) != type(rhs):
        lhs = _to_number(lhs)
        rhs = _to_number(rhs)
    if operator == '==':
        return lhs == rhs
    if operator == '!=':
        return lhs != rhs
    if operator == '~=':
        if isinstance(lhs, str) and isinstance(rhs, str):
            return re.search(rhs, lhs) is not None
        raise ValueError(
            f'Operator {operator} requires strings, got {lhs!r} and {rhs!r}.'
        )
    if operator == '<':
        return lhs < rhs  # type: ignore
    if operator == '<=':
        return lhs <= rhs  # type: ignore
    if operator == '>':
        return lhs > rhs  # type: ignore
    if operator == '>=':
        return lhs >= rhs  # type: ignore
    raise ValueError(f'Unknown operator {operator}')


def _fail_if_zero(len_: int, msg: str) -> None:
    if not len_:
        raise ValueError(f'Unexpected end of expression, was expecting {msg}')


def _fail_expecting(msg, what) -> NoReturn:
    raise ValueError(f'Invalid token, was expecting {msg}, got: {what}')


########################################################################
## Functions


def evaluate_function_arity_1(name: str, arg) -> Any:
    if name == 'fromJSON':
        return json.loads(arg)
    if name == 'toJSON':
        return json.dumps(arg)

    if name in DATETIME_FUNCTIONS:
        return evaluate_datetime_function(name, arg)
    raise ValueError(f'Unknown function {name}(arg)')


def evaluate_datetime_function(name: str, arg) -> Any:
    try:
        _dt = datetime.fromisoformat(arg)
    except ValueError:
        return ''

    if name == 'week':
        return _dt.isocalendar()[1]
    if name == 'day':
        return _dt.day
    if name == 'dayOfWeekISO':
        return _dt.isoweekday()
    if name == 'dayOfWeek':
        return WEEKDAYS[_dt.weekday()]
    if name == 'hour':
        return _dt.hour
    if name == 'month':
        return _dt.month
    if name == 'year':
        return _dt.year
    if name == 'minute':
        return _dt.minute
    if name == 'second':
        return _dt.second

    raise ValueError(f'Unknown function {name}(arg)')


def evaluate_function_arity_2(name: str, arg1, arg2) -> bool:
    if name == 'contains':
        needle = _to_string(arg2).lower()
        if isinstance(arg1, str):
            return needle in arg1.lower()
        return any(True for item in arg1 if _to_string(item).lower() == needle)
    if name == 'startsWith':
        return _to_string(arg1).lower().startswith(_to_string(arg2).lower())
    if name == 'endsWith':
        return _to_string(arg1).lower().endswith(_to_string(arg2).lower())
    raise ValueError(f'Unknown function {name}(arg1, arg2)')


def evaluate_status_function(name: str, contexts) -> bool:
    """Evaluate job status function.

    Annotates the contexts[SPECIAL_FUNCTIONS] entry with a `__called__`
    sub-entry, so that caller can detect status function usage.
    """
    funcs = contexts.get(SPECIAL_FUNCTIONS, {})
    if name not in funcs:
        raise ValueError(f'Unknown function {name}()')
    # a status function has been used
    funcs['__called__'] = True
    return funcs[name]


def _evaluate_identifier(
    tokens: List[TOKEN], contexts: Dict[str, Any], offset: int
) -> Tuple[int, Optional[Any]]:
    """Evaluate expressions starting with an identifier.

    true
    false
    null
    function()
    function(...)
    function(...,...)
    """
    if _is_boolean(tokens[offset]):
        return 1, tokens[offset][VALUE].lower() == 'true'  # type: ignore
    if _is_null(tokens[offset]):
        return 1, None

    if tokens[offset + 1] == LPAREN_TOKEN:
        function_name: str = tokens[offset][VALUE]  # type: ignore
        if tokens[offset + 2] == RPAREN_TOKEN:
            return 3, evaluate_status_function(function_name, contexts)  # type: ignore

        len_, what = _evaluate_expression(
            tokens, contexts, offset + 2, [COMMA_TOKEN, RPAREN_TOKEN]
        )
        _fail_if_zero(len_, 'expression or right parenthesis')
        if tokens[offset + 2 + len_] == RPAREN_TOKEN:
            return 2 + len_ + 1, evaluate_function_arity_1(function_name, what)
        else:
            len2, what2 = _evaluate_expression(
                tokens, contexts, offset + 2 + len_ + 1, RPAREN_TOKEN
            )
            return 2 + len_ + 1 + len2 + 1, evaluate_function_arity_2(
                function_name, what, what2
            )

    len_ = find_path(tokens, offset)
    what = evaluate_path(tokens[offset : offset + len_ + 1], contexts)
    return len_, what


def _evaluate_factor(
    tokens: List[TOKEN],
    contexts: Dict[str, Any],
    offset: int,
    end_token: Union[TOKEN, List[TOKEN]] = END_TOKEN,
) -> Tuple[int, Optional[Any]]:
    kind = tokens[offset][KIND]
    if kind == IDENTIFIER_KIND:
        len_, what = _evaluate_identifier(tokens, contexts, offset)
    elif kind in (STRING_KIND, NUMBER_KIND):
        len_, what = 1, tokens[offset][VALUE]
    elif tokens[offset] == NOT_TOKEN:
        len_, what = _evaluate_factor(tokens, contexts, offset + 1, end_token)
        len_, what = len_ + 1, not what
    elif tokens[offset] == LPAREN_TOKEN:
        len_, what = _evaluate_expression(tokens, contexts, offset + 1, RPAREN_TOKEN)
        len_ += 2
    else:
        _fail_expecting('expression', tokens[offset])

    return len_, what


def _evaluate_term(
    tokens: List[TOKEN],
    contexts: Dict[str, Any],
    offset: int,
    end_token: Union[TOKEN, List[TOKEN]] = END_TOKEN,
) -> Tuple[int, Optional[Any]]:
    len_, what = _evaluate_factor(tokens, contexts, offset)

    if _is_infix_operator(next_token := tokens[offset + len_]):
        len_rhs, rhs = _evaluate_factor(tokens, contexts, offset + len_ + 1, end_token)
        return len_ + 1 + len_rhs, evaluate_operation(what, next_token[VALUE], rhs)

    return len_, what


def _evaluate_expression(
    tokens: List[TOKEN],
    contexts: Dict[str, Any],
    offset: int,
    end_token: Union[TOKEN, List[TOKEN]] = END_TOKEN,
) -> Tuple[int, Optional[Any]]:
    """Parse and evaluate expression.

    infix = '==' | '!=' | '<=' | '<' | '>' | '>=' | '~='
    expression = term ('&&' term | '||' term)*
    term = factor (infix factor)?
    factor = path | string | number | '!'factor | '('expression')'

    # Required parameters

    - tokens: a list of tokens
    - contexts: a dictionary
    - offset: an integer

    # Optional parameters

    - end_token: a token or a list of tokens (END_TOKEN by default)

    # Returned value

    A pair.  The first element is an integer, the length of the
    evaluated segment (0 if empty).  The second element is an object
    (depending on `tokens`).  Could be a boolean, a number, a string, a
    list, or a dictionary.

    # Raised exceptions

    A _ValueError_ exception is raised if the expression is not valid.
    In particular, if the end of the expression is reached before
    finding an expected end token.
    """
    len_, what = _evaluate_term(tokens, contexts, offset)

    while (next_token := tokens[offset + len_]) in (AND_TOKEN, OR_TOKEN):
        len_rhs, rhs = _evaluate_term(tokens, contexts, offset + len_ + 1, end_token)
        len_ = len_ + 1 + len_rhs
        if next_token == AND_TOKEN:
            what = what and rhs
        else:
            what = what or rhs

    if next_token == end_token or next_token in end_token:
        return len_, what

    msg = 'operator' if end_token[0] is None else f'operator or "{end_token[0]}"'
    _fail_if_zero(0 if next_token == END_TOKEN else 1, msg)
    _fail_expecting(msg, next_token)


def evaluate(expr: str, contexts):
    """Perform expression evaluation, using contexts.

    # Required parameters

    - expr: a string
    - contexts: a dictionary

    # Returned value

    An object (depending on `expr`).  Could be a boolean, a number, a
    string, a list, or a dictionary.
    """
    return _evaluate_expression(tokenize(expr), contexts, 0)[1]


def evaluate_str(value: str, contexts):
    """Perform expression evaluation in string.

    `value` is either an expression or a string with expression(s) in
    it.

    # Required parameters

    - value: a string
    - contexts: a dictionary

    # Returned value

    If `value` is an expression, returns its evaluated value (can be
    any object).  If `value` contains expressions, returns a string
    with the expressions replaced by their values.
    """
    value = value.strip()
    if (
        value.startswith('${{')
        and value.endswith('}}')
        and value.count('${{') == 1
        and value.count('}}') == 1
    ):
        result = evaluate(value[3:-2].strip(), contexts)
    else:
        result = ''
        while '${{' in value:
            lhs, _, value = value.partition('${{')
            result += lhs
            expr, _, value = value.partition('}}')
            result += str(evaluate(expr.strip(), contexts))
        result += value
    return result


def evaluate_item(item, contexts):
    """Perform expression evaluation for item.

    If `item` is a list or dictionary, perform recursive evaluation.

    # Required parameters

    - item: any object
    - contexts: a dictionary

    # Returned value

    An object (same type as `item`).
    """
    if isinstance(item, dict):
        return evaluate_items(item, contexts)
    if isinstance(item, list):
        return [evaluate_item(entry, contexts) for entry in item]
    if isinstance(item, str):
        return evaluate_str(item, contexts)
    return item


def evaluate_items(items: Dict[str, Any], contexts) -> Dict[str, Any]:
    """Perform expression evaluation in items.

    If items contain sub-elements, the evaluation is performed recursively.

    If the referenced context element does not exist, raises a _KeyError_
    exception.

    Strip spaces around expressions, but does not strip spaces not in
    expressions.

    TODO: limit 'variables' context usage ('name', 'with', and 'if')
    """
    result = {}
    for item, value in items.items():
        if isinstance(value, str) and '${{' in value:
            result[item] = evaluate_str(value, contexts)
        elif isinstance(value, dict):
            result[item] = evaluate_items(value, contexts)
        elif isinstance(value, list):
            result[item] = [evaluate_item(entry, contexts) for entry in value]
        else:
            result[item] = value
    return result


def evaluate_bool(expr: str, contexts, special_functions=None) -> bool:
    """Evaluate expression in context.

    `expr` may be surrounded by `${{` and `}}`.

    `special_functions`, if provided, is a dictionary of function names
    to bools.

    # Required parameters

    - expr: a string
    - contexts: a dictionary

    # Optional parameters

    - special_functions: a dictionary or None (None by default)

    # Returned value

    A boolean.
    """
    expr = _maybe_remove_expression_syntax(expr)
    if special_functions:
        contexts = contexts.copy()
        contexts[SPECIAL_FUNCTIONS] = special_functions
    if '${{' in expr:
        return _to_number(evaluate_str(expr, contexts)) != 0
    return _to_number(evaluate(expr, contexts)) != 0


def _maybe_remove_expression_syntax(expr: str) -> str:
    """Strip expression syntax if present."""
    expr = expr.strip()
    if EXPRESSIONSYNTAX_MARK.match(expr):
        expr = expr[3:-2]
    return expr.strip()
