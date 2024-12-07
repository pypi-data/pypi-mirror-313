#!/usr/bin/python3

import os
os.makedirs("_versions", exist_ok=True)
os.makedirs("_sources", exist_ok=True) 
dest = "../src/assorthead"

def get_version_file(name):
    return os.path.join("_versions", name)

def already_exists(name, version):
    vfile = get_version_file(name)
    if os.path.exists(vfile):
        with open(vfile, 'r') as handle:
            existing_version = handle.read()
            if existing_version == version:
                return True
    return False

import subprocess
def git_clone(name, url, version):
    tmpname = os.path.join("_sources", name)

    if not os.path.exists(tmpname):
        out = subprocess.run(["git", "clone", url, tmpname])
        if out.returncode != 0:
            raise ValueError("failed to clone " + url);
    else:
        out = subprocess.run(["git", "-C", tmpname, "fetch", "--all"])
        if out.returncode != 0:
            raise ValueError("failed to fetch " + url);

    out = subprocess.run(["git", "-C", tmpname, "checkout", version])
    if out.returncode != 0:
        raise ValueError("failed to fetch " + url);
    return tmpname

import shutil
def purge_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)

def dir_copy(src, dest): 
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copytree(src, dest)

import collections
ManifestEntry = collections.namedtuple("ManifestEntry", ["name", "url", "version"])

manifest = []
with open("manifest.csv", "r") as handle:
    first = True
    for line in handle:
        if first:
            first = False
            continue
        payload = line.split(",")
        manifest.append(ManifestEntry(name=payload[0], url=payload[1], version=payload[2]))

##################################################

badbois = set([ "annoy", "hnswlib", "Eigen", "clrm1" ])
for i, man in enumerate(manifest):
    name = man.name
    url = man.url
    version = man.version

    if name in badbois:
        continue
    if already_exists(name, version):
        print(name + " (" + version + ") is already present")
        continue

    tmpname = git_clone(name, url, version)
    dest_include_path = os.path.join(dest, "include", name)
    purge_directory(dest_include_path)
    dir_copy(os.path.join(tmpname, "include", name), dest_include_path)

    dest_license_path = os.path.join(dest, "licenses", name)
    purge_directory(dest_license_path)
    os.makedirs(dest_license_path)
    shutil.copy2(os.path.join(tmpname, "LICENSE"), dest_license_path)

    vfile = get_version_file(name)
    with open(vfile, "w") as handle:
        handle.write(version)

####################################################

def download_annoy():
    name = "annoy"
    for x in manifest:
        if x.name == name:
            version = x.version
            url = x.url
            break

    if already_exists(name, version):
        print(name + " (" + version + ") is already present")
        return

    tmpname = git_clone(name, url, version)
    dest_include_path = os.path.join(dest, "include", name)
    purge_directory(dest_include_path)
    os.makedirs(dest_include_path)
    src_include_path = os.path.join(tmpname, "src")
    for x in os.listdir(src_include_path):
        if x.endswith(".h"):
            shutil.copy2(os.path.join(src_include_path, x), os.path.join(dest_include_path, x))

    dest_license_path = os.path.join(dest, "licenses", name)
    purge_directory(dest_license_path)
    os.makedirs(dest_license_path)
    shutil.copy2(os.path.join(tmpname, "LICENSE"), dest_license_path)

    vfile = get_version_file(name)
    with open(vfile, "w") as handle:
        handle.write(version)

download_annoy()

####################################################

def download_hnswlib():
    name = "hnswlib"
    for x in manifest:
        if x.name == name:
            version = x.version
            url = x.url
            break

    if already_exists(name, version):
        print(name + " (" + version + ") is already present")
        return

    tmpname = git_clone(name, url, version)
    dest_include_path = os.path.join(dest, "include", name)
    purge_directory(dest_include_path)
    dir_copy(os.path.join(tmpname, "hnswlib"), dest_include_path)

    dest_license_path = os.path.join(dest, "licenses", name)
    purge_directory(dest_license_path)
    os.makedirs(dest_license_path)
    shutil.copy2(os.path.join(tmpname, "LICENSE"), dest_license_path)

    vfile = get_version_file(name)
    with open(vfile, "w") as handle:
        handle.write(version)

download_hnswlib()

####################################################

def download_Eigen():
    name = "Eigen"
    for x in manifest:
        if x.name == name:
            version = x.version
            url = x.url
            break

    if already_exists(name, version):
        print(name + " (" + version + ") is already present")
        return

    tmpname = git_clone(name, url, version)
    dest_include_path = os.path.join(dest, "include", name)
    purge_directory(dest_include_path)
    dir_copy(os.path.join(tmpname, "Eigen"), dest_include_path)

    dest_license_path = os.path.join(dest, "licenses", name)
    purge_directory(dest_license_path)
    os.makedirs(dest_license_path)
    for x in os.listdir(tmpname):
        if x.startswith("COPYING."):
            shutil.copy2(os.path.join(tmpname, x), os.path.join(dest_license_path, x))

    vfile = get_version_file(name)
    with open(vfile, "w") as handle:
        handle.write(version)

download_Eigen()

###################################################

def download_clrm1():
    name = "clrm1"
    for x in manifest:
        if x.name == name:
            version = x.version
            url = x.url
            break

    if already_exists(name, version):
        print(name + " (" + version + ") is already present")
        return

    tmpname = git_clone(name, url, version)
    dest_include_path = os.path.join(dest, "include", name)
    purge_directory(dest_include_path)
    os.makedirs(dest_include_path)
    shutil.copy2(os.path.join(tmpname, "package", "src", "clrm1.hpp"), dest_include_path)

    dest_license_path = os.path.join(dest, "licenses", name)
    purge_directory(dest_license_path)
    os.makedirs(dest_license_path)
    shutil.copy2(os.path.join(tmpname, "LICENSE"), dest_license_path)

    vfile = get_version_file(name)
    with open(vfile, "w") as handle:
        handle.write(version)

download_clrm1()
