MOV R3, #1
    MOV R4, #200
    MOV R5, #250
    MOV R6, #10
    MOV R2, #1          // inicializa led UMA vez so

start:
    MOV R7, #0

volta_grossa:
    MOV R1, #0

loop_externo:
    MOV R0, #0

loop_interno:
    ADD R0, R0, R3
    CMP R0, R4
    JEQ sai_interno
    JMP loop_interno

sai_interno:
    ADD R1, R1, R3
    CMP R1, R5
    JEQ sai_externo
    JMP loop_externo

sai_externo:
    ADD R7, R7, R3
    CMP R7, R6
    JEQ pisca
    JMP volta_grossa

pisca:
    OUT R2
    XOR R2, R2, R3
    JMP start           // agora start nao toca R2