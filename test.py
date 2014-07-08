import git
import os
# from git import Repo

repo = git.Repo('/tmp/testmanager/manual-test-definitions.git/')

rev = repo.commit("9b0c65d2ea3ce8c1f1a21fb15d40973fb96ed9b7")

files = {}
for element in rev.tree.list_traverse():
    if element.mode == git.Blob.file_mode:
        files[element.path] = element

for element in rev.tree.list_traverse():
    if element.mode == git.Blob.link_mode:
        real_path = os.path.realpath(element.data_stream.read()).lstrip("/")
        files[element.path] = files[real_path]

print(files)
