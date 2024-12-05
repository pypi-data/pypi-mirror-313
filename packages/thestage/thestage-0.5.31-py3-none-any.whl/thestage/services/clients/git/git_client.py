import datetime

from pathlib import Path
from typing import Optional, List

import git
import typer
from git import Remote, Repo, GitCommandError, Commit
from rich import print
from thestage_core.services.filesystem_service import FileSystemServiceCore

from thestage.color_scheme.color_scheme import ColorScheme
from thestage.exceptions.git_access_exception import GitAccessException
from thestage.git.ProgressPrinter import ProgressPrinter


class GitLocalClient:
    __base_name_remote: str = 'origin'
    __base_name_local: str = 'main'
    __git_ignore_thestage_line: str = '/.thestage/'

    __special_main_branches = ['main', 'master']

    __base_git_url: str = 'https://github.com/'

    def __init__(
            self,
            file_system_service: FileSystemServiceCore,
    ):
        self.__file_system_service = file_system_service

    def __get_repo(self, path: str) -> Repo:
        return git.Repo(path)

    def is_present_local_git(self, path: str) -> bool:
        git_path = self.__file_system_service.get_path(path)
        if not git_path.exists():
            return False

        git_path = git_path.joinpath('.git')
        if not git_path.exists():
            return False

        result = git.repo.base.is_git_dir(git_path)
        return result

    def get_remote(self, path: str) -> Optional[List[Remote]]:
        is_git_repo = self.is_present_local_git(path=path)
        if is_git_repo:
            repo = git.Repo(path)
            remotes: Optional[List[Remote]] = list(repo.remotes) if repo.remotes else []
            return remotes
        return None

    def has_remote(self, path: str) -> bool:
        remotes: Optional[List[Remote]] = self.get_remote(path)
        return True if remotes is not None and len(remotes) > 0 else False

    def has_changes_with_untracked(self, path: str) -> bool:
        repo = self.__get_repo(path=path)
        return repo.is_dirty(untracked_files=True)

    def init_repository(
            self,
            path: str,
    ) -> Optional[Repo]:

        repo = git.Repo.init(path)
        if repo:
            # default git name master, rename to main - sync wih github
            repo.git.branch("-M", self.__base_name_local)
        return repo

    def add_remote_to_repo(
            self,
            path: str,
            remote_url: str,
            remote_name: str,
    ) -> bool:
        repo = self.__get_repo(path=path)
        remotes: List[Remote] = repo.remotes
        not_present = True
        if remotes:
            item = list(filter(lambda x: x.name == remote_name, remotes))
            if len(item) > 0:
                not_present = False

        if not_present:
            remote: Remote = repo.create_remote(
                name=self.__base_name_remote,
                url=remote_url,
            )
            if remote:
                return True
            else:
                return False
        else:
            return True

    def git_fetch(self, path: str, deploy_key_path: str):
        repo = self.__get_repo(path=path)
        git_ssh_cmd = 'ssh -F /dev/null -o StrictHostKeyChecking=no -o IdentitiesOnly=yes -i %s' % deploy_key_path

        with repo.git.custom_environment(GIT_SSH_COMMAND=git_ssh_cmd):
            remote: Remote = repo.remote(self.__base_name_remote)
            if remote:
                try:
                    remote.fetch()
                except GitCommandError as base_ex:
                    msg = base_ex.stderr
                    if msg and 'fatal: Could not read from remote repository' in msg:
                        raise GitAccessException(
                            message='You dont have access to repository, or repository not found.',
                            url=self.build_http_repo_url(git_path=remote.url),
                            dop_message=msg,
                        )
                    else:
                        raise base_ex

    def git_pull(self, path: str, deploy_key_path: str, branch: Optional[str] = None):
        repo = self.__get_repo(path=path)
        git_ssh_cmd = 'ssh -F /dev/null -o StrictHostKeyChecking=no -o IdentitiesOnly=yes -i %s' % deploy_key_path

        with repo.git.custom_environment(GIT_SSH_COMMAND=git_ssh_cmd):
            local_branch = self.__base_name_local
            if branch:
                if self.__base_name_remote in branch:
                    local_branch = branch.replace(f"{self.__base_name_remote}/", '').strip()
                else:
                    local_branch = branch

            repo.git.pull(self.__base_name_remote, local_branch)

    def find_main_branch_name(self, path: str) -> Optional[str]:
        repo = self.__get_repo(path=path)
        if repo:
            for branch in [head.name for head in repo.heads]:
                if branch in self.__special_main_branches:
                    return branch
        return None

    def get_active_branch_name(self, path: str) -> Optional[str]:
        repo = self.__get_repo(path=path)
        if repo:
            if repo.head.is_detached:
                return None
            return repo.active_branch.name
        return None

    def git_checkout_to_branch(self, path: str, branch: str):
        repo = self.__get_repo(path=path)
        if repo:
            repo.git.checkout(branch.strip())

    def git_checkout_to_commit(self, path: str, commit_hash: str = None) -> bool:
        repo = self.__get_repo(path=path)
        if repo:
            if is_commit_exists(repo, commit_hash):
                repo.git.checkout(commit_hash.strip())
                return True
            else:
                typer.echo(f"Could not checkout to commit {commit_hash} - reference not found in repository")
        return False

    def build_http_repo_url(self, git_path: str) -> str:
        start_path_pos = git_path.find(":")
        pre_url = git_path[start_path_pos + 1:]
        url = pre_url.replace('.git', '')
        return self.__base_git_url + url

    def clone(self, url: str, path: str, deploy_key_path: str) -> Optional[Repo]:
        try:
            git_ssh_cmd = 'ssh -F /dev/null -o StrictHostKeyChecking=no -o IdentitiesOnly=yes -i %s' % deploy_key_path
            return Repo.clone_from(url=url, to_path=path, env={"GIT_SSH_COMMAND": git_ssh_cmd})
        except GitCommandError as base_ex:
            msg = base_ex.stderr
            if msg and 'Repository not found' in msg and 'correct access rights' in msg:
                raise GitAccessException(
                    message='You dont have access to repository, or repository not found.',
                    url=self.build_http_repo_url(git_path=url),
                    dop_message=msg,
                )
            else:
                raise base_ex

    def commit_local_changes(
            self,
            path: str,
            name: Optional[str] = None,
    ) -> Optional[str]:
        repo = self.__get_repo(path=path)
        if repo.head.is_detached:
            line_color = ColorScheme.GIT_HEADLESS
            print(f'[{line_color}]Committing in detached head state at {repo.head.commit.hexsha}[/{line_color}]')
        commit_name = name if name else f"Auto commit {str(datetime.datetime.now().date())}"
        commit = repo.git.commit('--all', '--allow-empty', '-m', commit_name, )
        return commit

    def push_changes(
            self,
            path: str,
            deploy_key_path: str
    ):
        repo = self.__get_repo(path=path)
        git_ssh_cmd = 'ssh -F /dev/null -o StrictHostKeyChecking=no -o IdentitiesOnly=yes -i %s' % deploy_key_path

        with repo.git.custom_environment(GIT_SSH_COMMAND=git_ssh_cmd):
            origin = repo.remote(self.__base_name_remote)
            if origin:
                progress = ProgressPrinter()
                # repo.git.push(origin.name, repo.active_branch.name)
                try:
                    origin.push(refspec=repo.active_branch.name, progress=progress).raise_if_error()
                except GitCommandError as ex:
                    for line in progress.allDroppedLines():
                        # returning the whole output if failed - so that user have any idea what's going on
                        print(f'>> {line}')
                    raise ex

    def get_current_commit(self, path: str,) -> Optional[Commit]:
        repo = self.__get_repo(path=path)
        if repo:
            return repo.head.commit
        else:
            return None

    def get_commit_by_hash(self, path: str, commit_hash: str) -> Optional[Commit]:
        repo = self.__get_repo(path=path)
        if repo:
            return repo.commit(commit_hash)
        else:
            return None

    def _get_gitignore_path(self, path: str) -> Path:
        git_path = self.__file_system_service.get_path(path)
        return git_path.joinpath('.gitignore')

    def git_add_by_path(self, repo_path: str, file_path: str):
        repo = self.__get_repo(path=repo_path)
        if repo:
            repo.index.add(items=[file_path])

    def git_add_all(self, repo_path: str):
        repo = self.__get_repo(path=repo_path)
        if repo:
            repo.git.add(all=True)

    def git_diff_stat(self, repo_path: str) -> str:
        repo = self.__get_repo(path=repo_path)
        if repo:
            try:
                diff: str = repo.git.diff(repo.head.commit.tree, "--stat")
                return diff.splitlines()[-1]
            except ValueError as e:
                return str(e)

    def init_gitignore(self, path: str):
        gitignore_path = self._get_gitignore_path(path=path)
        if not gitignore_path.exists():
            self.__file_system_service.create_if_not_exists_file(gitignore_path)
            self.git_add_by_path(repo_path=path, file_path=str(gitignore_path))

        is_present_tsr = self.__file_system_service.find_in_text_file(file=str(gitignore_path),
                                                                      find=self.__git_ignore_thestage_line)
        if not is_present_tsr:
            self.__file_system_service.add_line_to_text_file(file=str(gitignore_path),
                                                             new_line=self.__git_ignore_thestage_line)

    def is_head_detached(self, path: str) -> bool:
        repo = self.__get_repo(path=path)
        if repo:
            return repo.head.is_detached

    def reset_hard(self, path: str):
        repo = self.__get_repo(path=path)
        if repo:
            repo.git.reset('--hard')

    # refers to a "headless commit" where something was committed while in detached head state and head is pointing at that commit
    def is_head_committed_in_headless_state(self, path: str) -> bool:
        repo = self.__get_repo(path=path)
        if repo:
            commit = repo.head.commit
            for branch in repo.heads:
                for commit_item in repo.iter_commits(branch):
                    if commit_item.hexsha == commit.hexsha:
                        return False
        return True

    def is_branch_exists(self, path: str, branch_name: str) -> bool:
        repo = self.__get_repo(path=path)
        if repo:
            for branch in repo.heads:
                if branch.name == branch_name:
                    return True
        return False

    def checkout_to_new_branch(self, path: str, branch_name: str):
        repo = self.__get_repo(path=path)
        if repo:
            repo.git.checkout("-b", branch_name)


def is_commit_exists(repo, commit_sha) -> bool:
    try:
        repo.commit(commit_sha)
        return True
    except ValueError:
        return False
