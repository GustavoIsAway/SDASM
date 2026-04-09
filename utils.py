import sys

error_warning = 0

def print_err(text: str):
    print("ERR:", text)
    sys.exit(1)

def print_warn(text: str):
    global error_warning
    print("WARN:", text)
    error_warning = 1

def reg_number(reg: str) -> int:
    # R0..R7 -> 0..7
    reg = clean_token(reg)
    if not reg.startswith("R") or not reg[1:].isdigit():
        print_err(f"Registrador inválido: '{reg}'")
    n = int(reg[1:])
    if n < 0 or n > 7:
        print_err(f"Registrador fora do range (R0-R7): '{reg}'")
    return n

def clean_token(token: str) -> str:
    return token.strip().strip(",")

def parse_immediate(token: str, bits: int) -> int:
    value = 0
    token = clean_token(token)
    if not token.startswith("#"):
        print_err(f"Imediato esperado (prefixo '#'): '{token}'")
    raw = token[1:]

    try:
        value = int(raw, 0)
    except ValueError:
        print_err(f"Valor imediato inválido: '{token}'")
    max_val = (1 << bits) - 1

    if value < 0 or value > max_val:
        print_err(f"Imediato {value} não cabe em {bits} bits (0..{max_val})")
    return value

def parse_mem_ref(token: str) -> str:
    # [Rm] -> 'Rm'
    token = clean_token(token)
    if not (token.startswith("[") and token.endswith("]")):
        print_err(f"Referência de memória inválida (esperado [Rn]): '{token}'")
    return token[1:-1]

def bits_to_hex(value: int, width: int = 16) -> str:
    mask = (1 << width) - 1
    return f"0x{(value & mask):04X}"