instructions=

name1 = str(instructions[0]).split("=")[0]
type1 = instructions[0].opcode


oper1= instructions[0].operands
operands1=[]

for x in oper1:
 operands1.append(x)




name2 = str(instructions[1]).split("=")[0]
type2 = instructions[1].opcode


oper2= instructions[1].operands
operands2=[]

for x in oper2:
 operands2.append(x)





k1 = KInstruction(name1,type1,operands1)
k2 = KInstruction(name2,type2,operands2)


divzerocheck(k2)


x = Int(str(operands1[0]).split(" ")[1])
y = int (str(operands1[1]).split(" ")[1])
s = Solver()


s.add(x+y== 0)

s.check()

