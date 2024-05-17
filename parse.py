##
#   @file parse.py
#
#   @brief Toto je implementace alanyzatoru kódu v IPPcode24
#
#   @autor Jakub Fukala (xfukal01)
#
import re
import sys
import xml.etree.ElementTree as Et
import xml.dom.minidom as minidom

# Definice regularnich vyrazu pro lexikalni analyzator
var = r"^(GF|LF|TF)@[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*$"
symb = r"^(GF|LF|TF)@[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*$|bool@true|bool@false|int@[-+]?[0-9]+$|int@[-+]?0x[0-9a-fA-F]+$|int@[-+]?0o[0-7]+$|string@[^#]*$|nil@nil"
label = r"^[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*$"
type_var = r"^(int|string|bool|nil)$"

# Slovník instrukcí a jejich parametrů
# Klíč je název instrukce, hodnota je pole parametrů
opcode_dict = {
    "MOVE": ["var", "symb"],
    "CREATEFRAME": [],
    "PUSHFRAME": [],
    "POPFRAME": [],
    "DEFVAR": ["var"],
    "CALL": ["label"],
    "RETURN": [],
    "PUSH": ["symb"],
    "POP": ["type"],
    "PUSHS": ["symb"],
    "POPS": ["var"],
    "ADD": ["var", "symb", "symb"],
    "SUB": ["var", "symb", "symb"],
    "MUL": ["var", "symb", "symb"],
    "IDIV": ["var", "symb", "symb"],
    "LT": ["var", "symb", "symb"],
    "GT": ["var", "symb", "symb"],
    "EQ": ["var", "symb", "symb"],
    "AND": ["var", "symb", "symb"],
    "OR": ["var", "symb", "symb"],
    "NOT": ["var", "symb"],
    "INT2CHAR": ["var", "symb"],
    "STRI2INT": ["var", "symb", "symb"],
    "READ": ["var", "type"],
    "WRITE": ["symb"],
    "CONCAT": ["var", "symb", "symb"],
    "STRLEN": ["var", "symb"],
    "GETCHAR": ["var", "symb", "symb"],
    "SETCHAR": ["var", "symb", "symb"],
    "TYPE": ["var", "symb"],
    "LABEL": ["label"],
    "JUMP": ["label"],
    "JUMPIFEQ": ["label", "symb", "symb"],
    "JUMPIFNEQ": ["label", "symb", "symb"],
    "EXIT": ["symb"],
    "DPRINT": ["symb"],
    "BREAK": []
}


def call_help():
    print("Nápověda:")
    print("Použití Např: python3.10 parser.py < [Vstupní soubor] > [Výstupní soubor]")
    print("  --help          Vypíše nápovědu")


# Funkce pro sestavení XML stromu
def line_to_tree(elem):

    rough_string = Et.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    # Odstranění hlavičky XML a odsazení
    return reparsed.toprettyxml(indent="  ").split('\n', 1)[1]


# Funkce pro přidání instrukce do XML a zároveň kontrolu její existence a přidání parametrů
def parse(root, intruction_order, opcode, *args):
    # Kontrola existence instrukce
    if opcode not in opcode_dict:
        sys.exit(22)

    # Přidání instrukce do XML
    element = Et.SubElement(root, "instruction")
    element.set("order", str(intruction_order))
    element.set("opcode", opcode)

    # Přidání parametrů
    num_of_args = len(opcode_dict.get(opcode))
    # Kontrola počtu parametrů
    if len(args) != num_of_args:
        sys.exit(23)
    for i in range(num_of_args):
        arg_type = opcode_dict.get(opcode)[i]

        # Je to hodnota nebo proměnná?
        if arg_type == "symb":
            # Kontrola existence parametru
            if not args[i]:
                sys.exit(23)
            if re.fullmatch(symb, args[i]):
                # Pokud je to proměnná, přidáme ji jako proměnnou
                if re.fullmatch(var, args[i]):
                    Et.SubElement(element, "arg" + str(i + 1), type="var").text = args[i]
                elif re.fullmatch(type_var, args[i].split("@")[0]):
                    # Pokud je to hodnota, zjistíme typ a přidáme ji jako hodnotu
                    arg_text = args[i].split("@", 1)
                    # Pokud se v řetězci vyskytuje escapovací sekvence tak zkontrolujeme, zda je správně zapsána
                    if arg_text[0] == "string":
                        # Pokud se v řetězci vyskytuje neplatné escapovací sekvence, skončíme s chybou
                        if re.search(r'\\(?![0-9]{3})', arg_text[1]):
                            sys.exit(23)
                    Et.SubElement(element, "arg" + str(i + 1), type=arg_text[0]).text = arg_text[1]
                else:
                    # Pokud parametr není správný, skončíme s chybou
                    sys.exit(23)
            else:
                # Pokud parametr není správný, skončíme s chybou
                sys.exit(23)
        elif arg_type == "var":
            # Kontrola existence parametru
            if not args[i]:
                sys.exit(23)
            # Kontrola správnosti parametru
            if re.fullmatch(var, args[i]):
                Et.SubElement(element, "arg" + str(i + 1), type="var").text = args[i]
            else:
                # Pokud parametr není správný, skončíme s chybou
                sys.exit(23)
        elif arg_type == "label":
            # Kontrola existence parametru
            if not args[i]:
                sys.exit(23)
            # Kontrola správnosti parametru
            if re.fullmatch(label, args[i]):
                Et.SubElement(element, "arg" + str(i + 1), type="label").text = args[i]
            else:
                # Pokud parametr není správný, skončíme s chybou
                sys.exit(23)
        elif arg_type == "type":
            # Kontrola existence parametru
            if not args[i]:
                sys.exit(23)
            # Kontrola správnosti parametru
            if re.fullmatch(type_var, args[i]):
                Et.SubElement(element, "arg" + str(i + 1), type="type").text = args[i]
            else:
                # Pokud parametr není správný, skončíme s chybou
                sys.exit(23)
        else:
            # Pokud parametr není správný, skončíme s chybou
            sys.exit(23)


def main():
    # Hlavička XML
    xml_header = '<?xml version="1.0" encoding="UTF-8" ?>\n'
    # Vytvoření kořenového elementu
    root = Et.Element("program")
    root.set("language", "IPPcode24")

    # Proměnná pro kontrolu hlavičky
    header = False
    # Pořadí instrukce
    intruction_order = 0
    # Načítání vstupu
    for line in sys.stdin:

        # Přeskočení komentářů a prázdných řádků
        if line.startswith("#") or line.strip() == "":
            continue
        # Rozdělení řádku na část před komentářem a část za komentářem
        parts = line.split("#")
        # Získání první části (před komentářem) a odstranění bílých znaků
        clean_line = parts[0].strip()
        # Na prvním řádku vstupu se očekává hlavička
        if not header:
            # Filtrace komentářů na řádku
            if clean_line == ".IPPcode24":
                header = True
                continue
            else:
                # Pokud hlavička chybí nebo nemá správný formát, skončíme s chybou
                sys.exit(21)

        # Kontrola duplicitní hlavičky
        if header and clean_line == ".IPPcode24":
            exit(23)

        # Zvýšení pořadí instrukce
        intruction_order += 1
        # Získání názvu instrukce
        intruction = clean_line.split()[0].upper()
        parse(root, intruction_order, intruction, *clean_line.split()[1:])

    if not header:
        sys.exit(21)
    # Výpis XML stromu na standardní výstup
    sys.stdout.write(xml_header + line_to_tree(root))


if __name__ == "__main__":
    if "--help" in sys.argv:
        call_help()
        sys.exit(0)
    main()
# Konec souboru parse.py (EOF)
