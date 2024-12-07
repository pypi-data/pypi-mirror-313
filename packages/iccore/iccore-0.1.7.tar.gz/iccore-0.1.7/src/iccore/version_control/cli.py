import json
import logging
import os
from pathlib import Path

from iccore.serialization import write_json
from iccore.filesystem import write_file
from iccore.cli_utils import launch_common
from iccore.version_control import git

from .gitlab_client import GitlabClient
from .gitlab import GitlabToken, GitlabInstance


logger = logging.getLogger(__name__)


def get_milestones(args):
    launch_common(args)

    logger.info("Fetching milestones for %s %s", args.resource_type, args.resource_id)

    token = GitlabToken(args.token, args.token_type)
    instance = GitlabInstance(args.url)
    gitlab = GitlabClient(instance, token)

    milestones = gitlab.get_milestones(args.resource_id, args.resource_type)
    output = [m.serialize() for m in milestones]
    output_json = json.dumps(output, indent=4)

    if args.output:
        write_json(output_json, args.output)
    else:
        print(output_json)

    logger.info("Finished fetching milestones")


def get_latest_release(args):
    launch_common(args)

    logger.info("Getting latest release for project %s", args.project_id)
    token = GitlabToken(args.token, args.token_type)
    instance = GitlabInstance(args.url)
    gitlab = GitlabClient(instance, token)

    version = gitlab.get_latest_release(
        args.project_id, args.asset_name, args.download_dir
    )
    if version:
        print(version)

    logger.info("Finished getting latest release")


def get_git_info(args):
    repo = git.get_repo_info(args.repo_dir.resolve())
    repo_json = repo.model_dump_json(indent=4)
    write_file(args.output_path.resolve(), repo_json)


def setup_gitlab_parsers(subparsers):
    gitlab_parser = subparsers.add_parser("gitlab")

    gitlab_parser.add_argument(
        "--token",
        type=str,
        default="",
        help="Access token for the Gitlab resource - if required",
    )
    gitlab_parser.add_argument(
        "--token_type",
        type=str,
        help="Type of token - corresponding to the header key in http requests",
        default="PRIVATE-TOKEN",
    )
    gitlab_parser.add_argument(
        "--url",
        type=str,
        help="URL for the Gitlab repo instance",
        default="https://git.ichec.ie",
    )

    gitlab_subparsers = gitlab_parser.add_subparsers(required=True)

    milestones_subparser = gitlab_subparsers.add_parser("milestone")
    milestones_subparser.add_argument(
        "resource_id", type=int, help="Id of the group or project being queried"
    )
    milestones_subparser.add_argument(
        "--resource_type",
        type=str,
        default="project",
        help="Whether to query 'project' or 'group' milestones",
    )
    milestones_subparser.add_argument(
        "--output",
        type=str,
        default="",
        help="Path to output, if not given the output is dumped to terminal",
    )
    milestones_subparser.set_defaults(func=get_milestones)

    latest_release_parser = gitlab_subparsers.add_parser("latest_release")
    latest_release_parser.add_argument(
        "project_id", type=int, help="Id of the project being queried"
    )
    latest_release_parser.add_argument(
        "--asset_name", type=str, help="Name of a release asset to download", default=""
    )
    latest_release_parser.add_argument(
        "--download_dir",
        type=Path,
        help="Directory to download release assets to",
        default=Path(os.getcwd()),
    )
    latest_release_parser.set_defaults(func=get_latest_release)


def setup_git_parsers(subparsers):
    git_parser = subparsers.add_parser("git")

    git_subparsers = git_parser.add_subparsers(required=True)

    info_subparser = git_subparsers.add_parser("info")
    info_subparser.add_argument(
        "--repo_dir", type=Path, default=Path(os.getcwd()), help="Path to the repo"
    )
    info_subparser.add_argument(
        "--output_path",
        type=Path,
        default=Path(os.getcwd()) / "repo_info.json",
        help="Path to the output",
    )
    info_subparser.set_defaults(func=get_git_info)


def setup_version_control_parsers(subparsers):

    setup_gitlab_parsers(subparsers)
    setup_git_parsers(subparsers)
