from .loader import load_comuni_data
from .exceptions import ComuneNotFoundError

class Comuni:
    def __init__(self, csv_file="database/comuni.csv"):
        self.data = load_comuni_data(csv_file)

    def cerca_comune(self, nome_comune):
        """Cerca un comune per nome."""
        risultato = self.data[self.data['Denominazione in italiano'].str.lower() == nome_comune.lower()]
        if risultato.empty:
            raise ComuneNotFoundError(f"Il comune '{nome_comune}' non è stato trovato.")
        return risultato.iloc[0].to_dict()

    def comuni_per_provincia(self, sigla_provincia):
        """Restituisce tutti i comuni di una provincia."""
        risultato = self.data[self.data['Sigla automobilistica'].str.upper() == sigla_provincia.upper()]
        return risultato.to_dict(orient='records')
