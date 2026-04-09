# SDASM
O SDASM é um assembler simples para um processador de arquitetura base RISC mínimo, a ser desenvolvido nas aulas de Sistemas Digitais na UFC de Quixadá para o semestre 2026.1.

## Requisitos
É necessário, no mínimo, Python 3.10 para executar código via interpretador. Praticamente todas as distros Linux possuem Python nativamente, cabendo apenas ao usuário de Windows instalá-lo.


## Tabela de Instruções
O SDASM gera arquivo .hex de instruções compatíveis com a tabela a seguir:

| Instrução           | Operação        | Tipo  | 15 | 14 | 13 | 12 | 11 | 10  | 9   | 8   | 7   | 6   | 5   | 4   | 3   | 2   | 1   | 0   |
|---------------------|----------------|-------|----|----|----|----|----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| NOP                | nop            | NOP   | 0  | 0  | 0  | 0  | 0  | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   |
| HALT               | halt           | HALT  | 1  | 1  | 1  | 1  | 1  | 1   | 1   | 1   | 1   | 1   | 1   | 1   | 1   | 1   | 1   | 1   |
| MOV Rd, Rm         | Rd = Rm        | MOV   | 0  | 0  | 0  | 1  | 0  | Rd₂ | Rd₁ | Rd₀ | Rm₂ | Rm₁ | Rm₀ | -   | -   | -   | -   | -   |
| MOV Rd, #Im        | Rd = #Im       | MOV   | 0  | 0  | 0  | 1  | 1  | Rd₂ | Rd₁ | Rd₀ | Im₇ | Im₆ | Im₅ | Im₄ | Im₃ | Im₂ | Im₁ | Im₀ |
| STR [Rm], Rn       | [Rm] = Rn      | STORE | 0  | 0  | 1  | 0  | 0  | -   | -   | -   | Rm₂ | Rm₁ | Rm₀ | Rn₂ | Rn₁ | Rn₀ | -   | -   |
| STR [Rm], #Im      | [Rm] = #Im     | STORE | 0  | 0  | 1  | 0  | 1  | Im₇ | Im₆ | Im₅ | Rm₂ | Rm₁ | Rm₀ | Im₄ | Im₃ | Im₂ | Im₁ | Im₀ |
| LDR Rd, [Rm]       | Rd = [Rm]      | LOAD  | 0  | 0  | 1  | 1  | -  | Rd₂ | Rd₁ | Rd₀ | Rm₂ | Rm₁ | Rm₀ | -   | -   | -   | -   | -   |
| ADD Rd, Rm, Rn     | Rd = Rm + Rn   | ULA   | 0  | 1  | 0  | 0  | -  | Rd₂ | Rd₁ | Rd₀ | Rm₂ | Rm₁ | Rm₀ | Rn₂ | Rn₁ | Rn₀ | -   | -   |
| SUB Rd, Rm, Rn     | Rd = Rm - Rn   | ULA   | 0  | 1  | 0  | 1  | -  | Rd₂ | Rd₁ | Rd₀ | Rm₂ | Rm₁ | Rm₀ | Rn₂ | Rn₁ | Rn₀ | -   | -   |
| MUL Rd, Rm, Rn     | Rd = Rm * Rn   | ULA   | 0  | 1  | 1  | 0  | -  | Rd₂ | Rd₁ | Rd₀ | Rm₂ | Rm₁ | Rm₀ | Rn₂ | Rn₁ | Rn₀ | -   | -   |
| AND Rd, Rm, Rn     | Rd = Rm and Rn | ULA   | 0  | 1  | 1  | 1  | -  | Rd₂ | Rd₁ | Rd₀ | Rm₂ | Rm₁ | Rm₀ | Rn₂ | Rn₁ | Rn₀ | -   | -   |
| ORR Rd, Rm, Rn     | Rd = Rm or Rn  | ULA   | 1  | 0  | 0  | 0  | -  | Rd₂ | Rd₁ | Rd₀ | Rm₂ | Rm₁ | Rm₀ | Rn₂ | Rn₁ | Rn₀ | -   | -   |
| NOT Rd, Rm         | Rd = ¬Rm       | ULA   | 1  | 0  | 0  | 1  | -  | Rd₂ | Rd₁ | Rd₀ | Rm₂ | Rm₁ | Rm₀ | -   | -   | -   | -   | -   |
| XOR Rd, Rm, Rn     | Rd = Rm xor Rn | ULA   | 1  | 0  | 1  | 0  | -  | Rd₂ | Rd₁ | Rd₀ | Rm₂ | Rm₁ | Rm₀ | Rn₂ | Rn₁ | Rn₀ | -   | -   |


## Uso
Para usá-lo simplesmente chame o comando com essa estrutura:

    $ python3 -m sdasm.py (destino).hex (fonte).asm

em que fonte é o seu código .asm e o destino é o arquivo final. Convém que o destino sempre tenha extensão .hex.

**Exemplo**

    $ python3 -m sdasm.py main.hex main.asm
    

Isso gera hex code em ASCII puro, que pode ser diretamente colocado em projeto desenvolvido via Verilog ou Verilog + Vivado.