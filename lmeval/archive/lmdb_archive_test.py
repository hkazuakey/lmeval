# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
