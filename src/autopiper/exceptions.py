class GithubReleaseAssetNotFoundError(Exception):
    """Exception raised when a GitHub release asset is not found."""

    def __init__(
        self,
        owner: str,
        repo: str,
        tag_name: str,
        asset_name: str,
    ) -> None:
        msg = (
            f"Asset '{asset_name}' not found in release "
            f"'{tag_name}' of {owner}/{repo}"
        )
        super().__init__(msg)
