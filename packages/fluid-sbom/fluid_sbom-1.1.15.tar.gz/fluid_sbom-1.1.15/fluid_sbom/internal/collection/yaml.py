import logging
import re
from contextlib import (
    suppress,
)
from typing import (
    Any,
    cast,
)

import tree_sitter_yaml
from tree_sitter import (
    Language as TLanguage,
)
from tree_sitter import (
    Node,
    Parser,
)

from fluid_sbom.internal.collection.types import (
    FileCoordinate,
    IndexedDict,
    IndexedList,
    Position,
)
from fluid_sbom.utils.exceptions import (
    UnexpectedChildrenLengthError,
    UnexpectedNodeError,
    UnexpectedNodeTypeError,
)

LOGGER = logging.getLogger(__name__)


def _generate_position(node: Node) -> Position:
    return Position(
        start=FileCoordinate(line=node.start_point[0] + 1, column=node.start_point[1] + 1),
        end=FileCoordinate(line=node.end_point[0] + 1, column=node.end_point[1] + 1),
    )


def _handle_block_mapping_node(
    node: Node,
) -> tuple[Node, IndexedDict[str, Any]]:
    data: IndexedDict[str, Any] = IndexedDict(node)
    for child in node.children:
        if child.type != "block_mapping_pair":
            continue
        childs = tuple(x for x in child.children if x.type != "comment")
        if len(childs) != 3:
            childs = (*childs, None)  # type: ignore
            try:
                if childs[1].type != ":":
                    raise UnexpectedChildrenLengthError(node, 3)
            except UnexpectedChildrenLengthError as exc:
                LOGGER.exception(
                    exc,
                    extra={
                        "node": node,
                        "childs": childs,
                    },
                )
                continue
        key_up_node, _, value_up_node = childs
        key_node, key_value = handle_node(key_up_node)
        if value_up_node is None:
            data[  # type: ignore
                (
                    key_value,
                    _generate_position(key_node),
                )
            ] = (
                None,
                None,
            )
            continue
        value_node, value_value = handle_node(value_up_node)
        data[(key_value, _generate_position(key_node))] = (
            value_value,
            _generate_position(value_node),
        )
    return node, data


def _handle_flow_mapping_node(
    node: Node,
) -> tuple[Node, IndexedDict[str, Any]]:
    pair_nodes = [x for x in node.children if x.type == "flow_pair"]
    data: IndexedDict[str, Any] = IndexedDict(node)
    for pair_node in pair_nodes:
        if len(pair_node.children) != 3:
            raise ValueError("Unexpected node")
        key_up_node, _, value_up_node = pair_node.children
        key_node, key_value = handle_node(key_up_node)
        value_node, value_value = handle_node(value_up_node)
        data[(key_value, _generate_position(key_node))] = (
            value_value,
            _generate_position(value_node),
        )
    return node, data


def _handle_boolean_scalar_node(node: Node) -> tuple[Node, bool]:
    node_string_value = node.text.decode("utf-8").lower() if node.text else "false"
    return node, node_string_value == "true"


def _handle_block_sequence_node(
    node: Node,
) -> tuple[Node, IndexedList[Position]]:
    data: IndexedList[Position] = IndexedList(node)
    for child in (x for x in node.children if x.type != "comment"):
        if child.type != "block_sequence_item":
            raise UnexpectedNodeTypeError(child.type, "block_sequence_item")
        resolved_item = handle_node(child)
        data.append((resolved_item[1], _generate_position(resolved_item[0])))
    return node, data


def _handle_block_sequence_item(node: Node) -> tuple[Node, Any]:
    if len(node.children) != 2 or node.children[0].type != "-":
        raise UnexpectedNodeTypeError(node)
    return handle_node(node.children[1])


def _handle_integer_scalar_node(node: Node) -> tuple[Node, int]:
    decode_str = node.text.decode("utf-8") if node.text else ""
    with suppress(ValueError):
        return node, int(decode_str)
    with suppress(ValueError):
        return node, int(decode_str, 16)
    raise ValueError(f"Invalid integer value: {decode_str}")


def _handle_flow_sequence_node(
    node: Node,
) -> tuple[Node, IndexedList[Position]]:
    data: IndexedList[Position] = IndexedList(node)
    for child in [x for x in node.children if x.type not in ("[", "]", ",")]:
        if child.type != "flow_node":
            raise UnexpectedNodeTypeError(child.type, "flow_node")
        resolved_node, resolved_item = handle_node(child)
        data.append((resolved_item, _generate_position(resolved_node)))
    return node, data


def _handle_float_scalar_node(node: Node) -> tuple[Node, float]:
    decoded_str = node.text.decode("utf-8") if node.text else ""
    with suppress(ValueError):
        return node, float(decoded_str)

    with suppress(ValueError):
        return node, float(decoded_str.replace(".", "").lower())

    raise ValueError(f"Invalid float value: {decoded_str}")


def _handle_block_scalar(node: Node) -> tuple[Node, str]:
    decoded_str = node.text.decode("utf-8") if node.text else ""
    value = ""
    if match := re.search(r"^>(\d+)", decoded_str):
        indent_spaces = int(match.group(1))
        decoded_str = re.sub(r"^>\d+", "", decoded_str).strip()
    else:
        indent_spaces = 1  # Default to no indent removal if no marker is found

    if decoded_str.startswith(">"):
        value = (" " * indent_spaces).join(decoded_str.lstrip(">+-").strip().split())
    elif decoded_str.startswith("|"):
        normalized_str = decoded_str.replace("\xa0", " ").lstrip("|+-")
        value = "\n".join(line.strip() for line in normalized_str.split("\n"))
        value = value.replace("\n", "", 1)
    return node, value


def handle_node(node: Node) -> tuple[Node, Any]:  # noqa: C901,PLR0912
    value: tuple[Node, Any] | None = None
    match node.type:
        case "block_node":
            if len(node.children) > 1:
                raise UnexpectedChildrenLengthError(node.type, 1)
            value = handle_node(node.children[0])
        case "block_mapping":
            value = _handle_block_mapping_node(node)
        case "flow_node" | "plain_scalar":
            if len(node.children) > 1:
                raise UnexpectedChildrenLengthError(node.type, 1)
            value = handle_node(node.children[0])
        case "string_scalar":
            value = node, node.text.decode("utf-8") if node.text else ""
        case "single_quote_scalar" | "double_quote_scalar":
            value = (
                node,
                node.text.decode("utf-8").strip("'\"") if node.text else "",
            )
        case "float_scalar":
            value = _handle_float_scalar_node(node)
        case "flow_mapping":
            value = _handle_flow_mapping_node(node)
        case "boolean_scalar":
            value = _handle_boolean_scalar_node(node)
        case "null_scalar":
            value = node, None
        case "integer_scalar":
            value = _handle_integer_scalar_node(node)
        case "block_sequence_item":
            value = _handle_block_sequence_item(node)
        case "block_sequence":
            value = _handle_block_sequence_node(node)
        case "flow_sequence":
            value = _handle_flow_sequence_node(node)
        case "block_scalar":
            value = _handle_block_scalar(node)
        case _:
            raise UnexpectedNodeError(node.type)
    return value


def parse_yaml_with_tree_sitter(
    content: str,
) -> IndexedDict | IndexedList | None:
    parser_language = TLanguage(tree_sitter_yaml.language())
    parser = Parser(parser_language)

    result = parser.parse(content.encode("utf-8"))
    documents = [x for x in result.root_node.children if x.type == "document"]
    if len(documents) != 1:
        return None
    block_node = next((x for x in documents[0].children if x.type == "block_node"), None)
    if not block_node:
        return None
    _, value = handle_node(block_node)
    return cast(IndexedDict | IndexedList, value)
