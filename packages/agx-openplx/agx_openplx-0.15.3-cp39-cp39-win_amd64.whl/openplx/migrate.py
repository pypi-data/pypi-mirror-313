#!/usr/bin/env python3
"""
Command line utility that helps migrating OpenPLX files to a newer version
"""
from pathlib import Path
import itertools
import os
import tempfile
import json
import urllib.request
import zipfile
from io import BytesIO
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, SUPPRESS
import agx
from openplx import __version__, get_error_strings
from openplx.Core import OpenPlxContext, parseFromFile, analyze, StringVector, DocumentVector
from openplx.migrations import collect_migrations, ReplaceOp, split_version
from openplx.versionaction import VersionAction
from openplx import register_plugins

def download_package_version(package_name, version):
    """Download a specific version of a package from PyPI."""
    url = f"https://pypi.org/pypi/{package_name}/{version}/json"
    with urllib.request.urlopen(url, timeout=16) as response:
        content = response.read().decode('utf-8')
    data = json.loads(content)
    return data['urls'][0]['url']


def unzip_package(url, extract_to):
    """Download and unzip a package."""
    with urllib.request.urlopen(url, timeout=32) as response:
        file_data = BytesIO(response.read())
    with zipfile.ZipFile(file_data) as zip_file:
        zip_file.extractall(extract_to)

def parse_args():
    parser = ArgumentParser(description="Migrates a .openplx file from an older to a newer version", formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("openplxfile", metavar="path", help="the .openplx file or directory to migrate")
    parser.add_argument("--version", help="Show version", action=VersionAction, nargs=0, default=SUPPRESS)
    parser.add_argument("--from-version", help="Version to convert from", required=True)
    parser.add_argument("--to-version", help="Version to convert to", default=__version__)
    return parser.parse_known_args()

def parse_and_analyze(openplxfile, openplx_context):
    parse_result = parseFromFile(str(Path(openplxfile).absolute()), openplx_context)

    documents = DocumentVector()

    if parse_result[0] is None:
        return documents

    analyze(openplx_context, None)

    documents.push_back(parse_result[0])
    return documents

def has_errors(openplx_context):
    if openplx_context.hasErrors():
        error_strings = get_error_strings(openplx_context.getErrors())
        for e_s in error_strings:
            print(e_s)
        return True
    return False

def refactor_openplx_file(migration, openplxfile, bundle_path_vec, from_version, to_version) -> bool: # pylint: disable=too-many-locals
    print(f"Migrating {openplxfile} from {from_version} to {to_version}")
    file_rename_migrations = []
    if migration.__name__ == "rename_from_brick_to_openplx":
        file_rename_migrations.append(migration(openplxfile))
        if openplxfile.endswith("config.openplx") or openplxfile.endswith("config.brick"):
            for m in file_rename_migrations:
                m.apply_to(None, None)
            return True

    openplx_context = OpenPlxContext(bundle_path_vec)
    register_plugins(openplx_context, None)
    documents = parse_and_analyze(openplxfile, openplx_context)

    if has_errors(openplx_context):
        return False

    if migration.__name__ == "rename_from_brick_to_openplx":
        for m in file_rename_migrations:
            m.apply_to(None, None)
    else:
        ops = migration(documents)

        for key, op_group in itertools.groupby(ops, lambda op: op.path):
            if Path(openplxfile).samefile(key):
                with open(key, 'r', encoding="utf8") as file:
                    lines = file.readlines()
                replace_ops = [op for op in op_group if isinstance(op, ReplaceOp)]
                lines = ReplaceOp.apply_many(replace_ops, lines)
                with open(key, 'w', encoding="utf8") as file:
                    file.writelines(lines)

    return True

def config_file_path(openplxfile, version):
    config_file_name = 'config.openplx'
    if split_version(version) < (0, 15, 0):
        config_file_name = 'config.brick'
    if os.path.isdir(openplxfile):
        return os.path.join(openplxfile, config_file_name)
    return os.path.join(os.path.dirname(openplxfile), config_file_name)

def migrate_config_file_versions(config_path, from_version, to_version):
    bundles = ["Math", "Physics", "Physics1D", "Physics3D",
               "Robotics", "Urdf", "Terrain", "Vehicles",
               "Simulation", "Visuals", "DriveTrain"]
    add_versions = (split_version(from_version) < (0, 11, 0)
                    and split_version(to_version) >= (0, 11, 0))
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding="utf8") as file:
            lines = file.readlines()
        lines = list(map(lambda line: line.replace(f"=={from_version}", f"=={to_version}"), lines))
        if add_versions:
            for i in range(len(lines)): # pylint: disable=consider-using-enumerate
                for bundle in bundles:
                    lines[i] = lines[i].replace(f"\"{bundle}\"", f"\"{bundle}=={to_version}\"")
        with open(config_path, 'w', encoding="utf8") as file:
            file.writelines(lines)

def run_openplx_migrate_from_version(migration, from_version, to_version, openplxfile): # pylint: disable=too-many-locals
    package_name = 'openplx-bundles'

    if split_version(from_version) < (0, 15, 0):
        package_name = 'brickbundles'

    # Download the package
    url = download_package_version(package_name, from_version)
    if url is None:
        print(f"Could not find the source distribution for {package_name}=={from_version}.")
        return

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmp_path = str(Path(os.path.realpath(tmpdirname)).absolute())
        print(f"Extracting to temporary directory: {tmp_path}")
        unzip_package(url, tmp_path)
        print(f"Package {package_name}=={from_version} extracted to {tmp_path}")
        bundle_path = str((Path(tmp_path) / package_name.replace("-", "")).absolute())

        print(f'Using bundle path {bundle_path}')
        print(os.listdir(bundle_path))

        bundle_path_vec = StringVector()
        bundle_path_vec.push_back(bundle_path)
        success = True
        # Apply the refactoring
        if os.path.isdir(openplxfile):
            for root, _, files in os.walk(openplxfile):
                for file in files:
                    if file.endswith(".openplx") or file.endswith(".brick"):
                        openplxfile = os.path.join(root, file)
                        if not refactor_openplx_file(migration, openplxfile,
                                                     bundle_path_vec, from_version, to_version):
                            success = False
        else:
            if not refactor_openplx_file(migration, openplxfile,
                                         bundle_path_vec, from_version, to_version):
                success = False
        if success:
            print(f"Refactor from {from_version} to {to_version} complete!")
        else:
            print(f"Refactor from {from_version} to {to_version} failed due to errors!")
            print("Note, some files might have been partially migrated.")


def run_openplx_migrate(args):
    migrations = collect_migrations(args.from_version, args.to_version)
    current_version = args.from_version
    for migration in migrations:
        migrate_config_file_versions(config_file_path(args.openplxfile, current_version),
                                     current_version, migration.openplx_from_version)
        run_openplx_migrate_from_version(migration, migration.openplx_from_version,
                                         migration.openplx_to_version, args.openplxfile)
        migrate_config_file_versions(
            config_file_path(args.openplxfile, migration.openplx_from_version),
            migration.openplx_from_version, migration.openplx_to_version)
        current_version = migration.openplx_to_version

def run():
    arguments, _ = parse_args()
    init = agx.AutoInit()  # pylint: disable=W0612 # Unused variable 'init'
    run_openplx_migrate(arguments)

if __name__ == '__main__':
    run()
