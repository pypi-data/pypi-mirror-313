from .loader import load_comuni_data
from .exceptions import ComuneNotFoundError


class Comuni:
    def __init__(self, csv_file="database/comuni.csv"):
        self.data = load_comuni_data(csv_file)

    def cerca_comune(self, nome_comune):
        """Cerca un comune per nome e restituisce solo i dati essenziali."""
        risultato = self.data[self.data['Denominazione_italiana'].str.lower() == nome_comune.lower()]
        if risultato.empty:
            raise ComuneNotFoundError(f"Il comune '{nome_comune}' non è stato trovato.")

        comune = risultato.iloc[0]
        # Filtra e rinomina solo i dati essenziali
        return {
            "nome": comune["Denominazione_italiana"],
            "provincia": comune["Provincia"],
            "sigla_provincia": comune["Sigla_provincia"],
            "regione": comune["Regione"],
            "codice_catastale": comune["Codice_catastale"],
        }

    def comuni_per_provincia(self, sigla_provincia):
        """Restituisce tutti i comuni di una provincia con dati essenziali."""
        risultato = self.data[self.data['Sigla_provincia'].str.upper() == sigla_provincia.upper()]
        comuni_filtrati = risultato.apply(
            lambda row: {
                "nome": row["Denominazione_italiana"],
                "provincia": row["Provincia"],
                "sigla_provincia": row["Sigla_provincia"],
                "regione": row["Regione"],
                "codice_catastale": row["Codice_catastale"],
            }, axis=1
        )
        return comuni_filtrati.tolist()

    def cerca_per_codice_catastale(self, codice_catastale):
        """Cerca un comune per codice catastale e restituisce solo i dati essenziali."""
        risultato = self.data[self.data['Codice_catastale'].str.upper() == codice_catastale.upper()]
        if risultato.empty:
            raise ComuneNotFoundError(f"Nessun comune trovato con il codice catastale '{codice_catastale}'.")

        comune = risultato.iloc[0]
        # Filtra e rinomina solo i dati essenziali
        return {
            "nome": comune["Denominazione_italiana"],
            "provincia": comune["Provincia"],
            "sigla_provincia": comune["Sigla_provincia"],
            "regione": comune["Regione"],
            "codice_catastale": comune["Codice_catastale"],
        }
