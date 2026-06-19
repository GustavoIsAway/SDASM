// _start
MOV R0, #1

primeira_label:
    MOV R1, #2
    JMP segunda_label

terceira_label:
    MOV R2, #3
    JMP final

segunda_label:
    MOV R3, #4
    JMP terceira_label

final:  // Loop infinito
    JMP final