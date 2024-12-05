import os
import requests
from pathlib import Path
import hashlib
from tqdm import tqdm
from .config import config

class MetaDataManager:
    def __init__(self, data_dir=config['archive.local']):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def get_data(self, filename, url, checksum=None):
        local_path = self.data_dir / filename

        if local_path.exists():
            #if checksum and self._verify_checksum(local_path, checksum):
            return str(local_path)

        # Download the file with progress bar
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte

        if not local_path.parent.exists():
            local_path.parent.mkdir(parents=True)
            
        with local_path.open('wb') as f:
            with tqdm(total=total_size, unit='iB', unit_scale=True, desc=filename) as pbar:
                for data in response.iter_content(block_size):
                    f.write(data)
                    pbar.update(len(data))

        if checksum and not self._verify_checksum(local_path, checksum):
            raise ValueError(f"Checksum mismatch for {filename}")

        #local_path.write_bytes(cache_path.read_bytes())
        return str(local_path)

    def _verify_checksum(self, file_path, expected_checksum):
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest() == expected_checksum
