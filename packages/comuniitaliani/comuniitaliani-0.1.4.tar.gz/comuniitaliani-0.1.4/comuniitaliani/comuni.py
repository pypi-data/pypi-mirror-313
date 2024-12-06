from .loader import load_comuni_data
from .exceptions import ComuneNotFoundError


class Comuni:
    def __init__(self, csv_file="database/comuni.csv"):
        self.data = load_comuni_data(csv_file)

    def cerca_comune(self, nome_comune):
        """Cerca un comune per nome e restituisce solo i dati essenziali."""
        risultato = self.data[self.data['Denominazione in italiano'].str.lower() == nome_comune.lower()]
        if risultato.empty:
            raise ComuneNotFoundError(f"Il comune '{nome_comune}' non è stato trovato.")

        comune = risultato.iloc[0]
        # Filtra e rinomina solo i dati essenziali
        return {
            "nome": comune["Denominazione in italiano"],
            "provincia": comune["Denominazione dell'unità territoriale sovracomunale \n(valida a fini statistici)"],
            "sigla_provincia": comune["Sigla automobilistica"],
            "regione": comune["Denominazione regione"],
            "codice_catastale": comune["Codice catastale del comune"],
        }

    def comuni_per_provincia(self, sigla_provincia):
        """Restituisce tutti i comuni di una provincia con dati essenziali."""
        risultato = self.data[self.data['Sigla automobilistica'].str.upper() == sigla_provincia.upper()]
        comuni_filtrati = risultato.apply(
            lambda row: {
                "nome": row["Denominazione in italiano"],
                "provincia": row["Denominazione dell'unità territoriale sovracomunale \n(valida a fini statistici)"],
                "sigla_provincia": row["Sigla automobilistica"],
                "regione": row["Denominazione regione"],
                "codice_catastale": row["Codice catastale del comune"],
            }, axis=1
        )
        return comuni_filtrati.tolist()

    def cerca_per_codice_catastale(self, codice_catastale):
        """Cerca un comune per codice catastale e restituisce solo i dati essenziali."""
        risultato = self.data[self.data['Codice catastale del comune'].str.upper() == codice_catastale.upper()]
        if risultato.empty:
            raise ComuneNotFoundError(f"Nessun comune trovato con il codice catastale '{codice_catastale}'.")

        comune = risultato.iloc[0]
        # Filtra e rinomina solo i dati essenziali
        return {
            "nome": comune["Denominazione in italiano"],
            "provincia": comune["Denominazione dell'unità territoriale sovracomunale \n(valida a fini statistici)"],
            "sigla_provincia": comune["Sigla automobilistica"],
            "regione": comune["Denominazione regione"],
            "codice_catastale": comune["Codice catastale del comune"],
        }
