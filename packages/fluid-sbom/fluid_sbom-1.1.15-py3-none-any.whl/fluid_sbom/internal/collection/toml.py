import logging
import re
from collections.abc import Iterator
from contextlib import (
    suppress,
)
from typing import (
    Any,
)

import tree_sitter_toml
from more_itertools import (
    mark_ends,
)
from tree_sitter import (
    Language as TLanguage,
)
from tree_sitter import (
    Node,
    Parser,
)

from fluid_sbom.internal.collection.types import (
    IndexedDict,
    IndexedList,
)
from fluid_sbom.utils.exceptions import (
    DuplicatedKeyError,
    InvalidDocumentKeyPairError,
    InvalidTypeError,
    UnexpectedNodeError,
)

LOGGER = logging.getLogger(__name__)


def _validate_key_pairs(root_node: Node) -> None:
    all_children_pairs = tuple(
        node.start_point[0] for node in root_node.children if node.type == "pair"
    )
    if len(all_children_pairs) != len(set(all_children_pairs)):
        raise InvalidDocumentKeyPairError


def handle_string(node: Node) -> str:
    value = node.text.decode("utf-8") if node.text else ""
    str_quote = "'" if value.startswith("'") else None
    str_quote = str_quote or ('"' if value.startswith('"') else None)
    if str_quote and (value.startswith(str_quote)) and (value.endswith(str_quote)):
        value = value.strip(str_quote)
        # Remove surrounding triple quotes if present
        value = re.sub(r'"""|\'\'\'', "", value)

        value = value.strip()

    return value


def handle_array(node: Node) -> IndexedList[Node]:
    data: IndexedList[Node] = IndexedList(node)
    for children_node in node.children:
        if children_node.type in ("[", "]", ",", "comment"):
            continue
        data.append((handle_node(children_node), children_node))
    return data


def handle_bare_key(node: Node) -> str:
    return handle_string(node)


def handle_quoted_key(node: Node) -> str:
    value = handle_string(node)
    if value.startswith(('"', "'")):
        return value[1:-1]
    return value


def handle_dotted_key(node: Node) -> list[str]:
    value = handle_string(node)
    parts = re.findall(r'"[^"]*"|[\w-]+', value)
    return [part.strip('" ') for part in parts]


def handle_table_array_element(
    node: Node,
) -> tuple[tuple[str | list[str], Node], IndexedDict[str, Any]]:
    data: IndexedDict[str, Any] = IndexedDict(node)
    bare_key = node.named_children[0]
    bare_key_value = handle_node(bare_key)

    # the children's are pair nods
    for children_node in node.named_children[1:]:
        if children_node.type in ("[", "]", ", ", "comment"):
            continue
        if children_node.type != "pair":
            raise UnexpectedNodeError(children_node)
        key, value = handle_node(children_node)
        data[key] = value
    return (bare_key_value, bare_key), data


def handle_pair(node: Node) -> tuple[tuple[str, Node], tuple[Any, Node]]:
    bare_key_node, value_node = node.named_children[:2]
    bare_key_value = handle_node(bare_key_node)
    value_resolved = handle_node(value_node)
    return (bare_key_value, bare_key_node), (value_resolved, value_node)


def handle_boolean(node: Node) -> bool:
    value = node.text.decode("utf-8") if node.text else ""
    return value.lower() == "true"


def handle_integer(node: Node) -> int:
    decode_str = node.text.decode("utf-8") if node.text else ""
    with suppress(ValueError):
        return int(decode_str)
    with suppress(ValueError):
        return int(decode_str, 16)
    with suppress(ValueError):
        return int(decode_str, 8)

    raise ValueError(f"Invalid integer value: {decode_str}")


def handle_float(node: Node) -> float:
    decoded_str = node.text.decode("utf-8") if node.text else ""
    with suppress(ValueError):
        return float(decoded_str)

    with suppress(ValueError):
        return float(decoded_str.replace(".", "").lower())

    raise ValueError(f"Invalid float value: {decoded_str}")


def handle_local_date(node: Node) -> str:
    return handle_string(node)


def handle_inline_table(node: Node) -> IndexedDict[str, Any]:
    data: IndexedDict[str, Any] = IndexedDict(node)
    for children_node in node.named_children:
        key, value = handle_node(children_node)
        nested_dict(
            data=data,
            keys=key[0],
            keys_node=key[1],
            value=value[0],
            value_node=value[1],
        )
    return data


def handle_table(node: Node, data_1: IndexedDict[str, Any]) -> None:
    data_new: IndexedDict[str, Any] = IndexedDict(node)
    for children_node in node.named_children[1:]:
        if children_node.type == "comment":
            continue
        key, value = handle_node(children_node)
        nested_dict(
            data=data_new,
            keys=key[0],
            keys_node=key[1],
            value=value[0],
            value_node=value[1],
        )
    bare_key_node = node.named_children[0]
    bare_key_value = handle_node(bare_key_node)
    if isinstance(bare_key_value, list):
        nested_dict(
            data=data_1,
            keys=bare_key_value,
            keys_node=bare_key_node,
            value=data_new,
            value_node=node,
        )
    else:
        data_1[(bare_key_value, bare_key_node)] = (
            data_new,
            node,
        )


def handle_node(node: Node) -> Any:  # noqa: C901, PLR0912
    value: Any | None = None
    match node.type:
        case "comment":
            value = None
        case "string":
            value = handle_string(node)
        case "array":
            value = handle_array(node)
        case "pair":
            value = handle_pair(node)
        case "bare_key":
            value = handle_bare_key(node)
        case "quoted_key":
            value = handle_quoted_key(node)
        case "dotted_key":
            value = handle_dotted_key(node)
        case "boolean":
            value = handle_boolean(node)
        case "integer":
            value = handle_integer(node)
        case "float":
            value = handle_float(node)
        case "inline_table":
            value = handle_inline_table(node)
        case "local_date":
            value = handle_local_date(node)
        case _:
            raise UnexpectedNodeError(node.type)

    return value


def _nested_dict_handle_list(data: Any) -> IndexedDict:
    if not isinstance(data, IndexedDict):
        if not isinstance(data, IndexedList):
            raise InvalidTypeError("Attempted to extend non-table type")
        data = data[-1]
    return data


def _nested_dict_validate_duplicated_data(data: IndexedDict, key: str, is_last: bool) -> None:
    try:
        if is_last and key in data:
            raise DuplicatedKeyError(key)
    except DuplicatedKeyError as exc:
        LOGGER.exception(
            exc,
            extra={
                "extra": {
                    "key": key,
                    "is_last": is_last,
                },
            },
        )


def nested_dict(
    *,
    data: IndexedDict,
    keys: list[str] | str,
    keys_node: Node,
    value: Any | None = None,
    value_node: Node | None = None,
) -> None:
    build_key = []
    for _, is_last, key in _mark_ends(keys):
        build_key.append(key)
        data = _nested_dict_handle_list(data)

        _nested_dict_validate_duplicated_data(data, key, is_last)
        if key not in data:
            if is_last:
                data[(key, keys_node)] = (
                    value if value is not None else IndexedDict(),
                    value_node or keys_node,
                )
                continue
            data[(key, keys_node)] = (IndexedDict(), value_node or keys_node)
        data = data[key]


def _mark_ends(keys: list[str] | str) -> Iterator[tuple[bool, bool, str]]:
    yield from mark_ends(keys if isinstance(keys, list) else [keys])


def _nested_list_handle_list(data: Any) -> IndexedDict:
    if isinstance(data, IndexedList):
        data = data[-1]
    return data


def _nested_list_handle_fists_keys(data: IndexedDict, key: str, is_last: bool) -> bool:
    return key not in data and not is_last


def _nested_list_handle_last_keys(data: IndexedDict, key: str, is_last: bool) -> bool:
    return key not in data and is_last


def _nested_list_handle_fists_keys_exists(data: IndexedDict, key: str, is_last: bool) -> bool:
    return key in data and not is_last


def nested_list(
    *,
    data: IndexedDict,
    keys: list[str] | str,
    keys_node: Node,
    value: Any | None = None,
    value_node: Node | None = None,
) -> None:
    build_key = []
    for _, is_last, key in _mark_ends(keys):
        build_key.append(key)
        data = _nested_list_handle_list(data)

        if _nested_list_handle_fists_keys(data, key, is_last):
            data[(key, keys_node)] = (IndexedDict(), value_node or keys_node)
            data = data[key]
            continue
        if _nested_list_handle_fists_keys_exists(data, key, is_last):
            data = data[key]
            continue

        if _nested_list_handle_last_keys(data, key, is_last):
            data[(key, keys_node)] = (
                IndexedList(keys_node),
                value_node or keys_node,
            )
        if is_last:  # if the doted key is the last, the item is a value to append
            try:
                data[key].append((value, value_node or keys_node))
            except AttributeError as exc:
                raise InvalidTypeError(
                    f"Attempted to extend non-table type: {'.'.join(build_key)}",
                ) from exc
            continue
        data = data[key]


def parse_toml_with_tree_sitter(toml_content: str) -> IndexedDict:
    parser_language = TLanguage(tree_sitter_toml.language())
    parser = Parser(parser_language)

    result = parser.parse(toml_content.encode("utf-8"))
    data: IndexedDict = IndexedDict(result.root_node)
    if result.root_node.type != "document":
        return data
    _validate_key_pairs(result.root_node)
    for node in result.root_node.children:
        try:
            if node.type == "pair":
                key, pair_value = handle_node(node)
                nested_dict(
                    data=data,
                    keys=key[0],
                    keys_node=key[1],
                    value=pair_value[0],
                    value_node=pair_value[1],
                )
            elif node.type == "table":
                handle_table(node, data)
            elif node.type == "table_array_element":
                key, value = handle_table_array_element(node)
                nested_list(
                    data=data,
                    keys=key[0],
                    keys_node=key[1],
                    value=value,
                    value_node=node,
                )
            elif node.type == "ERROR":
                raise UnexpectedNodeError(node)
        except UnexpectedNodeError as exc:
            LOGGER.exception(
                exc,
                extra={
                    "extra": {
                        "node_type": node.type,
                        "toml": toml_content,
                    },
                },
            )
            continue

    return data
