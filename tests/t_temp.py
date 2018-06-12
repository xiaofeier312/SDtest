from jsonpath_rw import Fields, jsonpath, parse,Root



d1={'foo': [{'baz': 1}, {'baz': 2}]}
jsp = parse("$.foo[0].baz")
r1=jsp.find(d1)
#r2 = Fields(jsp).update(d1,33)


jsp2 = parse("$..baz")
r2=jsp2.find(d1)

print(r2.value)

if __name__ == '__main__':
    print('r1 : {}'.format(r1))
    Root.update(jsp)