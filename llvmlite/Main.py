from llvmlite import binding as llvm
from z3 import * 
from KInstruction import *
from KModule import *
from KFunction import * 
from KBlock import * 
from graphviz import *
from KOperand import *
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()
import os

os.system("cd /libx32/llvmlite/ && clang-8  -emit-llvm divide3.c -S -o divide3.ll -Xclang -disable-O0-optnone && opt-8 divide3.ll -mem2reg -S -o output.ll")

ir = ""

#clang-8  -emit-llvm divide3.c -S -o divide3.ll -Xclang -disable-O0-optnone && opt-8 divide3.ll -mem2reg -S -o output.ll

with open("/libx32/llvmlite/output.ll", "r") as f:  
    ir = f.read() 




    


def printlist (list):
 for x in list: 
  print (x)




def isArgument (koperand):
   
   arguments = koperand.instruction.block.function.arguments #valueref 数组

   s = str(koperand.valueref)

   for x in arguments:
     if(str(x) == s):
       return True

   return False    
   
   
  


def isInstruction (koperand) :

   instructions= koperand.instruction.block.instructions
    
   s = str(koperand.valueref)

   for x in instructions:
     if(str(x) == s):
       return True

   return False   

def getKInstruction (koperand) :

   s = str(koperand.valueref)

   for x in kinstructions:
     if((str(x.valueref) == s) and (koperand.instruction.block == x.block) ):
        return x   

def isConstant(koperand):
    s = str(koperand.valueref).split(" ")[1]
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False


  



def getListfromIter (iter):
   list = []
   for x in iter :
     list.append (x)
   return list

def getArgumentSymbolMapfromIter (iter):
   dict = {}
   for x in iter :
     dict[str(x).split(" ")[1]] =Int(str(x).split(" ")[1])
   return (dict)   

def indexOf (list,x):
  index = -1
  for n in range(len(list)):
   if(list[n]==x):
      index =n
  return index    


def opcodetoformula (opcode):

  if(opcode =="add"):
    return "+"
  if(opcode =="sub"):
    return "-"  
  if(opcode =="mul"):
    return "*"  
  if(opcode =="sdiv"):
    return "/"  


def findoriginexpr (koperand):   
  
  if(isArgument(koperand) ):
    
    return koperand.instruction.block.function.symbol[str(koperand.valueref).split(" ")[1]]
  
  if(isConstant (koperand)):

    return int(str(koperand.valueref).split(" ")[1])

  else :

     instruction = getKInstruction(koperand)


     operands=instruction.operands

     opcode = instruction.type
     
     if(len(operands) == 2):       #二元运算表达式
       koperand1 =""
       koperand2 = ""
       for x in koperands:
          if(x.valueref == operands[0]):
             koperand1=x  
       for x in koperands:
          if(x.valueref == operands[1]):
             koperand2=x  

     if(opcode =="add"):
         return (findoriginexpr(koperand1) + findoriginexpr(koperand2)) 
     if(opcode =="sub"):
         return (findoriginexpr(koperand1) - findoriginexpr(koperand2))
     if(opcode =="mul"):
         return (findoriginexpr(koperand1) * findoriginexpr(koperand2))
     if(opcode =="sdiv"):
         return (findoriginexpr(koperand1) /findoriginexpr(koperand2)) 
     
    


  
   
  
   




mref=llvm.parse_assembly(ir)


globalvariables = getListfromIter(mref.global_variables)



functions=getListfromIter(mref.functions)




m = KModule(globalvariables,functions)


kfunctions=[]

for x in functions:
  kfunctions.append(KFunction(m,x.name,getListfromIter(x.blocks),getListfromIter(x.arguments),x,getArgumentSymbolMapfromIter(x.arguments)))





kblocks=[]

for i in range(len(kfunctions)):

  for j in range(len(kfunctions[i].blocks)):

   kblocks.append(KBlock(kfunctions[i],getListfromIter(kfunctions[i].blocks[j].instructions),kfunctions[i].blocks[j]))

blocks=kfunctions[1].blocks


kinstructions=[]


for i in range(len(kblocks)):
    
    for j in range(len(kblocks[i].instructions)):
       
       kinstructions.append(KInstruction(kblocks[i],kblocks[i].instructions[j].opcode,getListfromIter(kblocks[i].instructions[j].operands),kblocks[i].instructions[j] ))
      



koperands=[]


for i in range(len(kinstructions)):
    
    for j in range(len(kinstructions[i].operands)):
       
       koperands.append(KOperand(kinstructions[i],kinstructions[i].operands[j],j))















def analysisFunction(kfunction):
  
  filter=[]

  for x in kinstructions:

    if(x.block.function.functionname == kfunction.functionname):

      filter.append(x)

  for x in filter :

    if (x.type == "sdiv") :

     for y in range(len( koperands)):

       if(x == koperands[y].instruction): #对象相等
            
          operand = koperands[y+1] #分母
          if(x == koperands[y+1].instruction and (isArgument(operand) or isInstruction(operand))):#对象相等
         
           expr = findoriginexpr(operand)
          
           s = Solver()
     
           s.add( expr ==0)
           s.check()
           if str(s.check())=='sat' :
             print("发现除零错")
             print(s.model())
           else:
             print("未发现除零错")
                 


analysisFunction(kfunctions[0])





llvm.shutdown()

















