import json
from typing import Optional, ClassVar, Dict, List, Tuple, Type, Any


import math
from attr import field, define

from fix_plugin_aws.aws_client import AwsClient
from fix_plugin_aws.resource.base import AwsApiSpec, GraphBuilder, AwsResource
from fix_plugin_aws.resource.kms import AwsKmsKey
from fix_plugin_aws.utils import ToDict
from fixlib.baseresources import HasResourcePolicy, ModelReference, BaseNetworkShare, PolicySource, PolicySourceKind
from fixlib.graph import Graph
from fixlib.json import sort_json
from fixlib.json_bender import Bender, S, F, Bend
from fixlib.types import Json

service_name = "efs"


class EfsTaggable:
    def update_resource_tag(self, client: AwsClient, key: str, value: str) -> bool:
        client.call(
            aws_service=service_name,
            action="tag-resource",
            result_name=None,
            resourceId=self.id,  # type: ignore
            tags={key: value},
        )
        return True

    def delete_resource_tag(self, client: AwsClient, key: str) -> bool:
        client.call(
            aws_service=service_name,
            action="untag-resource",
            result_name=None,
            resourceId=self.id,  # type: ignore
            tagKeys=[key],
        )
        return True

    @classmethod
    def called_mutator_apis(cls) -> List[AwsApiSpec]:
        return [
            AwsApiSpec(service_name, "tag-resource", override_iam_permission="elasticfilesystem:TagResource"),
            AwsApiSpec(service_name, "untag-resource", override_iam_permission="elasticfilesystem:UntagResource"),
        ]


@define(eq=False, slots=False)
class AwsEfsMountTarget(AwsResource):
    kind: ClassVar[str] = "aws_efs_mount_target"
    _kind_display: ClassVar[str] = "AWS EFS Mount Target"
    _kind_description: ClassVar[str] = "An AWS EFS Mount Target is a network interface in a Virtual Private Cloud (VPC) subnet that connects to an Elastic File System (EFS). It provides an IP address for accessing the file system within the VPC. Mount targets act as endpoints for NFS clients to connect and mount EFS file systems on EC2 instances."  # fmt: skip
    _docs_url: ClassVar[str] = "https://docs.aws.amazon.com/efs/latest/ug/mounting-fs-mount-cmd-general.html"
    _kind_service: ClassVar[Optional[str]] = service_name
    _metadata: ClassVar[Dict[str, Any]] = {"icon": "config", "group": "storage"}
    _aws_metadata: ClassVar[Dict[str, Any]] = {"provider_link_tpl": None, "arn_tpl": "arn:{partition}:efs:{region}:{account}:mount-target/{id}"}  # fmt: skip
    mapping: ClassVar[Dict[str, Bender]] = {
        "id": S("MountTargetId"),
        "owner_id": S("OwnerId"),
        "life_cycle_state": S("LifeCycleState"),
        "ip_address": S("IpAddress"),
        "availability_zone_name": S("AvailabilityZoneName"),
    }
    _reference_kinds: ClassVar[ModelReference] = {"predecessors": {"default": ["aws_ec2_network_interface"]}}
    owner_id: Optional[str] = field(default=None)
    life_cycle_state: Optional[str] = field(default=None)
    ip_address: Optional[str] = field(default=None)
    availability_zone_name: Optional[str] = field(default=None)

    def connect_in_graph(self, builder: GraphBuilder, source: Json) -> None:
        if nic_id := source.get("NetworkInterfaceId"):
            builder.dependant_node(self, reverse=True, kind="aws_ec2_network_interface", id=nic_id)


@define(eq=False, slots=False)
class AwsEfsFileSystem(EfsTaggable, AwsResource, BaseNetworkShare, HasResourcePolicy):
    kind: ClassVar[str] = "aws_efs_file_system"
    _kind_display: ClassVar[str] = "AWS EFS File System"
    _aws_metadata: ClassVar[Dict[str, Any]] = {"provider_link_tpl": "https://{region_id}.console.aws.amazon.com/efs/home?region={region}#/file-systems/{FileSystemId}", "arn_tpl": "arn:{partition}:efs:{region}:{account}:file-system/{id}"}  # fmt: skip
    _kind_description: ClassVar[str] = "AWS EFS (Elastic File System) is a cloud-based network file storage service for Amazon EC2 instances. It provides a shared file system that can be accessed by multiple EC2 instances simultaneously. EFS automatically scales storage capacity as files are added or removed, and users pay only for the storage they use."  # fmt: skip
    _docs_url: ClassVar[str] = "https://docs.aws.amazon.com/efs/latest/ug/"
    _kind_service: ClassVar[Optional[str]] = service_name
    api_spec: ClassVar[AwsApiSpec] = AwsApiSpec(
        service_name,
        "describe-file-systems",
        "FileSystems",
        override_iam_permission="elasticfilesystem:DescribeFileSystems",
    )
    mapping: ClassVar[Dict[str, Bender]] = {
        "id": S("FileSystemId"),
        "tags": S("Tags", default=[]) >> ToDict(),
        "name": S("Name"),
        "ctime": S("CreationTime"),
        "owner_id": S("OwnerId"),
        "creation_token": S("CreationToken"),
        "arn": S("FileSystemArn"),
        "share_status": S("LifeCycleState"),
        "share_size": S("SizeInBytes", "Value") >> F(lambda x: math.ceil(x / 1024**3)),
        "share_encrypted": S("Encrypted"),
        "share_throughput": S("ProvisionedThroughputInMibps") >> F(lambda x: x * 1024**2),
        "provisioned_throughput_in_mibps": S("ProvisionedThroughputInMibps"),
        "number_of_mount_targets": S("NumberOfMountTargets"),
        "performance_mode": S("PerformanceMode"),
        "throughput_mode": S("ThroughputMode"),
        "availability_zone_name": S("AvailabilityZoneName"),
    }
    _reference_kinds: ClassVar[ModelReference] = {"successors": {"default": ["aws_kms_key"]}}
    owner_id: Optional[str] = field(default=None)
    creation_token: Optional[str] = field(default=None)
    number_of_mount_targets: Optional[int] = field(default=None)
    performance_mode: Optional[str] = field(default=None)
    throughput_mode: Optional[str] = field(default=None)
    provisioned_throughput_in_mibps: Optional[float] = field(default=None)
    availability_zone_name: Optional[str] = field(default=None)
    file_system_policy: Optional[Json] = field(default=None)

    def resource_policy(self, builder: Any) -> List[Tuple[PolicySource, Dict[str, Any]]]:
        if not self.file_system_policy or not self.arn:
            return []

        return [(PolicySource(PolicySourceKind.resource, self.arn), self.file_system_policy)]

    @classmethod
    def called_collect_apis(cls) -> List[AwsApiSpec]:
        return [
            cls.api_spec,
            AwsApiSpec(
                service_name, "describe-mount-targets", override_iam_permission="elasticfilesystem:DescribeMountTargets"
            ),
            AwsApiSpec(
                service_name,
                "describe-file-system-policy",
                override_iam_permission="elasticfilesystem:DescribeFileSystemPolicy",
            ),
        ]

    @classmethod
    def collect(cls: Type[AwsResource], js_list: List[Json], builder: GraphBuilder) -> None:
        def collect_mount_points(fs: AwsEfsFileSystem) -> None:
            for mt_raw in builder.client.list(
                service_name, "describe-mount-targets", "MountTargets", FileSystemId=fs.id
            ):
                if mt := AwsEfsMountTarget.from_api(mt_raw, builder):
                    builder.add_node(mt, mt_raw)
                    builder.add_edge(fs, node=mt)

        def fetch_file_system_policy(fs: AwsEfsFileSystem) -> None:
            with builder.suppress("describe-file-system-policy"):
                if policy := builder.client.get(
                    service_name,
                    "describe-file-system-policy",
                    "Policy",
                    FileSystemId=fs.id,
                    expected_errors=["PolicyNotFound", "FileSystemNotFound"],
                ):
                    fs.file_system_policy = sort_json(json.loads(policy), sort_list=True)  # type: ignore

        for js in js_list:
            if instance := cls.from_api(js, builder):
                builder.add_node(instance, js)
                builder.submit_work(service_name, collect_mount_points, instance)
                builder.submit_work(service_name, fetch_file_system_policy, instance)

    def connect_in_graph(self, builder: GraphBuilder, source: Json) -> None:
        if kms_key_id := source.get("KmsKeyId"):
            builder.dependant_node(from_node=self, clazz=AwsKmsKey, id=AwsKmsKey.normalise_id(kms_key_id))

    def delete_resource(self, client: AwsClient, graph: Graph) -> bool:
        client.call(service_name, "delete-file-system", FileSystemId=self.id)
        return True

    @classmethod
    def called_mutator_apis(cls) -> List[AwsApiSpec]:
        return [
            AwsApiSpec(service_name, "delete-file-system", override_iam_permission="elasticfilesystem:DeleteFileSystem")
        ]


@define(eq=False, slots=False)
class AwsEfsPosixUser:
    kind: ClassVar[str] = "aws_efs_posix_user"
    kind_display: ClassVar[str] = "AWS EFS POSIX User"
    kind_description: ClassVar[str] = (
        "EFS POSIX Users are user accounts that can be used to access and manage"
        " files in Amazon Elastic File System (EFS) using POSIX permissions."
    )
    mapping: ClassVar[Dict[str, Bender]] = {
        "uid": S("Uid"),
        "gid": S("Gid"),
        "secondary_gids": S("SecondaryGids", default=[]),
    }
    uid: Optional[int] = field(default=None)
    gid: Optional[int] = field(default=None)
    secondary_gids: List[int] = field(factory=list)


@define(eq=False, slots=False)
class AwsEfsCreationInfo:
    kind: ClassVar[str] = "aws_efs_creation_info"
    kind_display: ClassVar[str] = "AWS EFS Creation Info"
    kind_description: ClassVar[str] = (
        "EFS Creation Info is a parameter used in AWS to provide information for"
        " creating an Amazon Elastic File System (EFS) resource."
    )
    mapping: ClassVar[Dict[str, Bender]] = {
        "owner_uid": S("OwnerUid"),
        "owner_gid": S("OwnerGid"),
        "permissions": S("Permissions"),
    }
    owner_uid: Optional[int] = field(default=None)
    owner_gid: Optional[int] = field(default=None)
    permissions: Optional[str] = field(default=None)


@define(eq=False, slots=False)
class AwsEfsRootDirectory:
    kind: ClassVar[str] = "aws_efs_root_directory"
    kind_display: ClassVar[str] = "AWS EFS Root Directory"
    kind_description: ClassVar[str] = (
        "The root directory of an Amazon Elastic File System (EFS) provides a common"
        " entry point for accessing all files and directories within the file system."
    )
    mapping: ClassVar[Dict[str, Bender]] = {
        "path": S("Path"),
        "creation_info": S("CreationInfo") >> Bend(AwsEfsCreationInfo.mapping),
    }
    path: Optional[str] = field(default=None)
    creation_info: Optional[AwsEfsCreationInfo] = field(default=None)


@define(eq=False, slots=False)
class AwsEfsAccessPoint(AwsResource, EfsTaggable):
    kind: ClassVar[str] = "aws_efs_access_point"
    _kind_display: ClassVar[str] = "AWS EFS Access Point"
    _kind_description: ClassVar[str] = "AWS EFS Access Point is a feature of Amazon Elastic File System that creates a unique entry point to an EFS file system. It manages access permissions and enforces a root directory for NFS clients. Access Points simplify sharing data in multi-tenant applications by providing isolated namespaces within a single file system."  # fmt: skip
    _docs_url: ClassVar[str] = "https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html"
    _kind_service: ClassVar[Optional[str]] = service_name
    _metadata: ClassVar[Dict[str, Any]] = {"icon": "endpoint", "group": "storage"}
    _aws_metadata: ClassVar[Dict[str, Any]] = {"provider_link_tpl": "https://{region_id}.console.aws.amazon.com/efs/home?region={region}#/access-points/{id}", "arn_tpl": "arn:{partition}:efs:{region}:{account}:access-point/{id}"}  # fmt: skip
    api_spec: ClassVar[AwsApiSpec] = AwsApiSpec(
        service_name,
        "describe-access-points",
        "AccessPoints",
        override_iam_permission="elasticfilesystem:DescribeAccessPoints",
    )
    mapping: ClassVar[Dict[str, Bender]] = {
        "id": S("AccessPointId"),
        "tags": S("Tags", default=[]) >> ToDict(),
        "name": S("Name"),
        "client_token": S("ClientToken"),
        "arn": S("AccessPointArn"),
        "posix_user": S("PosixUser") >> Bend(AwsEfsPosixUser.mapping),
        "root_directory": S("RootDirectory") >> Bend(AwsEfsRootDirectory.mapping),
        "owner_id": S("OwnerId"),
        "life_cycle_state": S("LifeCycleState"),
    }
    _reference_kinds: ClassVar[ModelReference] = {"predecessors": {"default": ["aws_efs_file_system"]}}
    client_token: Optional[str] = field(default=None)
    posix_user: Optional[AwsEfsPosixUser] = field(default=None)
    root_directory: Optional[AwsEfsRootDirectory] = field(default=None)
    owner_id: Optional[str] = field(default=None)
    life_cycle_state: Optional[str] = field(default=None)

    def connect_in_graph(self, builder: GraphBuilder, source: Json) -> None:
        if fs_id := source.get("FileSystemId"):
            builder.dependant_node(
                from_node=self, reverse=True, delete_same_as_default=True, clazz=AwsEfsFileSystem, id=fs_id
            )


resources: List[Type[AwsResource]] = [AwsEfsFileSystem, AwsEfsAccessPoint]
