import os
from loguru import logger


def download_source(github_access_token, git_repository, git_ref) -> None:
    # Download code to current directory
    logger.debug(f"Downloading source code from {git_repository} {git_ref}")
    url = f"https://api.github.com/repos/{git_repository}/tarball/{git_ref}"
    # TODO: switch to supbrocess.run or subprocess.Popen
    result = os.system(
        f"curl -s -L -H 'Accept: application/vnd.github+json' -H 'Authorization: Bearer {github_access_token}' -H 'X-GitHub-Api-Version: 2022-11-28' {url} | tar zx --strip-components 1 -C ."
    )

    if result != 0:
        raise Exception("Failed to import repository.")
