import importlib
import os
import shutil
import zipfile
from pathlib import Path
from time import perf_counter
from typing import Any

from watch_lite import getHash

from .colors import completeColor, fileColor, folderColor, tagColor
from .config import dumpHashes, loadConfig, loadToml
from .transformations import minifyFile, minifyToString


def bundleFiles(
    sourceDirectory: Path = Path("./src/"),
    outputDirectory: Path = Path("./out"),
    outputFileName: str = "bundle.pyz",
    compressionLevel: int = 5,
    minification: bool = True,
) -> None:
    """Bundles dependencies and scripts into a single .pyz archive

    Args:
        sourceDirectory (Path): Source directory which must contain a __main__.py script
        outputDirectory (Path): Output directory for the bundle
        outputFileName (str): Name of the output bundle
        compressionLevel (int): Compression level for the bundle from 0-9
        minification (bool): If the scripts should be minified
    """
    outputDirectory.mkdir(parents=True, exist_ok=True)
    outputPath: Path = outputDirectory / outputFileName

    if outputPath.exists():
        outputPath.unlink()

    with zipfile.ZipFile(
        outputPath,
        "w",
        compresslevel=compressionLevel,
        compression=zipfile.ZIP_DEFLATED,
    ) as bundler:
        cachePath: Path = Path("./.effectual_cache/cachedPackages")
        if cachePath.exists():
            if os.listdir(cachePath):
                totalSize: int = int(0)
                for cachedFile in cachePath.rglob("*"):
                    if cachedFile.is_dir() and not any(cachedFile.iterdir()):
                        continue
                    totalSize += cachedFile.stat().st_size
                    arcName = cachedFile.relative_to(cachePath)
                    bundler.write(cachedFile, arcname=arcName)

                print(
                    f"{tagColor('bundling')}   || uv dependencies {folderColor(totalSize)}"  # noqa: E501
                )

        for pyFile in sourceDirectory.rglob("*.py"):
            print(f"{tagColor('bundling')}   || {pyFile.name} {fileColor(pyFile)}")
            if minification:
                fileContents = minifyToString(pyFile)
                bundler.writestr(zinfo_or_arcname=pyFile.name, data=fileContents)
            else:
                bundler.write(pyFile, arcname=pyFile.name)

    print(f"{tagColor('OUTPUT')}     || {outputFileName} {fileColor(outputPath)}")


def dependencies(minify: bool) -> None:
    packages: list[str] = (
        loadToml("./pyproject.toml").get("project").get("dependencies")
    )

    if len(packages) != 0:
        arguments: list[str] = [
            "--no-compile",
            "--quiet",
            "--no-binary=none",
            "--no-cache",
        ]

        pathToInstallTo: str = "./.effectual_cache/cachedPackages"
        argumentString: str = " ".join(arguments)

        if Path(pathToInstallTo).exists():
            shutil.rmtree(pathToInstallTo)

        for key in packages:
            print(f"{tagColor('installing')} || {key}")
            os.system(
                f'uv pip install "{key}" {argumentString} --target {pathToInstallTo}'
            )

        print(f"{tagColor('optimizing')} || {', '.join(packages)}")

        multiprocessing = importlib.import_module("multiprocessing")

        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            pool.map(optimizeDependencies, Path(pathToInstallTo).rglob("*"))


def optimizeDependencies(file: Path) -> None:
    stringFile: str = str(file)
    if (
        file.suffix in (".pyc", ".pyd", ".exe", ".typed")
        or "__pycache__" in stringFile
        or ".dist-info" in stringFile
        or ".lock" in stringFile
    ):
        try:
            file.unlink()
        except PermissionError:
            pass
    elif file.suffix == ".py":
        minifyFile(file)


def main() -> None:
    """Entrypoint

    Raises:
        RuntimeError: In the event there is no source directory
    """

    configData: dict[str, Any] = loadConfig("./pyproject.toml")

    sourceDirectory: Path = Path(configData.get("sourceDirectory", "src/"))
    outputDirectory: Path = Path(configData.get("outputDirectory", "out/"))
    outputFileName: str = configData.get("outputFileName", "bundle.pyz")
    compressionLevel: int = max(
        0, min(9, configData.get("compressionLevel", 5))
    )  # Default level if not set
    minification: bool = configData.get("minification", True)

    if not sourceDirectory.is_dir():
        raise RuntimeError(
            f"Source directory {sourceDirectory} does not exist or is not a directory."
        )

    uvHashPath: Path = Path("./.effectual_cache/pyprojectHash.toml")
    currentHash: dict[str, dict[str, str]] = dict()

    startTime = perf_counter()

    Path("./.effectual_cache/").mkdir(parents=True, exist_ok=True)
    currentHash["hashes"] = dict()
    currentHash["hashes"]["pyproject"] = getHash("./pyproject.toml")
    currentHash["hashes"]["lock"] = getHash("./uv.lock")

    if uvHashPath.exists():
        lastHash: dict[str, Any] = loadToml(uvHashPath).get("hashes")
        if currentHash["hashes"] != lastHash:
            with open(uvHashPath, "w") as file:
                dumpHashes(currentHash, file)
            dependencies(minify=minification)
    else:
        with open(uvHashPath, "x") as file:
            dumpHashes(currentHash, file)
        dependencies(minify=minification)

    bundleFiles(
        sourceDirectory,
        outputDirectory,
        outputFileName,
        compressionLevel,
        minification,
    )
    endTime = perf_counter()

    print(completeColor(f"Completed in {endTime - startTime:.4f}s"))


if "__main__" in __name__:
    main()
