from comuniitaliani import Comuni

def main():
    comuni = Comuni()

    # Test 1: Cerca un comune per nome
    print("---- TEST 1: Cerca un Comune per Nome ----")
    try:
        nome_comune = "Agliè"
        info = comuni.cerca_comune(nome_comune)
        print(f"Informazioni sul comune '{nome_comune}':")
        for key, value in info.items():
            print(f"  {key.capitalize()}: {value}")
    except Exception as e:
        print(f"Errore nel cercare il comune '{nome_comune}': {e}")
    print()

    # Test 2: Ottieni comuni di una provincia
    print("---- TEST 2: Comuni di una Provincia ----")
    try:
        sigla_provincia = "TO"
        provincia_comuni = comuni.comuni_per_provincia(sigla_provincia)
        if provincia_comuni:
            print(f"Primi 5 comuni della provincia '{sigla_provincia}':")
            for idx, comune in enumerate(provincia_comuni[:5], start=1):
                print(f"  {idx}. {comune['nome']} (Codice Catastale: {comune['codice_catastale']})")
        else:
            print(f"Nessun comune trovato nella provincia '{sigla_provincia}'.")
    except Exception as e:
        print(f"Errore nell'ottenere i comuni della provincia '{sigla_provincia}': {e}")
    print()

    # Test 3: Cerca un comune per codice catastale
    print("---- TEST 3: Cerca un Comune per Codice Catastale ----")
    try:
        codice_catastale = "A074"
        comune_info = comuni.cerca_per_codice_catastale(codice_catastale)
        print(f"Informazioni sul comune con codice catastale '{codice_catastale}':")
        for key, value in comune_info.items():
            print(f"  {key.capitalize()}: {value}")
    except Exception as e:
        print(f"Errore nel cercare il comune con codice catastale '{codice_catastale}': {e}")
    print()

if __name__ == "__main__":
    main()
