import re
import subprocess
from datetime import datetime
from json import loads as json_loads
from typing import Optional, TypeVar, Type, List, Union, Mapping

from pydantic import BaseModel


class CLIMigratePlan(BaseModel):
    migrationId: str
    estimatedDataDropped: int
    estimatedSampleTuples: int
    estimatedTimeSeconds: float


class CLIMigrationResult(BaseModel):
    storedOnline: int
    storedOffline: int
    computed: int
    dropped: int
    failed: int
    totalDurationS: float


class CLIResolverMigrationProgress(BaseModel):
    resolverFqn: str
    displayName: str
    progress: float
    result: CLIMigrationResult


class CLIMigrateResponse(BaseModel):
    status: str
    progress: List[CLIResolverMigrationProgress]


class CLIInitResponse(BaseModel):
    config: str
    created_project: bool
    created_ignore: bool


class CLISql(BaseModel):
    token: str


class CLIDashboard(BaseModel):
    url: str


class CLIEnvironmentSettings(BaseModel):
    runtime: Optional[str]
    requirements: Optional[str]
    dockerfile: Optional[str]


class CLIProjectSettings(BaseModel):
    project: str
    environments: Mapping[str, CLIEnvironmentSettings]


class CLIJWT(BaseModel):
    value: Optional[str]
    ValidUntil: Optional[datetime]


class CLITokenConfig(BaseModel):
    name: str
    clientId: str
    clientSecret: str
    validUntil: str
    apiServer: str
    activeEnvironment: str
    jwt: Optional[CLIJWT]


class CLIVersion(BaseModel):
    version: str
    platform: str
    sha1: str
    at: datetime


class CLIWhoAmI(BaseModel):
    user: str


class CLIToken(BaseModel):
    token: str


class CLIDeploymentComplete(BaseModel):
    id: str
    creator: str
    environmentId: str
    status: str
    isPreview: bool


class CLIApply(BaseModel):
    deployment_id: str
    deployment_url: str
    status: str
    response: Optional[CLIDeploymentComplete]


class CLIEnvironment(BaseModel):
    projectId: str
    name: str
    id: str


T = TypeVar("T")


class ChalkCLIHarness:
    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        environment: Optional[str] = None,
        json: bool = True,
        dry: bool = False,
        chalk_executable: str = "chalk",
    ):
        self._client_id = client_id
        self._client_secret = client_secret
        self._environment = environment
        self._json = json
        self._dry = dry
        self._chalk_executable = chalk_executable

    def _chalk_string(self, *args, **kwargs):
        all_kwargs = dict(
            client_id=self._client_id,
            client_secret=self._client_secret,
            environment=self._environment,
            json=self._json,
        )
        all_kwargs.update(kwargs)

        def format_key(k: str) -> str:
            return re.sub("_", "-", k.removesuffix("_"))

        kwarg_cli = [
            f"--{format_key(k)}={v}" if v is not True else f"--{format_key(k)}"
            for k, v in all_kwargs.items()
            if v is not None
        ]
        command = [self._chalk_executable, *args, *kwarg_cli]
        if self._dry:
            print(command)
            return command

        return subprocess.check_output(command).decode("UTF-8")

    def _chalk_json(self, model: Type[T], *args, **kwargs) -> Union[T, List[T]]:
        output = self._chalk_string(*args, **kwargs)
        if self._dry:
            return output
        j = json_loads(output)
        if isinstance(j, list):
            return [model.parse_obj(x) for x in j]
        return model.parse_obj(j)

    def apply_await(
            self,
            force: Optional[bool] = None,
            no_promote: Optional[bool] = None,
    ) -> CLIApply:
        return self._chalk_json(CLIApply, "apply", await_=True, force=force, no_promote=no_promote)

    def version(self) -> CLIVersion:
        return self._chalk_json(CLIVersion, "version")

    def version_tag_only(self) -> str:
        return self._chalk_string("version", tag_only=True)

    def dashboard(self) -> CLIDashboard:
        return self._chalk_json(CLIDashboard, "dashboard")

    def whoami(self) -> CLIWhoAmI:
        return self._chalk_json(CLIWhoAmI, "whoami")

    def token(self) -> CLIToken:
        return self._chalk_json(CLIToken, "token")

    def environments(self) -> List[CLIEnvironment]:
        return self._chalk_json(CLIEnvironment, "environment")

    def set_environment(self, environment: str) -> CLIEnvironment:
        return self._chalk_json(CLIEnvironment, "environment", environment)

    def config(self) -> CLITokenConfig:
        return self._chalk_json(CLITokenConfig, "config")

    def project(self) -> CLIProjectSettings:
        return self._chalk_json(CLIProjectSettings, "project")

    def init(self, template: Optional[str] = None) -> CLIInitResponse:
        return self._chalk_json(CLIInitResponse, "init", template=template)

    def sql(self) -> CLISql:
        return self._chalk_json(CLISql, "sql")

    def migrate(
        self,
        resolver: str,
        parallelism: Optional[int] = None,
        max_samples: Optional[int] = None,
        sampling_strategy: str = "all",  # most-recent also valid
        sample: Optional[str] = None,
        persist_online: bool = True,
        persist_offline: bool = True,
        drop_resolver_data: Optional[bool] = None,
    ) -> CLIMigrateResponse:
        return self._chalk_json(
            CLIMigrateResponse,
            "migrate",
            resolver=resolver,
            parallelism=parallelism,
            max_samples=max_samples,
            sampling_strategy=sampling_strategy,
            sample=sample,
            persist_online=persist_online,
            persist_offline=persist_offline,
            drop_resolver_data=drop_resolver_data,
        )

    def migrate_plan(
        self,
        resolver: str,
        parallelism: Optional[int] = None,
        max_samples: Optional[int] = None,
        sampling_strategy: str = "all",  # most-recent also valid
        sample: Optional[str] = None,
        persist_online: bool = True,
        persist_offline: bool = True,
        drop_resolver_data: Optional[bool] = None,
    ) -> CLIMigratePlan:
        return self._chalk_json(
            CLIMigratePlan,
            "migrate",
            plan=True,
            resolver=resolver,
            parallelism=parallelism,
            max_samples=max_samples,
            sampling_strategy=sampling_strategy,
            sample=sample,
            persist_online=persist_online,
            persist_offline=persist_offline,
            drop_resolver_data=drop_resolver_data,
        )
