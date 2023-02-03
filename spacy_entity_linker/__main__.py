import sys
import tarfile
import urllib.request
import tqdm
import os


class DownloadProgressBar(tqdm.tqdm):
    """
    Code taken from https://stackoverflow.com/questions/15644964/python-progress-bar-and-downloads
    """
    def update_to(self, chunk_id=1, max_chunk_size=1, total_size=None):
        if total_size is not None:
            self.total = total_size
        self.update(chunk_id * max_chunk_size - self.n)


def download_knowledge_base(
    file_url="https://huggingface.co/MartinoMensio/spaCy-entity-linker/resolve/main/knowledge_base.tar.gz"
):
    OUTPUT_TAR_FILE = os.path.abspath(
        os.path.dirname(__file__)) + '/../data_spacy_entity_linker/wikidb_filtered.tar.gz'
    OUTPUT_DB_PATH = os.path.abspath(os.path.dirname(__file__)) + '/../data_spacy_entity_linker'
    if not os.path.exists(OUTPUT_DB_PATH):
        os.makedirs(OUTPUT_DB_PATH)
    with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc='Downloading knowledge base') as dpb:
        urllib.request.urlretrieve(file_url, filename=OUTPUT_TAR_FILE, reporthook=dpb.update_to)

    tar = tarfile.open(OUTPUT_TAR_FILE)
    tar.extractall(OUTPUT_DB_PATH)
    tar.close()

    os.remove(OUTPUT_TAR_FILE)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("No arguments given.")
        pass

    command = sys.argv.pop(1)

    if command == "download_knowledge_base":
        download_knowledge_base()
    else:
        raise ValueError("Unrecognized command given. If you are trying to install the knowledge base, run "
                         "'python -m spacy_entity_linker \"download_knowledge_base\"'.")
