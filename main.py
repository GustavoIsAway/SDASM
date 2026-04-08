import sys
import os

# Instruções
instructions = {"ADD", "MUL", "SUB", "MOV", "LDR", "STR", "NOP", "HALT", "AND", "ORR", "NOT", "XOR"}



def print_err(text: str):
    print("ERR:", str)
    exit()

# Tratando argumentos
if not sys.argv[1] or not sys.argv[2]:
    print_err("Faltam argumentos a se fornecer.")

arg1 = sys.argv[1]
arg2 = sys.argv[2]
if sys.argv[3]:
    print_err("Argumento extra fornecido.")

if not os.path.isfile(arg2):
    print_err("Arquivo de origem fornecido não existe")



# Tratando modificadores do tipo -. (TODO)
if arg1[0] == '-' or arg2 == '-':
    print_err("Nenhum argumento aceita modificadores '-'.")

