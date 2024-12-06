import pandas as pd
import os
import requests
from datetime import datetime

ISTAT_CSV_URL = "http://www.istat.it/storage/codici-unita-amministrative/Elenco-comuni-italiani.csv"

def get_remote_last_modified():
    """Recupera la data dell'ultima modifica del CSV remoto."""
    response = requests.head(ISTAT_CSV_URL)
    if response.status_code == 200:
        remote_last_modified = response.headers.get('Last-Modified')
        if remote_last_modified:
            return datetime.strptime(remote_last_modified, '%a, %d %b %Y %H:%M:%S %Z')
    raise Exception("Impossibile ottenere la data di ultima modifica del file remoto.")

def get_local_last_modified(local_path):
    """Recupera la data di ultima modifica del file locale."""
    if os.path.exists(local_path):
        return datetime.fromtimestamp(os.path.getmtime(local_path))
    return None

def is_csv_updated(local_path="database/comuni.csv"):
    """Controlla se il file CSV locale è aggiornato rispetto alla versione remota."""
    try:
        remote_last_modified = get_remote_last_modified()
        local_last_modified = get_local_last_modified(local_path)
        if local_last_modified is None or local_last_modified < remote_last_modified:
            return False  # Non aggiornato
        return True  # Aggiornato
    except Exception as e:
        print(f"Errore durante il controllo dell'aggiornamento: {e}")
        return False

def download_csv(local_path="database/comuni.csv"):
    """Scarica il file CSV dell'ISTAT e lo salva localmente."""
    response = requests.get(ISTAT_CSV_URL)
    if response.status_code == 200:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, 'wb') as file:
            file.write(response.content)
        print(f"CSV scaricato correttamente: {local_path}")
    else:
        raise Exception("Errore durante il download del file CSV.")

def load_comuni_data(csv_file="database/comuni.csv"):
    """Carica i dati dei comuni dal file CSV."""
    if not is_csv_updated(csv_file):
        print("Il file CSV non è aggiornato. Download in corso...")
        download_csv(csv_file)
    else:
        print("Il file CSV è già aggiornato.")
    return pd.read_csv(csv_file, encoding='latin1', delimiter=';')
