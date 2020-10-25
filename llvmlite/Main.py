from llvmlite import binding as llvm
from z3 import * 
from KInstruction import *
from KModule import *
from KFunction import * 
from KBlock import * 
from graphviz import *
from KOperand import *
from pydot import *
import re
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()
import os

os.system("cd /libx32/llvmlite/ && clang-8  -emit-llvm divide3.c -g -S -o divide3.ll -Xclang -disable-O0-optnone && opt-8 divide3.ll   -gvn  -S -o output.ll")
#os.system("cd /libx32/llvmlite/ && clang-8  -emit-llvm test2.cpp -g -S -o test2.ll -Xclang -disable-O0-optnone && opt-8 test2.ll -mem2reg -S -o test2.ll")
ir = ""

#clang-8  -emit-llvm divide3.c -S -o divide3.ll -Xclang -disable-O0-optnone && opt-8 divide3.ll -mem2reg -S -o output.ll

with open("/libx32/llvmlite/output.ll", "r") as f:  
    ir = f.read() 




    


def printlist (list):
 for x in list: 
  print (x)



def findkblock (valueref,kfunction) :
  
  for x in kfunction.blocks:
    if(str(valueref) == str(x.valueref)):
      return x
   


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

            #print (("label "+re.findall(r"%\d+", each_attr_val)[0],re.findall(r"label %\d+", each_attr_val)))
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
     if(len(re.findall(r"i\d+",str(x)))>0):
      #dict[str(x).split(" ")[1]] =BitVec(str(x).split(" ")[1],int(re.findall(r"i\d+",str(x))[0][1:]))
      dict[str(x).split(" ")[1]] =Int(str(x).split(" ")[1])
   return (dict)   

def indexOf (list,x):
  index = -1
  for n in range(len(list)):
   if(list[n]==x):
      index =n
  return index    

def findmemorysize(koperand):  #溯源至内存时，提供内存的大小信息
   p = re.compile(r'[[](.*?)[]]', re.S)

   size=int(re.findall(p, str(koperand.valueref)) [0][0]   )

   return size

def findoriginexpr (koperand,analysispath,loopcounter):   #遇到循环时的回溯，要添加一个计数变量，默认仍是分析路径长度-2   
  
  if(isArgument(koperand) ):
    
    return koperand.instruction.block.function.symbol[str(koperand.valueref).split(" ")[1]]
  
  if(isConstant (koperand)):

    return int(str(koperand.valueref).split(" ")[1])

  else :

     instruction = getKInstruction(koperand)

     currentblock=instruction.block.name
     
     blocknumber = -1
     for x in range (len(analysispath)-1):
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
            
          
         return  findoriginexpr(operands[index],analysispath,loopcounter-1)

         #print(operands[index].valueref)
           



     if(len(operands) == 2):       #二元运算表达式
       koperand1 =operands[0]
       koperand2 = operands[1]
 
       if(opcode =="add"):
         return (findoriginexpr(koperand1,analysispath,loopcounter) + findoriginexpr(koperand2,analysispath,loopcounter)) 
       if(opcode =="sub"):
         return (findoriginexpr(koperand1,analysispath,loopcounter) - findoriginexpr(koperand2,analysispath,loopcounter))
       if(opcode =="mul"):
         return (findoriginexpr(koperand1,analysispath,loopcounter) * findoriginexpr(koperand2,analysispath,loopcounter))
       if(opcode =="shl"):
         return (findoriginexpr(koperand1,analysispath,loopcounter) * findoriginexpr(koperand2,analysispath,loopcounter)*2)  
       if(opcode =="sdiv"):
         return (findoriginexpr(koperand1,analysispath,loopcounter) / findoriginexpr(koperand2,analysispath,loopcounter))
        
           
     if(len(operands) == 1):       #一元运算表达式
       koperand1 =operands[0]
      
 
       if(opcode =="load" or opcode =="sext" ):
         return findoriginexpr(koperand1,analysispath,loopcounter) 
      

     if(len(operands) ==3):    
    
      koperand1 =operands[0]
      koperand2 =operands[1]
      koperand3 =operands[2]
      if(opcode == "getelementptr") :  #getelementptr 包含三要素 内存地址 基址 偏移量   
          
         return findoriginexpr(koperand3,analysispath,loopcounter) 



mref=llvm.parse_assembly(ir)


globalvariables = getListfromIter(mref.global_variables)



functions=getListfromIter(mref.functions)




m = KModule(globalvariables,functions)


kfunctions=[]

for x in functions:
  kfunctions.append(KFunction(m,x.name,getListfromIter(x.blocks),getListfromIter(x.arguments),x,getArgumentSymbolMapfromIter(x.arguments)))


m.functions=kfunctions




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



def IntraproceduralAnalysis(kblock,analysispath,constraint):   #过程内分析
  
  filter=[]

  for x in kblock.instructions:

    filter.append(x)

      

  for x in filter :
    #if (x.type == "add" ) :
     #    koperand1=x.operands[0]
      #   koperand2=x.operands[1]
      #   s = Solver()
      #   s.add(BVAddNoOverflow(findoriginexpr(koperand1,analysispath),findoriginexpr(koperand2,analysispath),True) == False)
      #   s.check()
        # if str(s.check())=='sat' :
       #      print("发现有符号数加法溢出")
         #    print(s.model())
         #    print(x.valueref)
    #if (x.type == "sub" ) :
       #  koperand1=x.operands[0]
        # koperand2=x.operands[1]
       #  s = Solver()
        # s.add(BVSubNoOverflow(findoriginexpr(koperand1,analysispath),findoriginexpr(koperand2,analysispath)) == False)
        # s.check()
        # if str(s.check())=='sat' :
           #  print("发现有符号数减法溢出")
           #  print(s.model())
            # print(x.valueref)         
    #if (x.type == "mul" ) :
      #   koperand1=x.operands[0]
       #  koperand2=x.operands[1]
       #  s = Solver()
        # s.add(BVMulNoOverflow(findoriginexpr(koperand1,analysispath),findoriginexpr(koperand2,analysispath),True) == False)
        # s.check()
        # if str(s.check())=='sat' :
         #    print("发现有符号数乘法溢出")
           #  print(s.model())
            # print(x.valueref) 

    if (x.type == "sdiv" or x.type == "srem" ) :
           
           operand = x.operands[1] #分母
      
         
           expr =findoriginexpr(operand,analysispath,len(analysispath)-1)
           
           
           s = Solver()
           print(expr)
           s.add( expr ==0)
           if(len(constraint) !=0):
            for t in constraint:        #基本块跳转附加约束
             
             s.add(t)
            s.check()
           if (str(s.check())=='sat') :
             print("发现除零错")
            
             metadata=re.findall(r"!\d+", str(x.valueref))[0]
           
             locationdata =re.findall(metadata+r" =.+", ir)[0] 
             print(locationdata)
             print("发生在第"+re.findall(r"line: \d+", locationdata)[0].split(" ")[1]+"行，"+"第"+re.findall(r"column: \d+", locationdata)[0].split(" ")[1]+"列")
             print("得到反例")
             print(s.model())

    if (x.type == "getelementptr"  ) :     
           
      operands=x.operands
      size=findmemorysize(operands[0])
      offset = findoriginexpr(operands[2],analysispath,len(analysispath)-1)
      s = Solver()
      s.add( offset>=size)
      if(len(constraint) !=0):
        for t in constraint:        
          s.add(t)
        s.check()     
      if (str(s.check())=='sat') :
             print("发现数组下标越界")
            
             metadata=re.findall(r"!\d+", str(x.valueref))[0]
             locationdata =re.findall(metadata+r" =.+", ir)[0]
             print("发生在第"+re.findall(r"line: \d+", locationdata)[0].split(" ")[1]+"行，"+"第"+re.findall(r"column: \d+", locationdata)[0].split(" ")[1]+"列")
             #print("得到反例")
             #print(s.model()) 
    if (x.type == "load"  ) :     
       
      if (re.findall(r"null", str(x.operands[0].valueref))) :
             print("发现空指针解引用")
             
             metadata=re.findall(r"!\d+", str(x.valueref))[0]
             locationdata =re.findall(metadata+r" =.+", ir)[0]
             print("发生在第"+re.findall(r"line: \d+", locationdata)[0].split(" ")[1]+"行，"+"第"+re.findall(r"column: \d+", locationdata)[0].split(" ")[1]+"列")
            
             #print("得到反例")
             #print(s.model()) 
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

         #print(expr) 
      

  last = filter[len(filter)-1]
 
  if (last.type == "br"):
     lens=len(last.operands)
     if(lens == 1) :  #无条件跳转
      analysispath.append(findkblock(last.operands[0].valueref,kblock.function).name)
      IntraproceduralAnalysis(findkblock(last.operands[0].valueref,kblock.function),analysispath,constraint)
     if(lens == 3) :  #有条件跳转 
      condition=getKInstruction(last.operands[0])
      trueblock = findkblock(last.operands[2].valueref,kblock.function)  
      falseblock= findkblock(last.operands[1].valueref,kblock.function)
  
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


      if(len(re.findall(r"slt", str(condition.valueref)))!=0):  #有符号数小于 signed less than

       trueexpr = findoriginexpr(condition.operands[0],analysispath,len(analysispath)-1) - findoriginexpr(condition.operands[1],analysispath,len(analysispath)-1) < 0
       trueconstraint.append(trueexpr) 
       
       s = Solver() #跳转之前先判断一下路径可达
       
       for t in trueconstraint:        #基本块跳转附加约束
             
        s.add(t)

       s.check()

     
       if (str(s.check())=='sat') :


  
              IntraproceduralAnalysis(trueblock,truepath,trueconstraint)
 



       falseexpr= findoriginexpr(condition.operands[0],analysispath,len(analysispath)-1) - findoriginexpr(condition.operands[1],analysispath,len(analysispath)-1) >= 0 
       falseconstraint.append(falseexpr)       
       print(findoriginexpr(condition.operands[0],analysispath,len(analysispath)-1))
       s = Solver() 
       print(falseconstraint)
       for t in falseconstraint:       
             
        s.add(t)

       s.check()

       if (str(s.check())=='sat') :
             
             print("")
             IntraproceduralAnalysis(falseblock,falsepath,falseconstraint)

      if(len(re.findall(r"sgt", str(condition.valueref)))!=0):  #有符号数大于 signed greater than

       trueexpr = findoriginexpr(condition.operands[0],analysispath,len(analysispath)-1) - findoriginexpr(condition.operands[1],analysispath,len(analysispath)-1) > 0
       trueconstraint.append(trueexpr) 
       
       s = Solver() 
       
       for t in trueconstraint:       
             
        s.add(t)

       s.check()

     
       if (str(s.check())=='sat') :


  
              IntraproceduralAnalysis(trueblock,truepath,trueconstraint)
 



       falseexpr= findoriginexpr(condition.operands[0],analysispath,len(analysispath)-1) - findoriginexpr(condition.operands[1],analysispath,len(analysispath)-1) <= 0 
       falseconstraint.append(falseexpr)       
       print(findoriginexpr(condition.operands[0],analysispath,len(analysispath)-1))
       s = Solver() 
       print(falseconstraint)
       for t in falseconstraint:       
             
        s.add(t)

       s.check()

       if (str(s.check())=='sat') :
             
             print("")
             IntraproceduralAnalysis(falseblock,falsepath,falseconstraint)
 
      if(len(re.findall(r"eq", str(condition.valueref)))!=0):  #等于 
       
       print("okw")
       trueexpr = findoriginexpr(condition.operands[0],analysispath,len(analysispath)-1) - findoriginexpr(condition.operands[1],analysispath,len(analysispath)-1) < 0
       trueconstraint.append(trueexpr) 
       
       s = Solver()
       
       for t in trueconstraint:       
             
        s.add(t)

       s.check()

     
       if (str(s.check())=='sat') :


  
              IntraproceduralAnalysis(trueblock,truepath,trueconstraint)
 



       falseexpr= findoriginexpr(condition.operands[0],analysispath,len(analysispath)-1) - findoriginexpr(condition.operands[1],analysispath,len(analysispath)-1) >= 0 
       falseconstraint.append(falseexpr)       
       print(findoriginexpr(condition.operands[0],analysispath,len(analysispath)-1))
       s = Solver() 
       print(falseconstraint)
       for t in falseconstraint:       
             
        s.add(t)

       s.check()

       if (str(s.check())=='sat') :
             
             print("")
             IntraproceduralAnalysis(falseblock,falsepath,falseconstraint)

  
  if (last.type == "ret"):
     
     print(analysispath)  



for x in kfunctions:
 set_blocknames (x)




#for x in kfunctions:
 #if(len(x.blocks) >0):  

  
  #IntraproceduralAnalysis(x.blocks[0],[x.blocks[0].name],[])
#print(re.findall(r"\d+ x", str(kinstructions[0].valueref))[0].split(" ")[0])


#print(kfunctions[4].blocks[0].instructions[6].operands[0].valueref)

      
IntraproceduralAnalysis(kfunctions[5].blocks[0],[kfunctions[5].blocks[0].name],[])     
       



llvm.shutdown()

















