import os
from .loader import load_comuni_data
from .exceptions import ComuneNotFoundError


class Comuni:
    def __init__(self, csv_file=None):
        # Usa un percorso predefinito all'interno della libreria se `csv_file` non è specificato
        if csv_file is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))  # Directory del modulo `comuni.py`
            csv_file = os.path.join(base_dir, "database/comuni.csv")

        # Assegna il percorso e carica i dati
        self.csv_file = csv_file
        self.data = load_comuni_data(self.csv_file)

    def cerca_comune(self, nome_comune):
        """Cerca un comune per nome e restituisce solo i dati essenziali."""
        risultato = self.data[self.data['denominazione_italiana'].str.lower() == nome_comune.lower()]
        if risultato.empty:
            raise ComuneNotFoundError(f"Il comune '{nome_comune}' non è stato trovato.")

        comune = risultato.iloc[0]
        return {
            "nome": comune["denominazione_italiana"],
            "provincia": comune["provincia"],
            "sigla_provincia": comune["sigla_provincia"],
            "regione": comune["regione"],
            "codice_catastale": comune["codice_catastale"],
        }

    def comuni_per_provincia(self, sigla_provincia):
        """Restituisce tutti i comuni di una provincia con dati essenziali."""
        risultato = self.data[self.data['sigla_provincia'].str.upper() == sigla_provincia.upper()]
        comuni_filtrati = risultato.apply(
            lambda row: {
                "nome": row["denominazione_italiana"],
                "provincia": row["provincia"],
                "sigla_provincia": row["sigla_provincia"],
                "regione": row["regione"],
                "codice_catastale": row["codice_catastale"],
            }, axis=1
        )
        return comuni_filtrati.tolist()

    def cerca_per_codice_catastale(self, codice_catastale):
        """Cerca un comune per codice catastale e restituisce solo i dati essenziali."""
        risultato = self.data[self.data['codice_catastale'].str.upper() == codice_catastale.upper()]
        if risultato.empty:
            raise ComuneNotFoundError(f"Nessun comune trovato con il codice catastale '{codice_catastale}'.")

        comune = risultato.iloc[0]
        return {
            "nome": comune["denominazione_italiana"],
            "provincia": comune["provincia"],
            "sigla_provincia": comune["sigla_provincia"],
            "regione": comune["regione"],
            "codice_catastale": comune["codice_catastale"],
        }
