import os
import tarfile
from autopiper import logger
from autopiper.download_github_release_asset import download_github_release_asset
from autopiper import settings


def download_piper_package(tag_name: str | None) -> None:
    # https://github.com/rhasspy/piper
    tag_name = tag_name or "2023.11.14-2"
    tar_gz_path = download_github_release_asset(
        owner="rhasspy",
        repo="piper",
        tag_name=tag_name,
        asset_name="piper_linux_x86_64.tar.gz",
        output_path=settings.CACHE_DIR,
    )
    tar_gz_extract_dir = settings.APP_ASSET_DIR.joinpath(tag_name)
    file = tarfile.open(tar_gz_path)
    file.extractall(path=tar_gz_extract_dir)
    file.close()
    logger.debug(f"Extracted {tar_gz_path} to {tar_gz_extract_dir}")

    # bin_dir = os.path.join(tar_gz_extract_dir, "piper")  # TODO save this to a config file
