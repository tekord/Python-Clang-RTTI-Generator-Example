import clang.cindex

index = clang.cindex.Index.create()
translation_unit = index.parse('Dummy.cpp', args=['-std=c++17'])

for i in translation_unit.get_tokens(extent=translation_unit.cursor.extent):
    print (i.kind)
