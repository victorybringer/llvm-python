from llvmlite import binding as llvm
from z3 import * 
from KInstruction import *
from KModule import *
from KFunction import * 
from KBlock import * 
from graphviz import *
from KOperand import *
from Callcollection import *
from KDeclare import *
from pydot import *
import re
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()
import os
import json

os.system("cd /libx32/llvmlite/ && clang-10  -emit-llvm overflow.c -g -S -o overflow.c.ll ")
#os.system("cd /libx32/llvmlite/ && clang-8  -emit-llvm test2.cpp -g -S -o test2.ll -Xclang -disable-O0-optnone && opt-8 test2.ll -mem2reg -S -o test2.ll")
ir = ""

#clang-8  -emit-llvm Divide_By_Zero_Test01.c -S -o divide3.ll -Xclang -disable-O0-optnone && opt-8 divide3.ll -mem2reg -S -o output.ll

with open("/libx32/llvmlite/overflow.c.ll", "r") as f:  
    ir = f.read() 

def isglobalsigned(globalvariable):
    metadata=re.findall(r"!dbg !\d+",globalvariable)[0].split(" ")[1]
    return metadatatobasetype(metadata)
    

def llvmdbgdeclare(kinstruction):
  name=str(kinstruction.valueref).split("=")[0].strip()
  for x in kinstruction.block.instructions:
    if(len(re.findall(r""+name,str(x.valueref)))>0 and len(re.findall(r"@llvm.dbg.declare",str(x.valueref)))>0):
      metadata=(re.findall(r"metadata !\d+",str(x.valueref))[0].split(" ")[1])
      
      return metadatatobasetype(metadata) 


def metadatatobasetype(metadata):
  dbginfo=(re.findall(metadata+r" =.+", ir)[0])

  if(re.findall(r"DIBasicType",dbginfo)):
    data=re.findall(r"\(.*\)",dbginfo)[0].split(",")[0].split(" ")[1]
    if(re.findall(r"unsigned",data)):
     return False
    return True
  if(re.findall(r"!DIDerivedType",dbginfo) or re.findall(r"!DICompositeType",dbginfo)):
    type=(re.findall(r"baseType: !\d+",dbginfo)[0])
    return metadatatobasetype(type.split(" ")[1])
  if(re.findall(r"!DIGlobalVariableExpression",dbginfo) ):
    type=(re.findall(r"var: !\d+",dbginfo)[0])
    return metadatatobasetype(type.split(" ")[1])  
  if((re.findall(r"!DIGlobalVariable",dbginfo) and not (re.findall(r"!DIGlobalVariableExpression",dbginfo))) or re.findall(r"!DISubprogram",dbginfo) or re.findall(r"DILocalVariable",dbginfo)):
    type=(re.findall(r"type: !\d+",dbginfo)[0])
    return metadatatobasetype(type.split(" ")[1])
  if(re.findall(r"!DISubroutineType",dbginfo) ):
    types=(re.findall(r"types: !\d+",dbginfo)[0])
    return metadatatobasetype(types.split(" ")[1])  
  if(not re.findall(r"!DI",dbginfo) ):
    return metadatatobasetype(re.findall(r"!\d+",dbginfo)[1])   
 
  
def dbgcorrect(kinstruction):         # 貌似是一个bug,instruction 字符串返回的调试信息与实际不一致，经常造成定位行数与实际不符    

   kfunction=str(kinstruction.block.function.valueref)
   
   blocks=kinstruction.block.function.blocks

   
   blockindex=-1
   for x in range(len(blocks)):
      if( blocks[x] == kinstruction.block):
        blockindex=x  
   
   
   
   
   instructions=kinstruction.block.instructions
   


  


   instructionindex=-1
   for x in range(len(instructions)):
      if(instructions[x] == kinstruction):
        instructionindex=x  
   

   strs=kfunction.split("\n") #function字符串按行处理
   
   index=0
   
   for x in range(0,blockindex):
   
    index+=len(blocks[x].instructions)
   
   index+=2*(blockindex+1)

   index+=instructionindex



   return strs[index].split("!")[2]
  




def findkblock (valueref,kfunction) :
  
  for x in kfunction.blocks:
    if(str(valueref) == str(x.valueref)):
      return x
   
def isGlobal (koperand):
   
   globals = mref.global_variables #valueref 数组
   
   s = str(koperand.valueref).strip()
   
   for x in globals:
     if(str(x).strip() == s):
       
       return True

   return False  

def isArgument (koperand):
   
   arguments = koperand.instruction.block.function.arguments #valueref 数组

   s = str(koperand.valueref)

   for x in arguments:
     if(str(x) == s):
       return True

   return False    
   
   

def set_blocknames(kfunction):

 s=llvm.get_function_cfg(kfunction.valueref)



 dotG = graph_from_dot_data(s)[0]

 dotG.write_png("/libx32/llvmlite/"+kfunction.functionname+".png")
 
 blocknames=[]


 for each_node in dotG.get_nodes():
       
        for each_attr_key, each_attr_val in each_node.get_attributes().items():
           if(each_attr_key == "label"):

            ## print (("label "+re.findall(r"%\d+", each_attr_val)[0],re.findall(r"label %\d+", each_attr_val)))
            blocknames.append("label "+re.findall(r"%\d+", each_attr_val)[0])
 for i in range(len(kfunction.blocks)):
            kfunction.blocks[i].name= blocknames[i]   


def isInstruction (koperand) :

   s = str(koperand.valueref)

   for x in kinstructions:
     if((str(x.valueref) == s) and (koperand.instruction.block.function == x.block.function) ):
       return True

   return False   

def getKInstruction (koperand) :

   s = str(koperand.valueref)

   for x in kinstructions:
     if((str(x.valueref) == s) and (koperand.instruction.block.function == x.block.function) ):
        return x   

def getKFunction (koperand) :

   s = str(koperand.valueref)

   for x in kfunctions:
     if(str(x.valueref) == s):
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



def typetosymbol(x,type):
  name=str(type)
  if(name=="i64" or name=="i64*"):
    return BitVec(x,64)
  if(name=="i32" or name=="i32*"):
    return BitVec(x,32)
  if(name=="i16" or name=="i16*"):
    return BitVec(x,16)
  if(name=="i8" or name=="i8*"):
    return BitVec(x,8)
  if(name=="float" ):
    return Real(x)
  if(name=="double" ):
    return Real(x)  

def Constanttype(x,type):
  
   if(type=="i64"  or type=="i64*"):
    return BitVecVal(x,64)
   if(type=="i32"  or type=="i32*"):
    return BitVecVal(x,32)
   if(type=="i16" or type=="i16*" ):
    return BitVecVal(x,16)
   if(type=="i8" or type=="i8*" ):
    return BitVecVal(x,8)
   

def getArgumentSymbolMapfromIter (name,iter):
   dict = {}
   for x in iter :
     
      
      dict[name+"@"+str(x).split(" ")[1]] =typetosymbol(name+"@"+str(x).split(" ")[1],x.type)
      #dict[name+"@"+str(x).split(" ")[1]] =Int(name+"@"+str(x).split(" ")[1])
   return (dict)   

def indexOf (list,x):
  index = -1
  for n in range(len(list)):
   if(list[n]==x):
      index =n
  return index    

def findmemorysize(koperand,offsetsize):  #溯源至内存时，提供内存的大小信息
   p = re.compile(r'[[](.*?)[]]', re.S)
   if(len(re.findall(p, str(koperand.valueref)))>0):
    print(offsetsize) 
    return Constanttype(int(re.findall(p, str(koperand.valueref)) [0][0]),offsetsize)
   else:

    return typetosymbol(koperand.instruction.block.function.functionname+"@"+str(koperand.valueref).split("=")[0].strip()+"memorysize",offsetsize)
   

def getTrueExpr(condition,analysispath,memory):
   
   if(len(re.findall(r"slt", str(condition.valueref)))!=0):  #有符号数小于 signed less than
       return findoriginexpr(condition.operands[0],analysispath,len(analysispath)-1,memory) - findoriginexpr(condition.operands[1],analysispath,len(analysispath)-1,memory) < 0     
   if(len(re.findall(r"sgt", str(condition.valueref)))!=0):  #有符号数大于 signed greater than
       return findoriginexpr(condition.operands[0],analysispath,len(analysispath)-1,memory) - findoriginexpr(condition.operands[1],analysispath,len(analysispath)-1,memory) > 0       
   if(len(re.findall(r"eq", str(condition.valueref)))!=0):  #等于 
       return findoriginexpr(condition.operands[0],analysispath,len(analysispath)-1,memory) - findoriginexpr(condition.operands[1],analysispath,len(analysispath)-1,memory) == 0
   if(len(re.findall(r"ne", str(condition.valueref)))!=0):  #不等于 
       return findoriginexpr(condition.operands[0],analysispath,len(analysispath)-1,memory) - findoriginexpr(condition.operands[1],analysispath,len(analysispath)-1,memory) != 0
   if(len(re.findall(r"sle", str(condition.valueref)))!=0):  #有符号数小于等于 signed less equal
       
       return findoriginexpr(condition.operands[0],analysispath,len(analysispath)-1,memory) - findoriginexpr(condition.operands[1],analysispath,len(analysispath)-1,memory) <= 0     
   if(len(re.findall(r"sge", str(condition.valueref)))!=0):  #有符号数大于等于 signed greater equal
       return findoriginexpr(condition.operands[0],analysispath,len(analysispath)-1,memory) - findoriginexpr(condition.operands[1],analysispath,len(analysispath)-1,memory) >= 0  

def findoriginexpr (koperand,analysispath,loopcounter,memory):   #要添加一个计数变量,表明当前指令在分析路径的哪个基本块内，尤其适用于循环时的多次回溯
  
  if(isGlobal(koperand)):
    
  
    return m.global_variables[koperand.valueref.name]

  if(isArgument(koperand) ):
    
    return koperand.instruction.block.function.symbol[koperand.instruction.block.function.functionname+"@"+str(koperand.valueref).split(" ")[1]]
  
  if(isConstant (koperand)):
    
    type=str(koperand.valueref).split(" ")[0]
    if(type!="double" and type!="float"):
     return Constanttype(int(str(koperand.valueref).split(" ")[1]),type)
    else:
     return 0 

  else :
  
     instruction = getKInstruction(koperand)
   
     currentblock=instruction.block.name
     
     blocknumber = -1
     for x in range (len(analysispath)):
          if (currentblock == analysispath[x] and x <=loopcounter):

               blocknumber=x

     loopcounter = blocknumber
  
     operands=instruction.operands

     opcode = instruction.type
     

     if(opcode =="phi"):
        
         lastblockname = analysispath[loopcounter-1].split(" ")[1]   #loopcounter表明当前指令在处分析路径的哪个位置，初衷是解决循环问题
         expr=instruction.valueref
         
         
         p = re.compile(r'[[](.*?)[]]', re.S)


         list=re.findall(p, str(expr))
                                                                   #用正则表达式得到phi节点的匹配值
         index=0
         for i in range(len(list)):
          result=re.findall(r""+lastblockname,list[i])
          if (len(result)>0):
            index=i
            
          
         return  findoriginexpr(operands[index],analysispath,loopcounter-1,memory)

         ## print(operands[index].valueref)
           

     if(opcode == "call"  ):
         
         return instruction.block.function.symbol[instruction.block.function.functionname+"@"+str(instruction.valueref).split("=")[0].strip()]
     if( opcode == "alloca" ):
         
         return memory[instruction.block.function.functionname+"@"+str(instruction.valueref).split("=")[0].strip()]
     if(len(operands) == 2):       #二元运算表达式
       koperand1 =operands[0]
       koperand2 = operands[1]
 
       if(opcode =="add"):
         return (findoriginexpr(koperand1,analysispath,loopcounter,memory) + findoriginexpr(koperand2,analysispath,loopcounter,memory)) 
       if(opcode =="sub"):
         return (findoriginexpr(koperand1,analysispath,loopcounter,memory) - findoriginexpr(koperand2,analysispath,loopcounter,memory))
       if(opcode =="mul"):
         return (findoriginexpr(koperand1,analysispath,loopcounter,memory) * findoriginexpr(koperand2,analysispath,loopcounter,memory))
       #if(opcode =="shl"):
        # return (findoriginexpr(koperand1,analysispath,loopcounter,memory) * findoriginexpr(koperand2,analysispath,loopcounter,memory)*2)  
       if(opcode =="sdiv"):
         return (findoriginexpr(koperand1,analysispath,loopcounter,memory) / findoriginexpr(koperand2,analysispath,loopcounter,memory))
        
           
     if(len(operands) == 1):       #一元运算表达式
       koperand1 =operands[0]
      
 
       if(opcode =="load"):
       
         return findoriginexpr(koperand1,analysispath,loopcounter,memory)

       if(opcode =="sext" ):
         large=int(str(instruction.valueref).strip().split(" ")[6][1:-1])
         small=int(str(instruction.valueref).strip().split(" ")[3][1:])
         
        
         return SignExt(large-small,findoriginexpr(koperand1,analysispath,loopcounter,memory))
       
       if(opcode =="zext" ):
         large=int(str(instruction.valueref).strip().split(" ")[6][1:-1])
         small=int(str(instruction.valueref).strip().split(" ")[3][1:])
         return ZeroExt(large-small,findoriginexpr(koperand1,analysispath,loopcounter,memory))
       
    
       if(opcode =="trunc" ):
         large=int(str(instruction.valueref).strip().split(" ")[3][1:])
         small=int(str(instruction.valueref).strip().split(" ")[6][1:-1])
         return Extract(large-1,small,findoriginexpr(koperand1,analysispath,loopcounter,memory))
        
       
     if(len(operands) ==3):    
    
      koperand1 =operands[0]
      koperand2 =operands[1]
      koperand3 =operands[2]
      if(opcode == "getelementptr") :  #getelementptr 包含三要素 内存地址 基址 偏移量   
          
         return findoriginexpr(koperand3,analysispath,loopcounter,memory) 



mref=llvm.parse_assembly(ir)


globalvariables = getListfromIter(mref.global_variables)



functions=getListfromIter(mref.functions)




m = KModule(globalvariables,functions)

globals={}

for x in m.global_variables:
  if(len(re.findall(r"global",str(x)))>0):
   
   globals[str(x.name)]=Constanttype(int(str(x).split("=")[-1].strip().split(" ")[indexOf(str(x).split("=")[-1].strip().split(" "),"global")+2][0:-1]),str(x.type))

m.global_variables=globals

print(globals)

callInstexprcollection=[]
kfunctions=[]

for x in functions:
  if(x.is_declaration == False ):
   kfunctions.append(KFunction(m,x.name,getListfromIter(x.blocks),getListfromIter(x.arguments),x,getArgumentSymbolMapfromIter(x.name,x.arguments)))


m.functions=kfunctions

kdeclares=[]
for x in functions:
  if(x.is_declaration  ):
    kdeclares.append(KDeclare(m,x.name,x))
kblocks=[]

for i in range(len(kfunctions)):

  for j in range(len(kfunctions[i].blocks)):

   kblocks.append(KBlock(kfunctions[i],getListfromIter(kfunctions[i].blocks[j].instructions),kfunctions[i].blocks[j]))


for i in range(len(kfunctions)):
  
   kfunctions[i].blocks=[]

for i in range(len(kfunctions)):
 for j in range(len(kblocks)):

   if(kfunctions[i]==kblocks[j].function):
  
    kfunctions[i].blocks.append(kblocks[j])









kinstructions=[]


for i in range(len(kblocks)):
    
    for j in range(len(kblocks[i].instructions)):
       
       kinstructions.append(KInstruction(kblocks[i],kblocks[i].instructions[j].opcode,getListfromIter(kblocks[i].instructions[j].operands),kblocks[i].instructions[j] ))
      



for i in range(len(kblocks)):
  
   kblocks[i].instructions=[]

for i in range(len(kblocks)):
 for j in range(len(kinstructions)):

   if(kblocks[i]==kinstructions[j].block):
  
    kblocks[i].instructions.append(kinstructions[j])




koperands=[]


for i in range(len(kinstructions)):
    
    for j in range(len(kinstructions[i].operands)):
       
       koperands.append(KOperand(kinstructions[i],kinstructions[i].operands[j],j))




for i in range(len(kinstructions)):
  
   kinstructions[i].operands=[]

for i in range(len(kinstructions)):
 for j in range(len(koperands)):

   if(kinstructions[i]==koperands[j].instruction):
  
    kinstructions[i].operands.append(koperands[j])





def SymbolicExecution(kblock,analysispath,constraint,functionstack,callcollection,currentmemoryregion):   #运用符号执行的过程内、间分析,functionstack 代表过程间分析路径
  
  

  filter=[]

  for x in kblock.instructions:

    filter.append(x)

      

  for x in filter :
    if (x.type == "add" or x.type == "sub" ) :
         koperand1=x.operands[0]
         koperand2=x.operands[1]
         
         destination=""
         resultsymbol=str(x.valueref).split("=")[0].strip()
       
         s = Solver()
         for y in x.block.function.blocks:
          for u in y.instructions:
             
             

             if((u.type=="trunc" or u.type=="zext" or u.type=="sext")and re.findall(r""+resultsymbol,str(u.valueref))):
           
               resultsymbol=str(u.valueref).split("=")[0].strip()
              
             if(u.type=="store" and re.findall(r""+resultsymbol,str(u.valueref))):
               destination=u.operands[1]
               break
         print(destination)
         issigned=''
         if(isGlobal(destination)):
           issigned=isglobalsigned(str(destination.valueref))
         else:
           issigned=llvmdbgdeclare(getKInstruction(destination))   
         

         print(issigned)
         if(issigned):
          if(x.type=="add"):  
           s.add(Or(BVAddNoOverflow(findoriginexpr(koperand1,analysispath,len(analysispath)-1,currentmemoryregion),findoriginexpr(koperand2,analysispath,len(analysispath)-1,currentmemoryregion),True) == False,BVAddNoUnderflow(findoriginexpr(koperand1,analysispath,len(analysispath)-1,currentmemoryregion),findoriginexpr(koperand2,analysispath,len(analysispath)-1,currentmemoryregion)) == False))
          else:
           s.add(Or(BVSubNoOverflow(findoriginexpr(koperand1,analysispath,len(analysispath)-1,currentmemoryregion),findoriginexpr(koperand2,analysispath,len(analysispath)-1,currentmemoryregion)) == False,BVSubNoUnderflow(findoriginexpr(koperand1,analysispath,len(analysispath)-1,currentmemoryregion),findoriginexpr(koperand2,analysispath,len(analysispath)-1,currentmemoryregion),True) == False)) 
          s.check()
          if str(s.check())=='sat' :
             metadata="!"+dbgcorrect(x)
             locationdata =re.findall(metadata+r" =.+", ir)[0] 
             if(x.type=="add"):
              print("发现有符号数加法溢出或反转,发生在"+re.findall(r"line: \d+", locationdata)[0].split(" ")[1]+"行，"+"第"+re.findall(r"column: \d+", locationdata)[0].split(" ")[1]+"列")
             else:
              print("发现有符号数减法溢出或反转,发生在"+re.findall(r"line: \d+", locationdata)[0].split(" ")[1]+"行，"+"第"+re.findall(r"column: \d+", locationdata)[0].split(" ")[1]+"列") 
             print(s.model())
             
         else:

          if(x.type=="add"): 

           s.add(BVAddNoOverflow(findoriginexpr(koperand1,analysispath,len(analysispath)-1,currentmemoryregion),findoriginexpr(koperand2,analysispath,len(analysispath)-1,currentmemoryregion),False) == False)
          else:
           s.add(BVSubNoUnderflow(findoriginexpr(koperand1,analysispath,len(analysispath)-1,currentmemoryregion),findoriginexpr(koperand2,analysispath,len(analysispath)-1,currentmemoryregion),False) == False) 
          s.check()
          if str(s.check())=='sat' :
             metadata="!"+dbgcorrect(x)
             locationdata =re.findall(metadata+r" =.+", ir)[0] 
             if(x.type=="add"):
              print("发现无符号数加法溢出,发生在"+re.findall(r"line: \d+", locationdata)[0].split(" ")[1]+"行，"+"第"+re.findall(r"column: \d+", locationdata)[0].split(" ")[1]+"列")
             else:
              print("发现无符号数减法反转,发生在"+re.findall(r"line: \d+", locationdata)[0].split(" ")[1]+"行，"+"第"+re.findall(r"column: \d+", locationdata)[0].split(" ")[1]+"列") 
             print(s.model())
    
             
    
            
    
                  
    if (x.type == "mul" ) :
         koperand1=x.operands[0]
         koperand2=x.operands[1]
         s = Solver()
         s.add(BVMulNoOverflow(findoriginexpr(koperand1,analysispath,len(analysispath)-1,currentmemoryregion),findoriginexpr(koperand2,analysispath,len(analysispath)-1,currentmemoryregion),True) == False)
         s.check()
         if str(s.check())=='sat' :
             metadata="!"+dbgcorrect(x)
             locationdata =re.findall(metadata+r" =.+", ir)[0] 
             # print("发现有符号数乘法溢出,发生在"+re.findall(r"line: \d+", locationdata)[0].split(" ")[1]+"行，"+"第"+re.findall(r"column: \d+", locationdata)[0].split(" ")[1]+"列")
             # print(s.model())
            
    if (x.type == "alloca"  ) :
      

      memorysymbol=typetosymbol(x.block.function.functionname+"@"+str(x.valueref).split("=")[0].strip(),x.operands[0].valueref.type) #符号化新开辟内存的临时变量
      llvmdbgdeclare(x)
      #x.block.function.symbol[x.block.function.functionname+"@"+str(x.valueref).split("=")[0].strip()]=memorysymbol
      currentmemoryregion[x.block.function.functionname+"@"+str(x.valueref).split("=")[0].strip()]=memorysymbol
      # print( currentmemoryregion)
    if (x.type == "sdiv" or x.type == "srem" or x.type == "udiv" ) :
           
           operand = x.operands[1] #分母
           
           
           expr =findoriginexpr(operand,analysispath,len(analysispath)-1,currentmemoryregion)
           
           print(expr)
          
           
           s = Solver()
           
           s.add( expr ==0)
           if(len(constraint) !=0):
            for t in constraint:        #基本块跳转附加约束
             
             s.add(t)
            s.check()
           if (str(s.check())=='sat') :
             ## print("发现除零错")
             
             
             #metadata=re.findall(r"!\d+", str(x.valueref))[0]
             metadata="!"+dbgcorrect(x)
             locationdata =re.findall(metadata+r" =.+", ir)[0] 
             
             print("发现除零错,发生在第"+re.findall(r"line: \d+", locationdata)[0].split(" ")[1]+"行，"+"第"+re.findall(r"column: \d+", locationdata)[0].split(" ")[1]+"列")
             # print("得到反例")
             print(s.model())
             # print(functionstack)
             return

    if (x.type == "getelementptr"  ) :     
           
      operands=x.operands
      size=findmemorysize(operands[0],str(operands[2].valueref.type))
      
      offset = findoriginexpr(operands[2],analysispath,len(analysispath)-1,currentmemoryregion)
      
      s = Solver()
      s.add( offset>=size)
      if(len(constraint) !=0):
        for t in constraint:        
          s.add(t)
        s.check()     
      if (str(s.check())=='sat') :
            
             
             metadata="!"+dbgcorrect(x)
             
             
             locationdata =re.findall(metadata+r" =.+", ir)[0]
             
             print("发现数组下标越界,发生在第"+re.findall(r"line: \d+", locationdata)[0].split(" ")[1]+"行，"+"第"+re.findall(r"column: \d+", locationdata)[0].split(" ")[1]+"列")
             print("得到反例")
             print(s.model()) 
    if (x.type == "load"  ) :     
       
      if (re.findall(r"null", str(x.operands[0].valueref))) :
        
             
             metadata="!"+dbgcorrect(x)
             
             locationdata =re.findall(metadata+r" =.+", ir)[0]
             # print("发现空指针解引用,发生在第"+re.findall(r"line: \d+", locationdata)[0].split(" ")[1]+"行，"+"第"+re.findall(r"column: \d+", locationdata)[0].split(" ")[1]+"列")
            
             ## print("得到反例")
             ## print(s.model()) 

    if(x.type=="store"):
     if(isGlobal(x.operands[1])==False):
      currentmemoryregion[x.block.function.functionname+"@"+str(x.operands[1].valueref).split("=")[0].strip()]=findoriginexpr(x.operands[0],analysispath,len(analysispath)-1,currentmemoryregion)
     else:
      m.global_variables[str(x.operands[1].valueref.name)]=  findoriginexpr(x.operands[0],analysispath,len(analysispath)-1,currentmemoryregion)
#验证一下phi的路径敏感
   # if (x.type == "phi") :  
        
        # koperand1 =x.operands[0]
       #  koperand2 = x.operands[1] 
        # lastblockname = analysispath[len(analysispath)-2]
        # blocks= x.block.function.blocks
        # s1 = str(koperand1.valueref)
        # s2 = str(koperand2.valueref)
      #   expr = ""
        # lastblock=""
        # for x in blocks:
         # if(x.name == lastblockname):
          #   lastblock = x
          
       #  for y in lastblock.instructions:
         
         # if(str(y.valueref) == s1):
           # expr=  findoriginexpr(koperand1,analysispath)
           # break   
         # if(str(y.valueref) == s2):
          #  expr=  findoriginexpr(koperand2,analysispath)
           # break

         ## print(expr) 
    if (x.type == "call" ) : 
      
      
       
      callee=getKFunction(x.operands[len(x.operands)-1])
      callername=x.block.function.functionname
      if(callee==None):
       if(len(str(x.valueref).split("="))>1): 

      
        callsymbol=typetosymbol(x.block.function.functionname+"@"+str(x.valueref).split("=")[0].strip(),str(x.valueref).strip().split(" ")[3]) #符号化函数的返回值
        
        x.block.function.symbol[x.block.function.functionname+"@"+str(x.valueref).split("=")[0].strip()]=callsymbol
      else:
       metadata=re.findall(r"!dbg !\d+",str(x.block.function.valueref))[0].split(" ")[1]
       print(metadata)
       metadatatobasetype(metadata)
       newfunctionstack=[]
       newconstraint=[]
       for y in constraint:
        newconstraint.append(y)
       for y in functionstack:
        newfunctionstack.append(y) 
       newfunctionstack.append(callee.functionname) 
       for y in range(len(x.operands)-1): 
       
      
        expr=findoriginexpr(x.operands[y],analysispath,len(analysispath)-1,currentmemoryregion) #抽取实参表达式
        
        newconstraint.append(expr==callee.symbol[callee.functionname+"@%"+str(y)])##被跳转的函数的形参与调用者的实参对应，通过等式约束关系
       
       
      
       SymbolicExecution(callee.blocks[0],[callee.blocks[0].name],newconstraint,newfunctionstack,callcollection,currentmemoryregion)
       
       callsymbol=typetosymbol(x.block.function.functionname+"@"+str(x.valueref).split("=")[0].strip(),str(x.valueref).strip().split(" ")[3]) #符号化函数的返回值
       x.block.function.symbol[x.block.function.functionname+"@"+str(x.valueref).split("=")[0].strip()]=callsymbol
       
       
       empty=[]
       for x in range(len(callcollection.collection)):
         empty.append([])
      
    
       empty2=[]
      
      
       for y in range(len(callcollection.collection)):
           empty[y].append(callsymbol==callcollection.collection[y][0])  
           for z in callcollection.collection[y][1]:
            empty[y].append(z)
         
       for x in empty:
         empty2.append(And(tuple(x)))
      
       constraint.append(Or(tuple(empty2))) 
       print(constraint)
  last = filter[len(filter)-1]
 
  if (last.type == "br"):
     lens=len(last.operands)
     if(lens == 1) :  #无条件跳转
      analysispath.append(findkblock(last.operands[0].valueref,kblock.function).name)
      SymbolicExecution(findkblock(last.operands[0].valueref,kblock.function),analysispath,constraint,functionstack,callcollection,currentmemoryregion)
     if(lens == 3) :  #有条件跳转 
      if(str(last.operands[0].valueref)=="i1 true"):  #条件里为True,视作无条件跳转
        
         analysispath.append(findkblock(last.operands[2].valueref,kblock.function).name)
         SymbolicExecution(findkblock(last.operands[2].valueref,kblock.function),analysispath,constraint,functionstack,callcollection,currentmemoryregion)
      else:
       condition=getKInstruction(last.operands[0])
       
       trueblock = findkblock(last.operands[2].valueref,kblock.function)  
       falseblock= findkblock(last.operands[1].valueref,kblock.function)
       truememory=currentmemoryregion.copy()
       falsememory=currentmemoryregion.copy()
       truepath = []
       falsepath = []
       for x in analysispath:
        truepath.append(x)
       for x in analysispath:
        falsepath.append(x) 
       truepath.append(trueblock.name)
       falsepath.append( falseblock.name)
       
       
       trueconstraint=[]
       for x in constraint:
        trueconstraint.append(x)
      
       falseconstraint=[]
       for x in constraint:
        falseconstraint.append(x)
       
       trueexpr = getTrueExpr(condition,analysispath,currentmemoryregion)
     
       trueconstraint.append(trueexpr) 
    
       s = Solver() #跳转之前先判断一下路径可达
       
       for t in trueconstraint:        #基本块跳转附加约束
             
         s.add(t)

       s.check()

       if (str(s.check())=='sat') :
             SymbolicExecution(trueblock,truepath,trueconstraint,functionstack,callcollection,truememory)
       falseexpr= Not(trueexpr)
     
       falseconstraint.append(falseexpr)       
        
       s = Solver() 
       
       for t in falseconstraint:       
             
         s.add(t)

       s.check()
       
       if (str(s.check())=='sat') :
         
         SymbolicExecution(falseblock,falsepath,falseconstraint,functionstack,callcollection,falsememory)

    
  if (last.type == "ret" and len(last.operands)>0):
      
      callcollection.collection.append((findoriginexpr(last.operands[0],analysispath,len(analysispath)-1,currentmemoryregion),constraint))
      



for x in kfunctions:
 set_blocknames (x)

### print(x.functionname)
      


def analysisFunction(functionname):
   
   for x in kfunctions:
     if(x.functionname==functionname):
       
       SymbolicExecution(x.blocks[0],[x.blocks[0].name],[],[x.functionname],Callcollection(),{})   



analysisFunction("main")

print(m.global_variables)








llvm.shutdown()

















