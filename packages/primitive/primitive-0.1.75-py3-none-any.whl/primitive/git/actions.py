import os
from pathlib import Path

from gql import gql
from loguru import logger

from primitive.utils.actions import BaseAction

from ..utils.auth import guard
from .graphql.queries import github_app_token_query


class Git(BaseAction):
    @guard
    def get_github_access_token(self) -> str:
        query = gql(github_app_token_query)
        filters = {}
        variables = {
            "filters": filters,
        }
        result = self.primitive.session.execute(
            query, variable_values=variables, get_execution_result=True
        )
        return result

    def download_git_repository_at_ref(
        self,
        git_repo_full_name: str,
        github_access_token: str,
        git_ref: str = "main",
        destination: Path = Path.cwd(),
    ) -> Path:
        logger.debug(f"Downloading source code from {git_repo_full_name} {git_ref}")
        # TODO: switch to subprocess.run or subprocess.Popen
        url = f"https://api.github.com/repos/{git_repo_full_name}/tarball/{git_ref}"
        untar_dir = Path(destination).joinpath(git_repo_full_name.split("/")[-1])
        untar_dir.mkdir(parents=True, exist_ok=True)

        result = os.system(
            f"curl -s -L -H 'Accept: application/vnd.github+json' -H 'Authorization: Bearer {github_access_token}' -H 'X-GitHub-Api-Version: 2022-11-28' {url} | tar zx --strip-components 1 -C {untar_dir}"
        )
        if result != 0:
            raise Exception("Failed to download repository")
        return untar_dir
