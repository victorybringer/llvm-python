from z3 import *
x = Int('%0')
y= int("9")

print(x)
s = Solver()
s.add(x+y-5 ==0)
s.check()
print(s.model())