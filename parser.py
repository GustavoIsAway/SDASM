from utils import reg_number, parse_immediate, parse_mem_ref, print_err, clean_token

# Hash set de registradores
REGISTERS = {f"R{i}" for i in range(8)}


# Limpa string do registrador, tirando vírgulas e espaços extras. Se correta a sintaxe, devolve apenas o número do registrador como inteiro
def clean_reg(token: str) -> int:
    return reg_number(clean_token(token))


# === OPERADORES NULÁRIOS ===

def encode_NOP(tokens: list[str], ln: int) -> int:
    if len(tokens) != 0:
        print_err(f"NOP espera 0 operandos, recebeu {len(tokens)}: {tokens}")
    return 0x0000

def encode_HALT(tokens: list[str], ln: int) -> int:
    if len(tokens) != 0:
        print_err(f"HALT espera 0 operandos, recebeu {len(tokens)}: {tokens}")
    return 0xFFFF


# === OPERADORES BINÁRIOS ===
# MOV  -  dois formatos
# MOV Rd, Rm
# MOV Rd, #Im8
# Rd sempre recebe
def encode_MOV(tokens: list[str], ln: int) -> int:
    if len(tokens) != 2:
        print_err(f"MOV espera 2 operandos, recebeu {len(tokens)}: {tokens}")

    rd_str = clean_token(tokens[0])
    src_str = clean_token(tokens[1])

    rd = clean_reg(rd_str)

    if src_str.startswith("#"):
        # MOV Rd, #Im8
        im = parse_immediate(src_str, 8)
        enc = (0b0001 << 12) | (1 << 11) | (rd << 8) | im
    else:
        # MOV Rd, Rm
        rm = clean_reg(src_str)
        enc = (0b0001 << 12) | (0 << 11) | (rd << 8) | (rm << 5)

    return enc


# STR  -  dois formatos
# STR [Rm], Rn
# STR [Rm], #Im (8 bits de imediato)
# Rm sempre recebe

def encode_STR(tokens: list[str], ln: int) -> int:
    if len(tokens) != 2:
        print_err(f"STR espera 2 operandos, recebeu {len(tokens)}: {tokens}")

    mem_str = clean_token(tokens[0])
    src_str = clean_token(tokens[1])

    rm = clean_reg(parse_mem_ref(mem_str))

    if src_str.startswith("#"):
        # STR [Rm], #Im8
        im = parse_immediate(src_str, 8)
        im_hi = (im >> 5) & 0b111
        im_lo = im & 0b11111
        enc = (0b0010 << 12) | (1 << 11) | (im_hi << 8) | (rm << 5) | (im_lo)
    else:
        # STR [Rm], Rn
        rn = clean_reg(src_str)
        enc = (0b0010 << 12) | (0 << 11) | (rm << 5) | (rn << 2)

    return enc



# LDR Rd, [Rm]
def encode_LDR(tokens: list[str], ln: int) -> int:
    if len(tokens) != 2:
        print_err(f"LDR espera 2 operandos, recebeu {len(tokens)}: {tokens}")

    rd = clean_reg(clean_token(tokens[0]))
    rm = clean_reg(parse_mem_ref(clean_token(tokens[1])))

    enc = (0b0011 << 12) | (rd << 8) | (rm << 5)
    return enc



_ULA_OPCODES = {
    "ADD": 0b0100,
    "SUB": 0b0101,
    "MUL": 0b0110,
    "AND": 0b0111,
    "ORR": 0b1000,
    "XOR": 0b1010,
}


def _encode_ula_ternary(mnemonic: str, tokens: list[str], ln: int) -> int:
    if len(tokens) != 3:
        print_err(f"{mnemonic} espera 3 operandos, recebeu {len(tokens)}: {tokens}")
    rd = clean_reg(clean_token(tokens[0]))
    rm = clean_reg(clean_token(tokens[1]))
    rn = clean_reg(clean_token(tokens[2]))
    opcode = _ULA_OPCODES[mnemonic]
    return (opcode << 12) | (rd << 8) | (rm << 5) | (rn << 2)



# Pra cada encode, envia linha para debug
def encode_ADD(tokens, ln): return _encode_ula_ternary("ADD", tokens, ln)
def encode_SUB(tokens, ln): return _encode_ula_ternary("SUB", tokens, ln)
def encode_MUL(tokens, ln): return _encode_ula_ternary("MUL", tokens, ln)
def encode_AND(tokens, ln): return _encode_ula_ternary("AND", tokens, ln)
def encode_ORR(tokens, ln): return _encode_ula_ternary("ORR", tokens, ln)
def encode_XOR(tokens, ln): return _encode_ula_ternary("XOR", tokens, ln)



def encode_NOT(tokens: list[str], ln: int) -> int:
    if len(tokens) != 2:
        print_err(f"NOT espera 2 operandos, recebeu {len(tokens)}: {tokens}")
    rd = clean_reg(clean_token(tokens[0]))
    rm = clean_reg(clean_token(tokens[1]))
    return (0b1001 << 12) | (rd << 8) | (rm << 5)


# Dicionário de dispatch (atualizar ela pra segunda metade das instruções, caso o Thiago queira)

ENCODERS = {    # Armazena ponteiros das funções, sem executá-las
    "NOP":  encode_NOP,
    "HALT": encode_HALT,
    "MOV":  encode_MOV,
    "STR":  encode_STR,
    "LDR":  encode_LDR,
    "ADD":  encode_ADD,
    "SUB":  encode_SUB,
    "MUL":  encode_MUL,
    "AND":  encode_AND,
    "ORR":  encode_ORR,
    "NOT":  encode_NOT,
    "XOR":  encode_XOR,
}


def parse_line(line: str, line_num: int) -> int | None:

    # Remove comentários na linha
    for comment_char in ("//"):
        if comment_char in line:
            line = line[:line.index(comment_char)]

    line = line.strip()
    if not line:
        return None

    tokens = line.split()
    mnemonic = tokens[0]
    operands = tokens[1:]  # mantém vírgulas; cada encoder chama clean_token(), o que remove as vírgulas

    if mnemonic not in ENCODERS:
        print_err(f"Ln {line_num} - Mnemônico desconhecido: '{mnemonic}'")

    return ENCODERS[mnemonic](operands, line_num)   # Executa funções a partir dos ponteiros