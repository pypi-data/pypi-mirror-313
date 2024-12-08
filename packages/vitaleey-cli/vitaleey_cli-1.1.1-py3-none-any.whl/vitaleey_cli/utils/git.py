import os

import gitlab
from dateutil import parser

from vitaleey_cli.config import gitlab_config


class GitException(Exception):
    pass


class Git:
    """
    Git class to interact with git commands
    """

    def __init__(self):
        self.config = gitlab_config()
        self._gl = None
        self._repo = None

    @staticmethod
    def get_local_repo_url():
        return os.popen("git config --get remote.origin.url").read().strip()

    def is_repo_part_of(self, group):
        _, repo = self.get_local_repo_url().split(":", 1)
        if not repo.startswith(group.lower()):
            group_namespace = "vitaleey"
            if group_namespace is None or group_namespace.lower() != group.lower():
                return False
        return True

    @property
    def branch(self):
        branch = self.config.branch
        if not branch:
            raise GitException("Branch not found")
        return branch

    @property
    def gl(self):
        if self._gl is None:
            self._gl = gitlab.Gitlab(private_token=self.config.private_token)
        return self._gl

    @property
    def project_id(self):
        project_id = self.config.project_id

        if not project_id:
            raise GitException("Project ID not found")
        return project_id

    @property
    def repo(self):
        if self._repo is None:
            self._repo = self.gl.projects.get(self.project_id)
        return self._repo

    def new_version(self, version):
        old_tag = self.latest_tag()
        self.delete_tag(old_tag)
        commit = self.commit(f"Release version {version} [skip ci]")
        self.tag(version, commit.id)

    def tag(self, tag, commit):
        return self.repo.tags.create({"tag_name": tag, "ref": commit})

    def commit(self, message):
        filename = "pyproject.toml"
        return self.repo.commits.create(
            {
                "branch": self.branch,
                "commit_message": message,
                "author_name": "Vitaleey CLI",
                "author_email": "admin@vitaleey.com",
                "actions": [
                    {
                        "action": "update",
                        "file_path": filename,
                        "content": open(os.path.join(os.getcwd(), filename)).read(),
                    }
                ],
            }
        )

    def delete_tag(self, tag):
        return self.repo.tags.delete(tag)

    def latest_commit(self):
        return self.repo.commits.list(ref_name=self.branch, all=True)[0].short_id

    def latest_tag(self):
        tags = self.repo.tags.list()
        newest_tag = None
        newest_date = None

        for tag in tags:
            created_at = parser.parse(tag.commit["created_at"])

            if newest_date is None or created_at > newest_date:
                newest_date = created_at
                newest_tag = tag

        if newest_tag:
            return newest_tag.name


git = Git()
