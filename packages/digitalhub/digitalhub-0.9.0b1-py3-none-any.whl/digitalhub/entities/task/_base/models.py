from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class VolumeType(Enum):
    """
    Volume type.
    """

    PERSISTENT_VOLUME_CLAIM = "persistent_volume_claim"
    EMPTY_DIR = "empty_dir"


class Volume(BaseModel):
    """
    Volume model.
    """

    model_config = ConfigDict(use_enum_values=True)

    volume_type: VolumeType
    """Volume type."""

    name: str
    """Volume name."""

    mount_path: str
    """Volume mount path inside the container."""

    spec: dict[str, str] = None
    """Volume spec."""


class NodeSelector(BaseModel):
    """
    NodeSelector model.
    """

    key: str
    """Node selector key."""

    value: str
    """Node selector value."""


class ResourceItem(BaseModel):
    """
    Resource item model.
    """

    requests: str = Field(default=None, pattern=r"[\d]+|^([0-9])+([a-zA-Z])+$")
    """Resource requests."""

    limits: str = Field(default=None, pattern=r"[\d]+|^([0-9])+([a-zA-Z])+$")
    """Resource limits."""


class Resource(BaseModel):
    """
    Resource model.
    """

    cpu: ResourceItem = None
    """CPU resource model."""

    mem: ResourceItem = None
    """Memory resource model."""

    gpu: ResourceItem = None
    """GPU resource model."""


class Env(BaseModel):
    """
    Env variable model.
    """

    name: str
    """Env variable name."""

    value: str
    """Env variable value."""


class Toleration(BaseModel):
    """
    Toleration model.
    """

    key: str = None
    """Toleration key."""

    operator: str = None
    """Toleration operator."""

    value: str = None
    """Toleration value."""

    effect: str = None
    """Toleration effect."""

    toleration_seconds: int = None
    """Toleration seconds."""


class V1NodeSelectorRequirement(BaseModel):
    key: str
    operator: str
    values: list[str] = None


class V1NodeSelectorTerm(BaseModel):
    match_expressions: list[V1NodeSelectorRequirement] = None
    match_fields: list[V1NodeSelectorRequirement] = None


class V1NodeSelector(BaseModel):
    node_selector_terms: list[V1NodeSelectorTerm]


class V1PreferredSchedulingTerm(BaseModel):
    preference: V1NodeSelector
    weight: int


class V1LabelSelectorRequirement(BaseModel):
    key: str
    operator: str
    values: list[str] = None


class V1LabelSelector(BaseModel):
    match_expressions: list[V1LabelSelectorRequirement] = None
    match_labels: dict[str, str] = None


class V1PodAffinityTerm(BaseModel):
    label_selector: V1LabelSelector = None
    match_label_keys: list[str] = None
    mismatch_label_keys: list[str] = None
    namespace_selector: V1LabelSelector = None
    namespaces: list[str] = None
    topology_key: str


class V1WeightedPodAffinityTerm(BaseModel):
    pod_affinity_term: V1PodAffinityTerm
    weight: int


class V1NodeAffinity(BaseModel):
    preferred_during_scheduling_ignored_during_execution: list[V1PreferredSchedulingTerm] = None
    required_during_scheduling_ignored_during_execution: V1NodeSelector = None


class V1PodAffinity(BaseModel):
    preferred_during_scheduling_ignored_during_execution: list[V1WeightedPodAffinityTerm] = None
    required_during_scheduling_ignored_during_execution: list[V1PodAffinityTerm] = None


class V1PodAntiAffinity(BaseModel):
    preferred_during_scheduling_ignored_during_execution: list[V1WeightedPodAffinityTerm] = None
    required_during_scheduling_ignored_during_execution: list[V1PodAffinityTerm] = None


class Affinity(BaseModel):
    """
    Affinity model.
    """

    node_affinity: V1NodeAffinity = None
    """Node affinity."""

    pod_affinity: V1PodAffinity = None
    """Pod affinity."""

    pod_anti_affinity: V1PodAntiAffinity = None
    """Pod anti affinity."""


class K8s(BaseModel):
    """
    Kubernetes resource model.
    """

    node_selector: list[NodeSelector] = None
    """Node selector."""

    volumes: list[Volume] = None
    """List of volumes."""

    resources: Resource = None
    """Resources restrictions."""

    affinity: Affinity = None
    """Affinity."""

    tolerations: list[Toleration] = None
    """Tolerations."""

    envs: list[Env] = None
    """Env variables."""

    secrets: list[str] = None
    """List of secret names."""

    profile: str = None
    """Profile template."""

    runtime_class: str = None
    """Runtime class name."""

    priority_class: str = None
    """Priority class."""


class CorePort(BaseModel):
    """
    Port mapper model.
    """

    port: int
    target_port: int


class CoreServiceType(Enum):
    """
    CoreServiceType enum.
    """

    EXTERNAL_NAME = "ExternalName"
    CLUSTER_IP = "ClusterIP"
    NODE_PORT = "NodePort"
    LOAD_BALANCER = "LoadBalancer"
