from itertools import permutations

valid_strings = set()
pairs = [
  (["foo", "killedfoo"], ["killedfoo"], []),
  (["bar", "killedbar"], ["killedbar"], []),
  (["baz", "killedbaz"], ["killedbaz"], [])
]
import itertools
for p1 in pairs[0]:
  for p2 in pairs[1]:
    for p3 in pairs[2]:
      sub_items = p1 + p2 + p3
      for p in permutations(sub_items):
          valid = True
          if "foo" in p and p.index("foo") > p.index("killedfoo"): valid = False
          if "bar" in p and p.index("bar") > p.index("killedbar"): valid = False
          if "baz" in p and p.index("baz") > p.index("killedbaz"): valid = False
          if valid:
              valid_strings.add("".join(p))

with open('scratch.txt', 'w') as f:
    f.write('    let is_valid_r2 = case r2 of\n')
    for s in sorted(valid_strings):
        f.write(f'          "{s}" -> true\n')
    f.write('          _ -> false\n')
