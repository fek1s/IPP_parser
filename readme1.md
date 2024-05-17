## Implementační dokumentace k 1. úloze do IPP 2023/2024
 - **Jméno a příjmení:** Jakub Fukala 
 - **Login:** xfukal01

### Popis skriptu
Toto je soubor popisující implementaci skriptu `parse.py`, který slouží jako jako
analyzátor kódu v IPPcode24. Skript čte kód ze standardního vstupu, kontroluje 
lexikální a syntaktickou správnost a XML reprezetaci programu na standardní výstup.

### Způsob řešení
Skript používá jednoduchý přístup k reprezentaci instrukcí a jejich parametrů 
pomocí slovníku `opcode_dict`, kde klíčem je název instrukce a hodnotou je list parametrů, což umožňuje snadné rozpoznání správných 
typů a počtů parametrů pro každou instrukci.

- **Lexikální analýza:** Skript po řádcích provadí lexikální analýzu kódu, kdy kontroluje správnost instrukcí a počty parametrů.
- **Syntaktická analýza:** Po lexikální analýze následuje syntaktická analýza, kdy se kontroluje správnost parametrů a jejich typ a využitím slovníku.
- **Výstup:** Po úspěšné syntaktické analýze se vytváří XML reprezentace kódu, 
která je po odřadkování a přidání odsazení pomocí funkce `line_to_tree` následně vypsána jako strom na standardní výstup.
- **Při nalezení** chyby se skript ukončí s odpovídajícím návratovým kódem.

