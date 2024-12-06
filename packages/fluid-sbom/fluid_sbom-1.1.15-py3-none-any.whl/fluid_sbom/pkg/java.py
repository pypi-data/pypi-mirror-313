from pydantic import (
    BaseModel,
    Field,
)

from fluid_sbom.model.core import (
    Package,
    PackageType,
)
from fluid_sbom.utils.file import (
    Digest,
)

# List of Jenkins plugin group IDs
jenkins_plugin_pom_properties_group_ids = [
    "io.jenkins.plugins",
    "org.jenkins.plugins",
    "org.jenkins-ci.plugins",
    "io.jenkins-ci.plugins",
    "com.cloudbees.jenkins.plugins",
]


class KeyValue(BaseModel):
    key: str
    value: str


class JavaPomParent(BaseModel):
    group_id: str
    artifact_id: str
    version: str


class KeyValues(BaseModel):
    items: list[KeyValue] = Field(default_factory=list)

    def get(self, key: str) -> str | None:
        for item in self.items:  # pylint: disable=not-an-iterable
            if item.key == key:
                return item.value
        return None


class JavaPomProject(BaseModel):
    path: str | None = None
    group_id: str | None = None
    artifact_id: str | None = None
    version: str | None = None
    name: str | None = None
    parent: JavaPomParent | None = None
    description: str | None = None
    url: str | None = None


class JavaPomProperties(BaseModel):
    name: str | None = None
    group_id: str | None = None
    artifact_id: str | None = None
    version: str | None = None
    path: str | None = None
    scope: str | None = None
    extra: dict[str, str] = Field(default_factory=dict)

    def pkg_type_indicated(self) -> PackageType:
        # Check if the group ID indicates a Jenkins plugin
        if any(
            self.group_id and self.group_id.startswith(prefix)
            for prefix in jenkins_plugin_pom_properties_group_ids
        ) or (
            self.group_id and ".jenkins.plugin" in self.group_id  # pylint: disable=unsupported-membership-test
        ):
            return PackageType.JenkinsPluginPkg
        return PackageType.JavaPkg


class JavaManifest(BaseModel):
    main: dict[str, str]
    sections: list[dict[str, str]] | None = None


class JavaArchive(BaseModel):
    virtual_path: str | None = None
    manifest: JavaManifest | None = None
    pom_properties: JavaPomProperties | None = None
    pom_project: JavaPomProject | None = None
    archive_digests: list[Digest] = Field(default_factory=list)
    parent: Package | None = None
