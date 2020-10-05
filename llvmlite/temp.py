from pydot import *
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


print (ir)


