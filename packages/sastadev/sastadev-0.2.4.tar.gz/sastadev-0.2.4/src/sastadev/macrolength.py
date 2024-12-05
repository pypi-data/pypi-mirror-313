from sastadev.macros import expandmacros, macrodict

resultlist = []
for macroname, macrovalue in macrodict.items():
    expandedmacrovalue = expandmacros(macrovalue)
    resultlist.append((macroname, len(expandedmacrovalue)))

querylist = ['//node[( %declarative% )]', '//node[( %Ond%  )',
             '//node[(   %Tarsp_B_X_count% = 3)]', '//node[%declarative% and %Ond%]',
             '//node[%declarative% and %Tarsp_B_X_count% = 3]']
#Invalid query: unknown error

queryresultlist = []
for query in querylist:
    expandedquery = expandmacros(query)
    queryresultlist.append((query, len(expandedquery)))

print('\n\nQueries:\n')
sortedqueryresultlist = sorted(queryresultlist, key=lambda x: x[1], reverse=True)
for (query, lvalue) in sortedqueryresultlist:
    print(f'{query}\t{lvalue}')

print('\n\nMacros:\n')
sortedresults = sorted(resultlist, key=lambda x: x[1], reverse=True)
for (name, lvalue) in sortedresults:
    print(f'{name}\t{lvalue}')
