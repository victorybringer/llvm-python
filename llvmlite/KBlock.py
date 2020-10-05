
 
class KBlock:
     
   function=""
   name=""
   instructions=[]
   blockconstraint=[]
   valueref=""
 
   def __init__(self, f, i,valueref):
      self. function=f
      self. instructions=i
    
      self.valueref =  valueref
     