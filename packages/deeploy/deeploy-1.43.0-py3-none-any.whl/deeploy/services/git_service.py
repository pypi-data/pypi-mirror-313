class GitService(object):
    """
    A class for interacting with a local Git project
    """

    def __init__(self, local_repository_path: str) -> None:
        """Initialise the Git client"""
        from git import Remote, Repo

        self.repository: Repo = Repo(local_repository_path)
        self.branch_name = self.repository.active_branch.name
        self.commit = self.repository.head.commit.hexsha
        self.remote: Remote = self.repository.remote("origin")

        if not self.__is_valid_git_project():
            raise Exception("Not a valid git project")

    def get_remote_url(self) -> str:
        return self.remote.url

    def get_branch_name(self) -> str:
        return self.branch_name

    def get_commit(self) -> str:
        return self.commit

    def __is_valid_git_project(self) -> bool:
        """Check if the supplied repository is valid"""
        return not self.repository.bare
