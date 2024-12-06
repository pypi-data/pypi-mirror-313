#
# Copyright (c) 2022 PrajjuS <theprajjus@gmail.com>.
#
# This file is part of NoobStuffs
# (see http://github.com/PrajjuS/NoobStuffs).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from logging import getLogger

from github import Github, GithubException, InputGitAuthor, UnknownObjectException

LOGGER = getLogger("GithubHelper")


class GithubHelper:
    def __init__(self, gh_token: str, username: str, email: str):
        self.g = Github(login_or_token=gh_token)
        self.user = self.g.get_user()
        self.committer = InputGitAuthor(name=username, email=email)

    def cleanup_repo(self, repo: str):
        LOGGER.info(f"Cleaning up repo: {repo}")
        try:
            r = self.g.get_repo(full_name_or_id=repo)
            r.delete()
        except UnknownObjectException as e:
            LOGGER.error(f"Error while cleaning up repo {repo}: {e.data}")

    def fork_repo(self, repo: str):
        LOGGER.info(f"Forking repo: {repo}")
        try:
            r = self.g.get_repo(full_name_or_id=repo)
            return self.user.create_fork(repo=r)
        except GithubException as e:
            LOGGER.error(f"Error while forking repo {repo}: {e.data}")

    def empty_commit(self, repo: str, path: str, commit_message: str, branch: str):
        LOGGER.info(
            f"Committing changes in repo: repo={repo}, message={commit_message}, branch={branch}",
        )
        try:
            r = self.g.get_repo(full_name_or_id=repo)
            contents = r.get_contents(path)
            return r.update_file(
                path=contents.path,
                message=commit_message,
                content=contents.decoded_content.decode(),
                sha=contents.sha,
                branch=branch,
                committer=self.committer,
            )
        except GithubException as e:
            LOGGER.error(f"Error while committing changes in repo {repo}: {e.data}")

    def commit_changes(
        self,
        repo: str,
        path: str,
        commit_message: str,
        content: str,
        branch: str,
    ):
        LOGGER.info(
            f"Committing changes in repo: repo={repo}, file={path} content={content} message={commit_message}, branch={branch}",
        )
        try:
            r = self.g.get_repo(full_name_or_id=repo)
            contents = r.get_contents(path)
            return r.update_file(
                path=contents.path,
                message=commit_message,
                content=content,
                sha=contents.sha,
                branch=branch,
                committer=self.committer,
            )
        except GithubException as e:
            LOGGER.error(f"Error while committing changes in repo {repo}: {e.data}")
