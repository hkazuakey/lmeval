import pytest
from time import time
from lmeval.archive.lmdb_archive import LMDBArchive


def test_encryption(tmp_path_factory):
    "test encryption"
    bench_dir = tmp_path_factory.mktemp("benchmark_files") / f"tesT_encryption_{int(time())}"
    path = bench_dir / "benchmark_test.lmarxiv"
    archive = LMDBArchive(path=path)
    data = b"Hello World"
    encrypted_data = archive._encrypt_data(data)
    assert data != encrypted_data
    decrypted_data = archive._decrypt_data(encrypted_data)
    assert data == decrypted_data

def test_encrypted_storage(tmp_path_factory):
    bench_dir = tmp_path_factory.mktemp("benchmark_files") / f"test_encrypted_storage_{int(time())}"
    path = bench_dir / "benchmark_test.lmarxiv"
    archive = LMDBArchive(path=path)
    data = b"Hello World"
    archive.write("data", data, encrypted=True)
    data2 = archive.read("data")
    assert data == data2
