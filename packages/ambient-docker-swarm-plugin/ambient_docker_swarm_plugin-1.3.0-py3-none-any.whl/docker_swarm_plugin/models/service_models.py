from typing import Dict, List, Optional

from ambient_backend_api_client import Service, ServiceNodeRelationship
from pydantic import BaseModel


class DockerServiceVersion(BaseModel):
    Index: int


class DockerServiceMount(BaseModel):
    Type: str
    Source: str
    Target: str


class DockerServiceContainerSpec(BaseModel):
    Image: str
    Args: List[str] = []
    Init: bool
    DNSConfig: Dict[str, str]
    Isolation: Optional[str] = None
    Env: List[str] = []
    Hostname: Optional[str] = None
    Mounts: List[DockerServiceMount] = []


class DockerServiceResources(BaseModel):
    Limits: Dict[str, str]
    Reservations: Dict[str, str]


class DockerServicePlacementPlatform(BaseModel):
    Architecture: Optional[str] = None
    OS: str


class DockerServicePlament(BaseModel):
    Platforms: List[DockerServicePlacementPlatform] = []


class DockerServiceTaskTemplate(BaseModel):
    ContainerSpec: DockerServiceContainerSpec
    Resources: DockerServiceResources
    Placement: DockerServicePlament
    ForceUpdate: int
    Runtime: str


class DockerServiceModeReplicated(BaseModel):
    Replicas: int


class DockerServiceMode(BaseModel):
    Replicated: DockerServiceModeReplicated


class DockerServicePort(BaseModel):
    Protocol: str
    TargetPort: int
    PublishedPort: int
    PublishMode: str


class DockerServiceEndpointSpec(BaseModel):
    Mode: Optional[str] = None
    Ports: List[DockerServicePort] = []


class DockerServiceEndpoint(BaseModel):
    Spec: DockerServiceEndpointSpec


class DockerServiceSpec(BaseModel):
    Name: str
    Labels: Dict[str, str]
    TaskTemplate: DockerServiceTaskTemplate
    Mode: DockerServiceMode
    EndpointSpec: DockerServiceEndpointSpec


class DockerServiceAttrs(BaseModel):
    ID: str
    Version: DockerServiceVersion
    CreatedAt: str
    UpdatedAt: str
    Spec: DockerServiceSpec
    Endpoint: DockerServiceEndpoint


class ServiceNodeRelationshipWithDockerAttrs(ServiceNodeRelationship):
    class Config:
        from_attributes = True

    docker_service_attrs: Optional[DockerServiceAttrs] = None


class ServiceWithDockerAttrs(Service):
    class Config:
        from_attributes = True

    docker_service_attrs: Optional[DockerServiceAttrs] = None


class SyncSurveyReport(BaseModel):
    """For all properties, True means the property is in sync,
    False means it is not in sync"""

    both_inputs_are_not_none: bool = False
    image_in_sync: bool = False
    ports_in_sync: bool = False
    replicas_in_sync: bool = False
    labels_in_sync: bool = False
    env_vars_in_sync: bool = False
    hostname_in_sync: bool = False
    mounts_in_sync: bool = False
    networks_in_sync: bool = True  # TODO: Implement network comparison

    @property
    def in_sync(self) -> bool:
        return all(
            [
                self.both_inputs_are_not_none,
                self.image_in_sync,
                self.ports_in_sync,
                self.replicas_in_sync,
                self.labels_in_sync,
                self.env_vars_in_sync,
                self.hostname_in_sync,
                self.mounts_in_sync,
                self.networks_in_sync,
            ]
        )
