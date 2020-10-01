
 
class KInstruction:
   block=""
   
   type=""
   operands=[]
   valueref = ""
 
   def __init__(self,block, type, operands,valueref):
      self.block=block
     
      self.type=type
      self.operands=operands
      self.valueref =  valueref
      