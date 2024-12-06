from comuniitaliani import Comuni

comuni = Comuni()

# Cerca un comune
try:
    info = comuni.cerca_comune("Agliè")
    print("Comune trovato:", info)
except Exception as e:
    print("Errore:", e)

# Ottieni comuni di una provincia
try:
    provincia_comuni = comuni.comuni_per_provincia("TO")
    print("Comuni della provincia di TO:", provincia_comuni[:5])
except Exception as e:
    print("Errore:", e)
