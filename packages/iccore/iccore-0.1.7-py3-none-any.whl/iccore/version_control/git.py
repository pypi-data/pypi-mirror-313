import logging
from pathlib import Path

from pydantic import BaseModel

from iccore.system import process
from iccore.project import version

logger = logging.getLogger(__name__)


class GitUser(BaseModel):

    name: str = ""
    email: str = ""


class GitRemote(BaseModel):

    url: str = ""
    name: str = "origin"


class GitRepo(BaseModel):
    """
    Representation of a git repository, including methods for querying and modifying
    repo contents.
    """

    user: GitUser
    remotes: list[GitRemote] = []
    path: Path


def get_user_email(repo_dir: Path) -> str:
    cmd = "git config user.email"
    return process.run(cmd, repo_dir, is_read_only=True).strip()


def init_repo(repo_dir: Path) -> str:
    cmd = "git init ."
    return process.run(cmd, repo_dir)


def get_user_name(repo_dir: Path) -> str:
    cmd = "git config user.name"
    return process.run(cmd, repo_dir, is_read_only=True).strip()


def get_user(repo_dir: Path) -> GitUser:
    email = get_user_email(repo_dir)
    name = get_user_name(repo_dir)
    return GitUser(**{"name": name, "email": email})


def get_remotes(repo_dir: Path) -> list[GitRemote]:
    cmd = "git remote"
    remote_names = process.run(cmd, is_read_only=True).splitlines()
    remotes: list[GitRemote] = []
    for name in remote_names:
        remotes.append(GitRemote(**{"name": name}))
    return remotes


def get_repo_info(repo_dir: Path) -> GitRepo:
    return GitRepo(
        user=get_user(repo_dir), remotes=get_remotes(repo_dir), path=repo_dir
    )


def add_remote(repo_dir: Path, remote: GitRemote):
    logger.info("Adding remote with name %s and url %s", remote.name, remote.url)
    cmd = f"git remote add {remote.name} {remote.url}"
    process.run(cmd, repo_dir)


def get_changed_files(repo_dir: Path) -> list[str]:
    cmd = "git diff --name-only"
    result = process.run(cmd, repo_dir, is_read_only=True)
    return result.splitlines()


def has_tags(repo_dir: Path) -> bool:
    cmd = "git tag -l"
    # Result will be empty string if no tags
    return bool(process.run(cmd, repo_dir, is_read_only=True))


def get_latest_tag_on_branch(repo_dir: Path) -> str:
    if not has_tags(repo_dir):
        return ""

    cmd = "git describe --tags --abbrev=0"
    return process.run(cmd, repo_dir, is_read_only=True)


def get_branch(repo_dir: Path) -> str:
    cmd = "git branch --show-current"
    return process.run(cmd, repo_dir, is_read_only=True)


def push_tags(repo_dir: Path, remote: str = "origin"):
    cmd = f"git push --tags {remote}"
    process.run(cmd, repo_dir)


def set_tag(repo_dir: Path, tag: str):
    cmd = f"git tag {tag}"
    process.run(cmd, repo_dir)


def set_user_email(repo_dir: Path, email: str):
    cmd = f"git config user.email {email}"
    process.run(cmd, repo_dir)


def set_user_name(repo_dir: Path, name: str):
    cmd = f"git config user.name {name}"
    process.run(cmd, repo_dir)


def set_user(repo_dir: Path, user: GitUser):
    logger.info("Setting user name: %s and email: %s", user.email, user.name)
    set_user_email(repo_dir, user.email)
    set_user_name(repo_dir, user.name)


def add_all(repo_dir: Path):
    cmd = "git add ."
    process.run(cmd, repo_dir)


def commit(repo_dir: Path, message: str):
    cmd = f"git commit -m {message}"
    process.run(cmd, repo_dir)


def push(
    repo_dir: Path,
    remote: str = "origin",
    src: str = "HEAD",
    dst: str = "main",
    extra_args: str = "",
):
    cmd = f"git push {remote} {src}:{dst} {extra_args}"
    process.run(cmd, repo_dir)


def switch_branch(repo_dir: Path, target_branch: str):
    cmd = f"git checkout {target_branch}"
    return process.run(cmd, repo_dir)


def increment_tag(
    repo_dir: Path,
    version_scheme: str = "semver",
    field: str = "patch",
    branch="main",
    remote: str | None = None,
):

    current_branch = get_branch(repo_dir)
    if current_branch != branch:
        switch_branch(repo_dir, branch)

    latest_tag = get_latest_tag_on_branch(repo_dir)

    repo_version = version.parse(latest_tag, version_scheme)
    logging.info("Current tag is: %s", repo_version.as_string())

    repo_version.increment(field)
    logging.info("Updating tag to: %s", repo_version.as_string())
    set_tag(repo_dir, repo_version.as_string())

    if remote:
        working_remote = remote
    else:
        remotes = get_remotes(repo_dir)
        working_remote = remotes[-1].name
    logging.info("Setting remote to: %s", working_remote)
    push_tags(repo_dir, working_remote)
