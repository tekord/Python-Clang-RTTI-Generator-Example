import clang.cindex
import typing

index = clang.cindex.Index.create()
translation_unit = index.parse('Nodes.h', args=['-std=c++17'])

def filter_node_list_by_file(
    nodes: typing.Iterable[clang.cindex.Cursor],
    file_name: str
) -> typing.Iterable[clang.cindex.Cursor]:
    result = []

    for i in nodes:
        if i.location.file.name == file_name:
            result.append(i)

    return result

def filter_node_list_by_node_kind(
    nodes: typing.Iterable[clang.cindex.Cursor],
    kinds: list
) -> typing.Iterable[clang.cindex.Cursor]:
    result = []

    for i in nodes:
        if i.kind in kinds:
            result.append(i)

    return result

def is_exposed_field(node):
    return node.access_specifier == clang.cindex.AccessSpecifier.PUBLIC

def find_all_exposed_fields(
    cursor: clang.cindex.Cursor
):
    result = []

    field_declarations = filter_node_list_by_node_kind(cursor.get_children(), [clang.cindex.CursorKind.FIELD_DECL])

    for i in field_declarations:
        if not is_exposed_field(i):
            continue

        result.append(i.displayname)

    return result

source_nodes = filter_node_list_by_file(translation_unit.cursor.get_children(), translation_unit.spelling)
all_classes = filter_node_list_by_node_kind(source_nodes, [clang.cindex.CursorKind.CLASS_DECL, clang.cindex.CursorKind.STRUCT_DECL])

class_inheritance_map = {}
class_field_map = {}

for i in all_classes:
    bases = []

    for node in i.get_children():
        if node.kind == clang.cindex.CursorKind.CXX_BASE_SPECIFIER:
            referenceNode = node.referenced

            bases.append(node.referenced)

    class_inheritance_map[i.spelling] = bases

for i in all_classes:
    fields = find_all_exposed_fields(i)

    class_field_map[i.spelling] = fields

def populate_field_list_recursively(class_name: str):
    field_list = class_field_map.get(class_name)

    if field_list is None:
        return []

    baseClasses = class_inheritance_map[class_name]

    for i in baseClasses:
        field_list = populate_field_list_recursively(i.spelling) + field_list

    return field_list

rtti_map = {}

for class_name, class_list in class_inheritance_map.items():
    rtti_map[class_name] = populate_field_list_recursively(class_name)

for class_name, field_list in rtti_map.items():
    wrapper_template = """\
RTTI_PROVIDER_BEGIN_TYPE(%s)
(
%s
)
RTTI_PROVIDER_END_TYPE()
"""

    rendered_fields = []

    for f in field_list:
        rendered_fields.append("    RTTI_DEFINE_FIELD(%s, %s)" % (class_name, f))

    print (wrapper_template % (class_name, ",\n".join(rendered_fields)))
