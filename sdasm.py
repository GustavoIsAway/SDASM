import sys
import os
from utils import print_err, print_warn, bits_to_hex, error_warning
from parser import LABELS, parse_line



def _is_label(line: str) -> str | None:
    stripped = line.strip()
    for comment_char in ("//",):
        if comment_char in stripped:
            stripped = stripped[:stripped.index(comment_char)]
    stripped = stripped.strip()
    if stripped and stripped.endswith(":") and not stripped[0].isdigit():
        return stripped[:-1]
    return None


def _is_instruction(line: str) -> bool:
    stripped = line.strip()
    for comment_char in ("//",):
        if comment_char in stripped:
            stripped = stripped[:stripped.index(comment_char)]
    stripped = stripped.strip()
    if not stripped:
        return False
    if stripped.endswith(":") and not stripped[0].isdigit():
        return False
    return True


def main():
    if len(sys.argv) > 3:
        print_err("Argumento extra fornecido. Uso: dasm.py <dest> <source>")
    if len(sys.argv) < 3:
        print_err("Argumentos insuficientes. Uso: dasm.py <dest> <source>")

    out_path = sys.argv[1]
    src_path = sys.argv[2]

    if out_path.startswith("-") or src_path.startswith("-"):
        print_err("Nenhum argumento aceita modificadores '-'")

    if not os.path.isfile(src_path):
        print_err(f"Arquivo de origem não encontrado: '{src_path}'")

    with open(src_path, "r") as f:
        raw_lines = f.read().upper().splitlines()

    # === PRIMEIRO PASSE: registra labels com endereço real na ROM ===
    encoded_count = 0
    for line in raw_lines:
        label = _is_label(line)
        if label is not None:
            if label not in LABELS:
                LABELS[label] = encoded_count
        elif _is_instruction(line):
            encoded_count += 1

    # === SEGUNDO PASSE: encode ===
    encoded: list[str] = []
    for line_num, line in enumerate(raw_lines, start=1):
        result = parse_line(line, line_num)
        if result is None:
            continue
        encoded.append(bits_to_hex(result))

    if not encoded:
        print_warn("Nenhuma instrução encontrada no arquivo fonte.")

    with open(out_path, "w") as f:
        for word in encoded:
            f.write(word + "\n")

    status = "Assembler montou com avisos" if error_warning else "Montagem perfeita"
    print(f"{status}: {len(encoded)} {'instrução' if len(encoded) == 1 else 'instruções'} -> '{out_path}'")


if __name__ == "__main__":
    main()