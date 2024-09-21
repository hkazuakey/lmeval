import json
import tempfile
import time
import zlib

import lmdb
from lmeval import system_config
from lmeval import utils
from lmeval.archive.archive import Archive


class LMDBArchive(Archive):
    """Use LMDB Archive to hold data in storage."""
    def __init__(self, path,
                 compression_level: int = -1,
                 keyfname: str = 'data.key',
                 map_size: int = 2_000_000_000,
                 use_tempfile: bool | None = None,
                 restore: bool = True):
        super().__init__(name="LMDBArchive", version="1.0")
        self.temp_dir = None
        if use_tempfile is None:
            use_tempfile = system_config.CONFIG["use_tempfile"]
        if use_tempfile:
            self.temp_dir = tempfile.TemporaryDirectory()
            self.path = self.temp_dir.name
            self.real_path = path
            p = utils.Path(self.real_path)
            if restore and  p.exists():
                utils.recursively_copy_dir(self.real_path, self.path, overwrite=True)
        else:
            self.path = path
            self.real_path = None
            p = utils.Path(self.path)
            if not p.exists():
                p.mkdir(parents=True)
        self.path = str(self.path)
        try:
            self.arxiv = lmdb.open(self.path, map_size=map_size)
        except Exception as e:
            raise ValueError(f"Error opening LMDB archive at {self.path}: {e}")

        self.compression_level = compression_level
        self.keyfname = keyfname
        self.key = ""
        self.filesinfo_name = "files_info.json"
        self.filesinfo = {}  # used to track files

    def __del__(self):
        if self.arxiv:
            self.persist()
            self.arxiv.close()
            if self.temp_dir is not None:
                self.temp_dir.cleanup()

    def write(self, name: str, data: bytes|str, encrypted: bool):

        # compress data
        if isinstance(data, str):
            data = data.encode("utf-8")
        compressed_data = zlib.compress(data, level=self.compression_level)

        if encrypted:
            compressed_data = self._encrypt_data(compressed_data)

        self.filesinfo[name] = {
            "encrypted": encrypted,
            "write_ts": int(time.time()),
            "original_size": len(data),
            "compressed_size": len(compressed_data),
            "hash": self._compute_hash(data)
        }

        with self.arxiv.begin(write=True) as txn:
            # write data
            txn.put(name.encode(), compressed_data)

            # update filesinfo
            compressed_filesinfo = json.dumps(self.filesinfo).encode()
            compressed_filesinfo = zlib.compress(compressed_filesinfo,
                                                 level=self.compression_level)
            txn.put(self.filesinfo_name.encode(), compressed_filesinfo)

        # ensure everything is written to disk
        self.arxiv.sync()

    def read(self, name: str) -> bytes|str:
        with self.arxiv.begin() as txn:
            data = txn.get(name.encode())
            if data is None:
                raise KeyError(f"No file named '{name}' found")

            #  get filesinfo
            filesinfo_data = txn.get(self.filesinfo_name.encode())
            filesinfo_data = zlib.decompress(filesinfo_data)
            self.filesinfo = json.loads(filesinfo_data)

            # ! special case when we extract fileinfo
            if name == self.filesinfo_name:
                return filesinfo_data

            if name in self.filesinfo and self.filesinfo[name]["encrypted"]:
                data = self._decrypt_data(data)
            data = zlib.decompress(data)
            return data

    def list_files(self):
        fnames = []
        with self.arxiv.begin() as txn:
            cursor = txn.cursor()
            for k, v in cursor:
                fnames.append(k.decode())
        return fnames

    def _get_keyset(self) -> str:
        "read encryption key from archive and returns it"
        if self.key:
            return self.key

        with self.arxiv.begin(write=True) as txn:

            key = txn.get(self.keyfname.encode())
            if key:
                self.key = zlib.decompress(key).decode()
            else:
                # If the key is not in the archive, write it
                if not self.KEYSET_STR:
                    raise ValueError(
                        "No key found in archive and self.KEYSET_STR is not set")

                ckey = zlib.compress(self.KEYSET_STR.encode(),
                                     level=self.compression_level)

                txn.put(self.keyfname.encode(), ckey)
                self.key = self.KEYSET_STR

        return self.key

    def persist(self):
        "persist the archive to the 'real_path'"
        if self.real_path is not None:
            self.arxiv.sync()
            p = utils.Path(self.real_path)
            if not p.exists():
                p.mkdir(parents=True)
            utils.recursively_copy_dir(self.path, self.real_path,
                                       overwrite=True, backup=True)
