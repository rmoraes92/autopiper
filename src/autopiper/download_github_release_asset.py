from pathlib import Path
import requests
import os
from autopiper import logger
from autopiper.exceptions import GithubReleaseAssetNotFoundError


def download_github_release_asset(
    owner: str,
    repo: str,
    tag_name: str,
    asset_name: str,
    output_path: Path,
):
    """
    Downloads a specific asset from a GitHub release.

    Args:
        owner (str): The owner of the repository (e.g., 'octocat').
        repo (str): The name of the repository (e.g., 'Spoon-Knife').
        tag_name (str): The tag name of the release (e.g., 'v1.0').
        asset_name (str): The name of the asset to download (e.g., 'my_binary.zip').
        output_path (str, optional): The directory to save the downloaded asset. Defaults to the current directory.

    Returns:
        bool: True if the download was successful, False otherwise.
    """

    file_path = Path(output_path, asset_name)

    if file_path.is_file():
        logger.debug(
            f"file '{file_path}' already exists, skipping download of '{asset_name}'"
        )
        return Path(file_path)

    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{tag_name}"

    response = requests.get(api_url)
    response.raise_for_status()  # Raise an exception for bad status codes
    logger.debug(f"API response status code: {response.status_code}, URL: {api_url}")

    release_data = response.json()
    assets = release_data.get("assets", [])

    download_url = None
    for asset in assets:
        if asset["name"] == asset_name:
            logger.debug("found asset '%s' in release '%s'", asset_name, tag_name)
            download_url = asset["url"]
            break

    if not download_url:
        logger.debug(
            f"asset '{asset_name}' not found in release '{tag_name}' of {owner}/{repo}"
        )
        raise GithubReleaseAssetNotFoundError(
            owner=owner,
            repo=repo,
            tag_name=tag_name,
            asset_name=asset_name,
        )

    headers = {"Accept": "application/octet-stream"}
    download_response = requests.get(download_url, headers=headers, stream=True)
    download_response.raise_for_status()
    logger.debug(f"download response status code: {download_response.status_code}")

    os.makedirs(output_path, exist_ok=True)

    with file_path.open("wb") as f:
        for chunk in download_response.iter_content(chunk_size=8192):
            f.write(chunk)

    logger.debug(
        f"successfully downloaded '{asset_name}' from release '{tag_name}' of {owner}/{repo} to '{file_path}'"
    )

    return file_path
