from pydantic import BaseModel


class GitlabToken(BaseModel):

    value: str
    token_type: str = "PRIVATE-TOKEN"


class GitlabResource(BaseModel):

    name: str
    id: int


class GitlabReleaseAssetLink(BaseModel):

    name: str
    base_url: str
    url: str = ""
    archive_name: str = ""
    link_type: str = "package"
    direct_asset_path: str = "/"

    def model_post_init(self, __context):
        self.url = f"{self.base_url}/{self.name}"
        if self.archive_name:
            self.direct_asset_path += f"{self.archive_name}/"
            self.direct_asset_path += self.name


class GitlabReleaseAssetCollection(BaseModel):

    names: list[str] = []
    links: list[str] = []


class GitlabReleaseManifest(BaseModel):

    project_version: str
    base_url: str
    assets: GitlabReleaseAssetCollection
    name: str = ""
    tag_name: str = ""
    ref: str = "master"

    def model_post_init(self, __context):
        self.name = f"Release {self.project_version}"
        self.tag_name = f"v{self.project_version}"
        for name in self.assets.names:
            self.assets.links.append(GitlabReleaseAssetLink(name, self.base_url))


class GitlabRelease(BaseModel):

    manifest: GitlabReleaseManifest | None = None


class GitlabProject(GitlabResource):

    group_name: str = ""
    releases: list[GitlabRelease] = []


class GitlabGroup(GitlabResource):

    projects: list[GitlabProject] = []


class GitlabInstance:

    url: str
    groups: list[GitlabGroup]
    api_url: str = ""

    def model_post_init(self, __context):
        self.api_url = f"{self.url}/api/v4"
