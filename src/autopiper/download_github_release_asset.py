from pathlib import Path
import requests
import os
from autopiper.logger import setup_logger
from autopiper.exceptions import GithubReleaseAssetNotFoundError

logger = setup_logger()


def download_github_release_asset(
    owner: str,
    repo: str,
    tag_name: str,
    asset_name: str,
    output_path: str | None = None,
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

    output_path = output_path or os.getcwd()
    output_path = os.path.expanduser(output_path)
    file_path = os.path.join(output_path, asset_name)

    if os.path.exists(file_path):
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

    with open(file_path, "wb") as f:
        for chunk in download_response.iter_content(chunk_size=8192):
            f.write(chunk)

    logger.debug(
        f"successfully downloaded '{asset_name}' from release '{tag_name}' of {owner}/{repo} to '{file_path}'"
    )

    return Path(file_path)


if __name__ == "__main__":
    # Example usage:
    owner = "octocat"
    repo = "Spoon-Knife"
    tag_name = "v1.0"
    asset_name = "octocat-v1.0.zip"  # Replace with the actual asset name
    output_directory = "downloads"

    success = download_github_release_asset(
        owner, repo, tag_name, asset_name, output_directory
    )
    if success:
        print("Download completed.")
    else:
        print("Download failed.")

    # Another example: Downloading from the latest release
    def download_latest_github_release_asset(owner, repo, asset_name, output_path="."):
        api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            release_data = response.json()
            tag_name = release_data.get("tag_name")
            if not tag_name:
                print(
                    f"Could not find tag name for the latest release of {owner}/{repo}"
                )
                return False
            return download_github_release_asset(
                owner, repo, tag_name, asset_name, output_path
            )
        except requests.exceptions.RequestException as e:
            print(f"Error fetching latest release info: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    owner_latest = "kubernetes"
    repo_latest = "kubernetes"
    asset_name_latest = (
        "kubernetes-server-linux-amd64.tar.gz"  # Replace with an actual asset name
    )
    output_directory_latest = "latest_downloads"

    # Note: The above asset name is just a placeholder. You need to find an actual asset in the latest release.
    # You can inspect the JSON response of the latest release API to find the correct asset name.
    # Example of how to inspect the latest release data:
    # latest_release_info = requests.get(f"https://api.github.com/repos/{owner_latest}/{repo_latest}/releases/latest").json()
    # print(latest_release_info['assets'])

    # Uncomment the following lines to try downloading from the latest release (after finding a valid asset name)
    # success_latest = download_latest_github_release_asset(owner_latest, repo_latest, asset_name_latest, output_directory_latest)
    # if success_latest:
    #     print("Download from latest release completed.")
    # else:
    #     print("Download from latest release failed.")
