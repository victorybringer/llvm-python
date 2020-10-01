
 
class KFunction():
   
   valueref = ""

   functionname =""
   module =""

   blocks=[]
   arguments=[]
   functionconstraint=[]

   symbol=[]
 
   def __init__(self, m,n,b,a,valueref,symbol):

      self.module =m  
      self.functionname = n
      self.blocks=b
      self. arguments =a 
      self.valueref =  valueref
      self.symbol =symbol
 