import pandas as pd
import os
import requests
from datetime import datetime

ISTAT_CSV_URL = "http://www.istat.it/storage/codici-unita-amministrative/Elenco-comuni-italiani.csv"

# Percorso della directory "database" basato sul file corrente
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV_PATH = os.path.join(BASE_DIR, "database/comuni.csv")


def get_remote_last_modified():
    """Recupera la data dell'ultima modifica del CSV remoto."""
    try:
        response = requests.head(ISTAT_CSV_URL)
        response.raise_for_status()
        remote_last_modified = response.headers.get('Last-Modified')
        if remote_last_modified:
            return datetime.strptime(remote_last_modified, '%a, %d %b %Y %H:%M:%S %Z')
    except Exception as e:
        print(f"Impossibile ottenere la data di ultima modifica del file remoto: {e}")
        return None


def get_local_last_modified(local_path):
    """Recupera la data di ultima modifica del file locale."""
    if os.path.exists(local_path):
        return datetime.fromtimestamp(os.path.getmtime(local_path))
    return None


def is_csv_updated(local_path=DEFAULT_CSV_PATH):
    """Controlla se il file CSV locale è aggiornato rispetto alla versione remota."""
    remote_last_modified = get_remote_last_modified()
    local_last_modified = get_local_last_modified(local_path)

    # Se non è possibile ottenere la data remota, consideriamo il file locale valido
    if remote_last_modified is None:
        print("Non è stato possibile verificare l'aggiornamento remoto. Uso il file locale.")
        return os.path.exists(local_path)

    # Verifica aggiornamento basandosi sulla data
    if local_last_modified is None or local_last_modified < remote_last_modified:
        return False  # Non aggiornato
    return True  # Aggiornato


def download_csv(local_path=DEFAULT_CSV_PATH):
    """Scarica il file CSV dell'ISTAT e lo salva localmente."""
    try:
        response = requests.get(ISTAT_CSV_URL, stream=True)
        response.raise_for_status()
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"CSV scaricato correttamente: {local_path}")
    except Exception as e:
        raise Exception(f"Errore durante il download del file CSV: {e}")


def clean_column_names(columns):
    """Pulisce i nomi delle colonne per renderli coerenti."""
    return (
        columns
        .str.strip()  # Rimuovi spazi iniziali e finali
        .str.replace('\n', ' ', regex=False)  # Sostituisci newline con uno spazio
        .str.replace(r'\s+', '_', regex=True)  # Sostituisci spazi multipli con _
        .str.lower()  # Convertili in minuscolo
    )


def load_comuni_data(csv_file):
    """Carica i dati dei comuni dal file CSV."""
    if not is_csv_updated(csv_file):
        print("Il file CSV non è aggiornato. Download in corso...")
        download_csv(csv_file)
    else:
        print("Il file CSV è già aggiornato.")

    # Carica il CSV
    data = pd.read_csv(csv_file, encoding='latin1', delimiter=';')

    # Pulisce i nomi delle colonne
    data.columns = clean_column_names(data.columns)

    # Rinomina le colonne per semplicità
    data.rename(columns={
        "denominazione_in_italiano": "denominazione_italiana",
        "sigla_automobilistica": "sigla_provincia",
        "denominazione_regione": "regione",
        "denominazione_dell'unità_territoriale_sovracomunale_(valida_a_fini_statistici)": "provincia",
        "codice_catastale_del_comune": "codice_catastale"
    }, inplace=True)

    return data
