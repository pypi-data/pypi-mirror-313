# -*- coding: utf-8 -*-
"""Configuration options for discovery migration."""
import ipaddress
import json
import pathlib
import typing as t

import pydantic
import yaml
from pydantic import constr  # Constrained string type.
from pydantic import Field, ValidationError, root_validator, validator
from dm.res.AviatrixProviderVersion import AviatrixProviderVersion
from dm.res.Globals import Globals

if not hasattr(t, "Literal"):
    from typing_extensions import Literal

    t.Literal = Literal


RegionName = t.Literal[
    "af-south-1",
    "ap-east-1",
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-northeast-3",
    "ap-south-1",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-southeast-3",
    "ca-central-1",
    "eu-central-1",
    "eu-north-1",
    "eu-south-1",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "me-south-3",
    "sa-east-1",
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
]
CleanupResources = t.Literal[
    "INTERNAL_LB",
    "NAT",
    "TGW_ATTACHMENT",
    "VGW",
    "PEERING"
]
CIDRList = t.List[ipaddress.IPv4Network]
IPAddressList = t.List[ipaddress.IPv4Address]
Tag = t.Dict[str, str]
Tags = t.List[Tag]
_str = constr(strip_whitespace=True)


def _default_network() -> CIDRList:
    return [ipaddress.IPv4Network("0.0.0.0/0")]


class _BaseModel(pydantic.BaseModel):
    discovery_only: t.ClassVar[bool] = False

    class Config:
        json_encoders = {
            ipaddress.IPv4Address: str,
            ipaddress.IPv4Network: str,
        }
        extra = "forbid"


class BackupConfig(_BaseModel):
    """Backup account folder.

    Uses cloud storage to backup the generated account folder.
    Omit this section if backup is not required.

    Note:
        Currently only S3 backup is supported.

    Attributes:
        s3: S3 backup configuration.
    """

    class S3Config(_BaseModel):
        """Setup S3 for storing the terraform output files.

        Attributes:
            account: S3 bucket account number.
            role_name: S3 bucket access permission.
            name: S3 bucket name.
            region: S3 bucket region.
        """

        account: _str
        role_name: _str
        name: _str
        region: _str
        tf_state_key: t.Optional[_str] = None

    s3: S3Config


class TfControllerAccessConfig(_BaseModel):
    """
    Attributes:
        mode: if "ENV" is used, AVIATRIX_USERNAME and AVIATRIX_PASSWORD should be set for terraform use.
        ssm_role: role with SSM:getParameter permission, e.g., aviatrix-role-app. If it is set to empty string,
                  NO assume_role statement is generated in the AWS provider.
    """

    alias: _str = "us_west_2"
    mode: t.Literal["ENV", "SSM"] = "ENV"
    password_store: _str = "avx-admin-password"
    region: _str = "us-west-2"
    ssm_role: _str = ""
    username: _str = "admin"

    @root_validator(pre=True)
    def check_mode(cls, values):
        """
        Avoid confusion, do not allow other attributes if ENV is used.
        """
        if "mode" in values and values["mode"] == "ENV":
            if len(values) > 1:
                lvalues = dict(values)
                del lvalues["mode"]
                raise ValueError(
                    f"When aviatrix.tf_controller_access.mode is 'ENV', "
                    f"the following attribute(s) {lvalues} should be removed."
                )

        return values


class TfCloudConfig(_BaseModel):
    organization: _str = None
    workspace_name: _str = None
    tags: t.Optional[t.List[_str]] = None

    @classmethod
    def valid_str_attribute(cls, val):
        if val is None or len(val) == 0:
            return False
        return True

    @root_validator(pre=True)
    def check_required_attributes(cls, values):
        """
        check required attributes are there:
        - organization attribute is mandatory;
        - only one of workspace_name and tags attributes is allowed and required.
        check if
        """
        if "organization" not in values or not cls.valid_str_attribute(
            values["organization"]
        ):
            raise ValueError("Missing organization name")
        if "workspace_name" not in values and "tags" not in values:
            raise ValueError(
                "Required workspace_name or tags atttribute to be defined"
            )
        if "workspace_name" in values and "tags" in values:
            raise ValueError("Either workspace_name or tags is allowed")
        if "workspace_name" in values and not cls.valid_str_attribute(
            values["workspace_name"]
        ):
            raise ValueError("Missing workspace_name")
        if "tags" in values and not all(
            [cls.valid_str_attribute(x) for x in values["tags"]]
        ):
            raise ValueError("Empty tag not allowed")
        return values

    @validator("tags")
    def check_and_rewrite_tags(cls, v):
        """
        1. If tags list is empty, raise error
        2. Convert input tags (list of string), e.g., ['abc', 'dec'] into
           a string tags with double quote, e.g., '["abc", "dec"]'.
           This will facilitate terraform tags generation, which requires a list
           of double quote string.

           Performing the conversion here seems to be pretty clean; otherwise,
           it can be done inside common.readGlobalConfigOption.

           *** Of course, we are changing the tags type in such conversion,
           *** seems to be allowed by pydantic.
        """
        if v is not None:
            if len(v) == 0:
                raise ValueError("tags list cannot be empty")
            return json.dumps(v)
        return v


class TerraformConfig(_BaseModel):
    """Terraform configuration.

    Attributes:
        terraform_output: Absolute path to the TF files created.
        terraform_version: Terraform version in terraform version syntax
        aviatrix_provider: Aviatrix terraform provider version in
            terraform version syntax
        aws_provider: AWS terraform provider version in terraform version syntax
        enable_s3_backend: Generate terraform S3 backend config.
            Default to True.
        module_source:  Override the module source in `vpc.tf`. If this is
            omitted or "", we use the included TF module source.
            Defaults to "".
    """

    DEFAULT_MODULE_SOURCE: t.ClassVar[_str] = "../module_aws_brownfield_spoke_vpc"
    DEFAULT_MODULE_NAME: t.ClassVar[_str] = "module_aws_brownfield_spoke_vpc"

    regenerate_common_tf: bool = True
    terraform_output: _str
    terraform_version: t.Optional[_str] = None  # = ">= 0.14"
    aviatrix_provider: t.Optional[_str] = None  # "= 2.19.3"
    aws_provider: t.Optional[_str] = None  # "~> 3.43.0"
    enable_s3_backend: bool = False
    module_source: t.Optional[_str] = DEFAULT_MODULE_SOURCE
    module_name: t.Optional[_str] = DEFAULT_MODULE_NAME
    tf_cloud: TfCloudConfig = None
    tmp_folder_id: t.Optional[_str] = None

    @validator("aviatrix_provider")
    def validateAviatrixProviderVersion(cls, val):
        Globals.setAvxProvider(val)
        return val

    @validator("terraform_version", "aviatrix_provider", "aws_provider", always=True)
    def check_field_for_none(cls, val, values, field):
        if cls.discovery_only:
            return val

        if val is None:
            raise ValueError(f"missing {field.name} attribute")
        return val

    @validator("tf_cloud")
    def check_tfcloud_for_none(cls, val, values):
        """
        handle tfcloud None case where none of its attributes are defined.
        """
        if val is None:
            raise ValueError("missing organization, workspace_name, tags attributes")
        return val

    @validator("tmp_folder_id")
    def validate_tmp_folder_id(cls, val):

        if val is not None and val != "VPC_ID" and val != "YAML_ID":
            raise ValueError('Valid input for tmp_folder_id is "VPC_ID" or "YAML_ID"')
        
        return val

class AviatrixConfig(_BaseModel):
    """Aviatrix config for onboarding.

    Attributes:
        controller_ip: Aviatrix controller IP address.
        controller_account: The AWS Account # where the controller resides.
        ctrl_role_app: Controller app role name in the SPOKE account.
        ctrl_role_ec2: Controller EC2 role name in the CONTROLLER account
        gateway_role_app: Gateway role name in the SPOKE account
        gateway_role_ec2: Gateway instance profile name in the SPOKE account
        tf_controller_access: terraform attributes for accessing controller password, via AWS SSM or ENV
    """

    controller_ip: ipaddress.IPv4Address
    controller_account: _str
    ctrl_role_app: _str = "aviatrix-role-app"
    ctrl_role_ec2: _str = "aviatrix-role-ec2"
    gateway_role_app: _str = "aviatrix-role-app"
    gateway_role_ec2: _str = "aviatrix-role-ec2"
    tf_controller_access: TfControllerAccessConfig = Field(
        default_factory=TfControllerAccessConfig
    )


class AlertConfig(_BaseModel):
    """Alert configuration.

    Attributes:
        expect_dest_cidrs: Alert IP not fall within the given CIDR list. Turn
            off this alert using [“0.0.0.0/0”].
        expect_vpc_prefixes: Alert VPC prefix not fall within given CIDR
            ranges. Turn off this alert using [“0.0.0.0/0”].
    """

    expect_dest_cidrs: CIDRList = Field(default_factory=_default_network)
    expect_vpc_prefixes: CIDRList = Field(default_factory=_default_network)
    check_gateway_existence: t.Optional[bool] = True


class SnatPoliciesConfig(_BaseModel):
    src_ip: _str = None
    connection: _str = None
    new_src_ip: _str = None
    protocol: _str = "all"
    apply_route_entry: t.Optional[bool] = False


class ScriptHsConfig(_BaseModel):
    """Configuration for script features.

    Attributes:
        allow_vpc_cidrs: List of allowed VPC CIDRs. Only the allowed CIDRs will
            be copied to vpc_cidr and passed to the brownfield spoke VPC
            terraform module. Set it to [“0.0.0.0/0”] to allow any CIDR.
        configure_gw_name:
        configure_spoke_advertisement:
        filter_tgw_attachment_subnet: enable tgw attachment subnet filtering.
            Skip subnet used by TGW vpc attachement.
        route_table_tags: List of tags to be added to the route table(s). Omit
            this section if no tags required.
            Defaults to [].
        subnet_tags: List of tags to be added to the subnet(s). Omit this
            section if no tags required.
            Defaults to [].
        migrate_natgw_eip: migrate NATgw EIP
        deploy_2_spokes_only: deploy 2 spokes only since controller does not support 3 spokes with customerized SNAT
        deploy_dummy_spokes: deploy dummy to hold the EIP
        migrate_natgw_one_spoke_per_az: Use one spoke per AZ when migrating NATgw
        natgw_backup_dir: the folder name of the natgw backup

    """

    allow_vpc_cidrs: CIDRList = Field(default_factory=_default_network)
    configure_gw_name: bool = True
    configure_spoke_advertisement: bool = False
    configure_transit_gw_egress: t.Optional[bool] = False
    configure_gw_lb_ep: t.Optional[bool] = False 
    configure_spoke_gw_hs: t.Literal[True]
    filter_tgw_attachment_subnet: bool = False
    filter_vgw_routes: t.Optional[bool] = True
    filter_tgw_routes: t.Optional[bool] = True
    route_table_tags: Tags = Field(default_factory=list)
    subnet_tags: Tags = Field(default_factory=list)
    snat_policies: t.List[SnatPoliciesConfig] = None
    import_resources: t.Optional[bool] = True
    migrate_natgw_eip: t.Optional[bool] = False
    deploy_2_spokes_only: t.Optional[bool] = False
    deploy_dummy_spokes: t.Optional[bool] = False
    migrate_natgw_one_spoke_per_az: t.Optional[bool] = False
    natgw_backup_dir: t.Optional[_str] = "natgw_backups"
    configure_jumbo_frame: t.Optional[bool] = False

    @validator("configure_spoke_gw_hs")
    def validate_configure_spoke_gw_hs(cls, val, values):
        values["add_vpc_cidr"] = False
        return val

    @validator("deploy_2_spokes_only", always=True)
    def validate_deploy_2_spokes_only(cls, val, values):
        if val == True and values["migrate_natgw_eip"] == False:
            raise ValueError('migrate_natgw_eip must be set to True before deploy_2_spokes_only can be set to True')
        if val == False and values["snat_policies"] is not None and values["migrate_natgw_eip"] == True:
            raise ValueError('When using gateway group (configure_spoke_gw_hs is True) with customized SNAT, deploy_2_spokes_only must be set to True')
        return val

    @validator("deploy_dummy_spokes")
    def validate_deploy_dummy_spokes(cls, val, values):
        if val == True:
            if (("migrate_natgw_eip" in values and values["migrate_natgw_eip"] == False) or 
                ("deploy_2_spokes_only" in values and values["deploy_2_spokes_only"] == False)):
                raise ValueError('configure_spoke_gw_hs, migrate_natgw_eip, and deploy_2_spokes_only must be set to True before setting deploy_dummy_spokes to True')
        return val

    @validator("migrate_natgw_one_spoke_per_az")
    def validate_migrate_natgw_one_spoke_per_az(cls, val, values):
        if val == True:
            if "migrate_natgw_eip" in values and values["migrate_natgw_eip"] == False:
                raise ValueError('configure_spoke_gw_hs and migrate_natgw_eip must be set to True before setting migrate_natgw_one_spoke_per_az to True')
        return val


class ScriptConfig(_BaseModel):
    """Configuration for script features.

    Attributes:
        add_vpc_cidr: indicates whether avtx_cidr is to be created by terraform.
        allow_vpc_cidrs: List of allowed VPC CIDRs. Only the allowed CIDRs will
            be copied to vpc_cidr and passed to the brownfield spoke VPC
            terraform module. Set it to [“0.0.0.0/0”] to allow any CIDR.
        configure_gw_name:
        configure_spoke_advertisement:
        filter_tgw_attachment_subnet: enable tgw attachment subnet filtering.
            Skip subnet used by TGW vpc attachement.
        route_table_tags: List of tags to be added to the route table(s). Omit
            this section if no tags required.
            Defaults to [].
        subnet_tags: List of tags to be added to the subnet(s). Omit this
            section if no tags required.
            Defaults to [].
    """

    add_vpc_cidr: bool = True
    allow_vpc_cidrs: CIDRList = Field(default_factory=_default_network)
    configure_gw_name: bool = True
    configure_spoke_advertisement: bool = False
    configure_transit_gw_egress: t.Optional[bool] = False
    configure_gw_lb_ep: t.Optional[bool] = False 
    configure_spoke_gw_hs: t.Literal[False]
    filter_tgw_attachment_subnet: bool = False
    filter_vgw_routes: t.Optional[bool] = True
    filter_tgw_routes: t.Optional[bool] = True
    route_table_tags: Tags = Field(default_factory=list)
    subnet_tags: Tags = Field(default_factory=list)
    snat_policies: t.List[SnatPoliciesConfig] = None
    import_resources: t.Optional[bool] = True
    configure_jumbo_frame: t.Optional[bool] = False

    @validator("configure_spoke_gw_hs")
    def validate_configure_spoke_gw_hs(cls, val, values):
        values["migrate_natgw_eip"] = False
        values["deploy_2_spokes_only"] = False
        values["deploy_dummy_spokes"] = False
        values["migrate_natgw_one_spoke_per_az"] = False
        values["natgw_backup_dir"] = "natgw_backups"
        return val
    
    # @validator("configure_spoke_gw_hs")
    # def validate_configure_spoke_gw_hs(cls, val, values):
    #     if val == True:
    #         if values["add_vpc_cidr"] == True:
    #             raise ValueError('To enable configure_spoke_gw_hs, add_vpc_cidr must be set to False')
    #     return val

    # @validator("migrate_natgw_eip")
    # def validate_migrate_natgw_eip(cls, val, values):
    #     if val == True and values["configure_spoke_gw_hs"] == False:
    #         raise ValueError('configure_spoke_gw_hs must be set to True before setting migrate_natgw_eip to True')
    #     return val

    # @validator("deploy_2_spokes_only", always=True)
    # def validate_deploy_2_spokes_only(cls, val, values):
    #     # configure_spoke_gw_hs might not exist if it failed its own validation
    #     if not "configure_spoke_gw_hs" in values:
    #         return val
    #     if val == False and values["configure_spoke_gw_hs"] == True and values["snat_policies"] is not None:
    #         raise ValueError('When using gateway group (configure_spoke_gw_hs is True) with customized SNAT, deploy_2_spokes_only must be set to True')
    #     if val == True and values["configure_spoke_gw_hs"] == False:
    #         raise ValueError('configure_spoke_gw_hs must be set to True before setting deploy_2_spokes_only to True')
    #     return val

    # @validator("deploy_dummy_spokes")
    # def validate_deploy_dummy_spokes(cls, val, values):
    #     if val == True:
    #         if "configure_spoke_gw_hs" in values and values["configure_spoke_gw_hs"] == False:
    #             raise ValueError('configure_spoke_gw_hs and deploy_2_spokes_only must be set to True before setting deploy_dummy_spokes to True')                
    #         if "deploy_2_spokes_only" in values and values["deploy_2_spokes_only"] == False:
    #             raise ValueError('configure_spoke_gw_hs and deploy_2_spokes_only must be set to True before setting deploy_dummy_spokes to True')
    #     return val

    # @validator("migrate_natgw_one_spoke_per_az")
    # def validate_migrate_natgw_one_spoke_per_az(cls, val, values):
    #     if val == True:
    #         if "configure_spoke_gw_hs" in values and values["configure_spoke_gw_hs"] == False:
    #             raise ValueError('configure_spoke_gw_hs and migrate_natgw_eip must be set to True before setting migrate_natgw_one_spoke_per_az to True')
    #         if "migrate_natgw_eip" in values and values["migrate_natgw_eip"] == False:
    #             raise ValueError('configure_spoke_gw_hs and migrate_natgw_eip must be set to True before setting migrate_natgw_one_spoke_per_az to True')
    #     return val

class TGWConfig(_BaseModel):
    """Transit gateways.

    Attributes:
        tgw_account: TGW account number.
        tgw_role: TGW account access role.
        tgw_by_region: Dictionary of TGW Regions to TGW ID.
            e.g.: {"us-east-1": "tgw-020a8339660950770"}
    """

    tgw_account: _str
    tgw_role: _str
    tgw_by_region: t.Dict[RegionName, _str] = Field(default_factory=dict)


GWName = constr(strip_whitespace=True, max_length=50)


class VPCConfig(_BaseModel):
    """Settings for VPC migration.

    Attributes:
        vpc_id: VPC ID to be migrated
        avtx_cidr: Sets the Aviatrix CIDR used in `vpc-id.tf`.
        gw_zones: Zone letters to deploy spoke gateways in. Discovery will
            deduce the zones if an empty list [] is used.
            Defaults to [].
        spoke_gw_tags: A list of tags applied to the spoke gateway.
        domain:
        encrypt:
        inspection:
        spoke_advertisement:
        spoke_routes:
        spoke_gw_name: Name of the spoke gateway.
        transit_gw_name: Name of the transit gateway.
        retain_peerings: List of pcx-ids for which the peering routes will NOT be deleted when running dm.delete_peer_route.
    """

    vpc_id: _str
    avtx_cidr: t.Optional[ipaddress.IPv4Network] = None
    avtx_subnets: t.Optional[CIDRList] = None
    number_of_spokes: t.Optional[int] = None
    gw_zones: t.List[_str] = Field(default_factory=list)
    eips: t.Optional[IPAddressList] = None
    spoke_gw_tags: Tags = Field(default_factory=list)
    domain: t.Optional[_str] = None
    encrypt: t.Optional[bool] = None
    encrypt_key: t.Optional[_str] = None
    inspection: t.Optional[bool] = None
    spoke_advertisement: t.Optional[CIDRList] = None
    spoke_routes: t.Optional[CIDRList] = None
    spoke_gw_name: t.Optional[GWName] = None
    transit_gw_name: t.Optional[GWName] = None
    transit_gw_egress_name: t.Optional[GWName] = None
    enable_spoke_egress: t.Optional[bool] = None
    spoke_gw_size: t.Optional[_str] = None
    hpe: t.Optional[bool] = None
    max_hpe_performance: t.Optional[bool] = None
    spoke_ha: t.Optional[bool] = None
    retain_peerings: t.List[str] = Field(default_factory=list)
    retain_peering_cidrs: CIDRList = Field(default_factory=_default_network)
    customized_single_ip_snat: bool = False
    az_affinity: t.Optional[bool] = False
    enable_jumbo_frame: t.Optional[bool] = None

    @validator("max_hpe_performance")
    def validate_max_hpe_performance(cls, val, values):
        avxProviderVersionStr = Globals.getAvxProvider()
        avxProvider = AviatrixProviderVersion(avxProviderVersionStr)
        if avxProvider.lessThan("2.22.3"):
            raise ValueError('attribute max_hpe_performance is available only if aviatrix_provider is >= 2.22.3')

        hpe = values.get("hpe", None)
        if hpe is not None and hpe == False and val is not None:
            raise ValueError('attribute max_hpe_performance is available only if hpe is set to True')
        return val


    # @validator("avtx_cidr", always=True)
    # def check_avtx_cidr_for_none(cls, val, values):
    #     """
    #     Setup avtx_cidr be an optional attribute initially.
    #     This routine is used to dynamically control its optional behavior,
    #     based upon the args.discovery_only flag.
    #     It also makes sure this is a valid IPv4 address
    #     """
    #     if cls.discovery_only:
    #         return val

    #     if val is None:
    #         raise ValueError("missing avtx_cidr attribute")

    #     ipaddress.ip_network(val)  # Checks `val` is a valid IP address.

    #     return val

    @validator("encrypt_key")
    def check_encrypt_key(cls, val, values):
        """
        encrypt_key can only be set if encrypt is True
        """
        if cls.discovery_only:
            return val

        encrypt = values.get("encrypt", None)
        if (encrypt is None or encrypt == False) and val is not None:
            raise ValueError("encrypt must be True to set encrypt_key")

        return val


class Region(_BaseModel):
    """Region config container.

    Attributes:
        region: Name of the region.
        vpcs: List of vpcs in the region.
    """

    region: RegionName
    vpcs: t.List[VPCConfig]


class AccountInfo(_BaseModel):
    """Information about spoke VPCs.

    Attributes:
        account_id: AWS Account number.
        account_name: Name of the VPC account owner.
        hpe: Enable high performance encryption on spoke gateways.
            Defaults to True.
        managed_tgw:
        filter_cidrs: Filters out any route within specified CIDR when copying
            the route table. No need to add RFC1918 routes in the list; they
            are filtered by default. Set it to empty list [] if no filtering required.
        spoke_gw_size: Spoke gateway instance size.
        role_name: IAM role assumed to execute API calls.
        add_account:
        onboard_account:
        regions: Dictionary of region names to a list of VPC configurations.
    """

    account_id: constr(strip_whitespace=True, regex=r"^[0-9]+$")  # noqa: F722
    account_name: t.Optional[_str] = ""
    regions: t.List[Region]
    hpe: bool = True
    managed_tgw: bool = False
    filter_cidrs: CIDRList = Field(default_factory=list)
    spoke_gw_size: _str = "t3.micro"
    role_name: _str = "aviatrix-role-app"
    add_account: bool = False
    onboard_account: bool = False
    enable_spoke_egress: bool = False
    max_hpe_performance: t.Optional[bool] = None
    spoke_ha: t.Optional[bool] = True

    @validator("max_hpe_performance")
    def validate_max_hpe_performance(cls, val, values):
        avxProviderVersionStr = Globals.getAvxProvider()
        avxProvider = AviatrixProviderVersion(avxProviderVersionStr)
        if avxProvider.lessThan("2.22.3"):
            raise ValueError('attribute max_hpe_performance is available only if aviatrix_provider is >= 2.22.3')

        hpe = values.get("hpe", None)
        if hpe is not None and hpe == False and val is not None:
            raise ValueError('attribute max_hpe_performance is available only if hpe is set to True')
        return val


class SwitchTrafficConfig(_BaseModel):
    """Settings used during `switch_traffic.

    Attributes:
        delete_tgw_route_delay: Specifiy the delay between
            spoke-gw-advertize-cidr and tgw-route-removal in seconds.
            Defaults to 5.
    """

    delete_tgw_route_delay: _str = "5"
    delete_tgw_route_to_vpcs: t.List[_str] = Field(default_factory=list)


class CleanupConfig(_BaseModel):
    """Resources to cleanup.

    Attributes:
        vpc_cidrs: CIDR's to be deleted from VPC.
        resources: Delete resources like `VGW`, `TGW_ATTACHMENT`, 'NAT' in a VPC.
    """

    vpc_cidrs: CIDRList = Field(default_factory=list)
    resources: t.List[CleanupResources] = Field(default_factory=list)
    report_only: bool = False


GW_NAME_KEYS = ["spoke_gw_name", "transit_gw_name"]


class DiscoveryConfiguration(_BaseModel):
    """Discovery Migration Configuration.

    Attributes:
        aviatrix: Generate terraform resource for onboarding an Aviatrix account.
        alert: Alerts configuration.
        config: Script feature configuration.
        tgw: List of TGWs used, assuming all TGWs are defining within one account.
        account_info: Spoke VPC info.
        switch_traffic: Configuration during switch_traffic.
        cleanup: Resources to cleanup.
        aws: Use AWS S3 to backup the generated account folder.
        terraform: Mark the beginning of terraform info.
    """

    id: t.Optional[_str] = None
    terraform: TerraformConfig
    aviatrix: t.Optional[AviatrixConfig] = None
    account_info: t.List[AccountInfo]
    alert: AlertConfig = Field(default_factory=AlertConfig)
    config: t.Union[ScriptConfig, ScriptHsConfig] = Field(..., discriminator='configure_spoke_gw_hs')
    # config: ScriptConfig = Field(default_factory=ScriptConfig)    
    cleanup: CleanupConfig = Field(default_factory=CleanupConfig)
    switch_traffic: SwitchTrafficConfig = Field(default_factory=SwitchTrafficConfig)
    aws: t.Optional[BackupConfig] = None
    tgw: t.Optional[TGWConfig] = Field(default_factory=dict)

    @validator("aviatrix", always=True)
    def check_field_for_none(cls, val, values, field):
        if cls.discovery_only:
            return val

        if val is None:
            raise ValueError(f"missing {field.name}")
        return val

    @validator("tgw")
    def check_tgw_for_none(cls, val, values):
        """
        handle tgw None case where none of its attributes are defined.
        """
        if val is None:
            raise ValueError(
                "missing tgw_account, tgw_role and tgw_by_region attributes"
            )
        return val

    @classmethod
    def isExpectedVpcPrefix(cls, ip, prefixes):
        ipn = ipaddress.ip_network(ip)
        for n in prefixes:
            if ipn.subnet_of(n):
                return True
        return False
    
    @classmethod
    def validate_number_of_spokes_dependence(cls, val, values):
        config = val
        account_info = values.get("account_info", [])        
        errors = []
        errors2 = []
        errors3 = []
        errors4 = []    
        if config.configure_spoke_gw_hs == True:
            if config.migrate_natgw_eip == False:
                for account in account_info:
                    for region in account.regions:
                        for vpc in region.vpcs:
                            if vpc.avtx_subnets is None and vpc.number_of_spokes is None:
                                errors.append(
                                    (account.account_id, region.region, vpc.vpc_id)
                                )
                            if vpc.avtx_subnets is not None and vpc.number_of_spokes is not None:
                                errors2.append(
                                    (account.account_id, region.region, vpc.vpc_id)
                                )
            else:
                for account in account_info:
                    for region in account.regions:
                        for vpc in region.vpcs:
                            if vpc.avtx_subnets is not None or vpc.number_of_spokes or len(vpc.gw_zones) > 0:
                                errors3.append(
                                    (account.account_id, region.region, vpc.vpc_id)
                                )
        else:
            for account in account_info:
                for region in account.regions:
                    for vpc in region.vpcs:
                        if vpc.avtx_subnets is not None or vpc.number_of_spokes is not None:
                            errors4.append(
                                (account.account_id, region.region, vpc.vpc_id)
                            )
    
        if errors:
            error_vpc_str = "\n".join(
                f"account: {account_id}, region: {region}, vpc: {vpc_id}"
                for account_id, region, vpc_id in errors
            )
            raise ValueError(
                'one of avtx_subnets and number_of_spokes attribute must be defined.'
                'List of nonconforming VPCs:'
                f'{error_vpc_str}'
                )
        
        if errors2:
            error_vpc_str = "\n".join(
                f"account: {account_id}, region: {region}, vpc: {vpc_id}"
                for account_id, region, vpc_id in errors2
            )
            raise ValueError(
                'Only one of avtx_subnets and number_of_spokes attribute can be used.'
                '\nList of nonconforming VPCs:\n'
                f'{error_vpc_str}'
                )
        
        if errors3:
            error_vpc_str = "\n".join(
                f"account: {account_id}, region: {region}, vpc: {vpc_id}"
                for account_id, region, vpc_id in errors3
            )
            raise ValueError(
                'gw_zones, avtx_subnets and number_of_spokes attributes cannot be used when migrate_natgw_eip is True.'
                '\nList of nonconforming VPCs:\n'
                f'{error_vpc_str}'
                )
        
        if errors4:
            error_vpc_str = "\n".join(
                f"account: {account_id}, region: {region}, vpc: {vpc_id}"
                for account_id, region, vpc_id in errors4
            )
            raise ValueError(
                'Both avtx_subnets and number_of_spokes attributes cannot be used when configure_spoke_gw_hs is False.'
                '\nList of nonconforming VPCs:\n'
                f'{error_vpc_str}'
                )
    
    @validator("config")
    def check_config(cls, val, values):
        """1. Check configure_transit_gw_egress to configure_gw_name dependence
           2. Check configure_transit_gw_egress to transit_gw_egress_name dependence
           3. Validate gateway names.

        Args:
            val: The account_info dictionary.
            values: All values passed to DiscoveryConfiguration init.

        returns:
            The account_info dictionary.
        """
        config = val
        errors = []

        # if discovery_only, skip validation
        #
        if cls.discovery_only:
            return val

        account_info = values.get("account_info", [])

        # 1. check config.configure_transit_gw_egress requires config.configure_gw_name.
        if config.configure_transit_gw_egress == True and config.configure_gw_name == False:
            raise ValueError(
                "config.configure_transit_gw_egress is only available when config.configure_gw_name is True."
            )

        # 2. check config.configure_transit_gw_egress and account_info.region.vpc.transit_gw_egress_name dependence
        if config.configure_transit_gw_egress == False:
            for account in account_info:
                for region in account.regions:
                    for vpc in region.vpcs:
                        if getattr(vpc, "transit_gw_egress_name") is not None:
                            errors.append(
                                (account.account_id, region.region, vpc.vpc_id)
                            )
        if errors:
            error_vpc_str = "\n".join(
                f"account: {account_id}, region: {region}, vpc: {vpc_id}"
                for account_id, region, vpc_id in errors
            )
            raise ValueError(
                f"'config.configure_transit_gw_egress' must be set to True to use vpc.transit_gw_egress_name."
                " Nonconforming VPCs: "
                f"{error_vpc_str}"
            )

        # 3. check_gw_names
        errors = []
        errors2 = []
        if config.configure_gw_name:
            for account in account_info:
                for region in account.regions:
                    for vpc in region.vpcs:
                        if any(getattr(vpc, key) is None for key in GW_NAME_KEYS):
                            errors.append(
                                (account.account_id, region.region, vpc.vpc_id)
                            )
        else:
            for account in account_info:
                for region in account.regions:
                    for vpc in region.vpcs:
                        if any(getattr(vpc, key) is not None for key in GW_NAME_KEYS):
                            errors2.append(
                                (account.account_id, region.region, vpc.vpc_id)
                            )

        if errors:
            error_vpc_str = "\n".join(
                f"account: {account_id}, region: {region}, vpc: {vpc_id}"
                for account_id, region, vpc_id in errors
            )
            raise ValueError(
                f"'config.configure_gw_name' is {config.configure_gw_name}, "
                "both 'spoke_gw_name' and 'transit_gw_name' must be set in all VPCs."
                "\nList of nonconforming VPCs:\n"
                f"{error_vpc_str}"
            )
        if errors2:
            error_vpc_str = "\n".join(
                f"account: {account_id}, region: {region}, vpc: {vpc_id}"
                for account_id, region, vpc_id in errors2
            )
            raise ValueError(
                f"'config.configure_gw_name' is {config.configure_gw_name}, "
                "both 'spoke_gw_name' and 'transit_gw_name' must NOT be set in any VPCs."
                "\nList of nonconforming VPCs:\n"
                f"{error_vpc_str}"
            )

        # 4. check number_of_spokes:
        cls.validate_number_of_spokes_dependence(val, values)

        # 5. check configure_spoke_gw_hs and avtx_cidr/avtx_subnets dependences
        #    check gw_zones length
        errors = []
        avtx_cidr_errors = []
        avtx_cidr_prefixlen_errors = []
        gw_zones_errors = []
        eips_hs_errors = []
        eips_errors = []
        avtx_cidr_missing_errors = []
        enable_jumbo_frame_errors = []
        for account in account_info:
            spoke_ha = getattr(account,"spoke_ha")
            for region in account.regions:
                for vpc in region.vpcs:
                    if getattr(vpc,"spoke_ha") is not None:
                        # override account-level spoke_ha if vpc-level spoke_ha is NOT None
                        spoke_ha = getattr(vpc,"spoke_ha")
                    if config.configure_spoke_gw_hs:
                        if config.migrate_natgw_eip == False:
                            #
                            # gateway group:
                            # configure_spoke_gw_hs True and migrate_natgw_gw_eip False
                            #
                            allow_list = config.allow_vpc_cidrs
                            avtx_cidr = getattr(vpc, "avtx_cidr")
                            if avtx_cidr is not None and not cls.isExpectedVpcPrefix(avtx_cidr,allow_list):
                                # log error if defined avtx_cidr is NOT in allow_vpc_cidrs list
                                avtx_cidr_errors.append(
                                    (account.account_id, region.region, vpc.vpc_id)
                                )
                            if avtx_cidr is not None:
                                ipn = ipaddress.IPv4Network(avtx_cidr)
                                if ipn.prefixlen > 24:
                                    # log error if defined avtx_cidr prefix length is larger than 24
                                    avtx_cidr_prefixlen_errors.append(
                                        (account.account_id, region.region, vpc.vpc_id)
                                    )
                            avtx_subnets = getattr(vpc, "avtx_subnets")
                            if avtx_cidr is None or avtx_subnets is not None:
                                # When avtx_cidr is not provided, the followings
                                # are mandatory: 
                                # avtx_subnets, gw_zones, and eip
                                avtx_subnets = getattr(vpc, "avtx_subnets")
                                eips = getattr(vpc, "eips")                     
                                if avtx_subnets is None or len(avtx_subnets) == 0:
                                    # log error if avtx_subnets list is empty
                                    errors.append(
                                        (account.account_id, region.region, vpc.vpc_id)
                                    )
                                elif len(avtx_subnets) > len(getattr(vpc, "gw_zones")):
                                    # log error if length of avtx_subnets does not match length of gw_zones
                                    gw_zones_errors.append(
                                        (account.account_id, region.region, vpc.vpc_id)
                                    )
                                elif eips is not None and len(eips) != len(avtx_subnets):
                                    # log error if defined number of eips does not match length of avtx_subnets list
                                    eips_hs_errors.append(
                                        (account.account_id, region.region, vpc.vpc_id)
                                    )
                        else:
                            # migrate_natgw_eip True
                            if getattr(vpc, "avtx_cidr") is None:
                                avtx_cidr_missing_errors.append(
                                    (account.account_id, region.region, vpc.vpc_id)
                                )
                    else:
                        #
                        # classic:
                        # configure_spoke_gw_hs False
                        #
                        eips = getattr(vpc, "eips")                        
                        if spoke_ha == True:
                            if eips is not None and len(eips) != 2:
                                # log error if defined number of eips is NOT 2 in HA mode
                                eips_errors.append(f"HA mode, 2 eips is needed in {account.account_id}/{region.region}/{vpc.vpc_id}")
                        else:
                            # log error if defined number of eips is NOT 1 in non-HA mode
                            if eips is not None and len(eips) != 1:
                                eips_errors.append(f"Non HA mode, only 1 eip is needed in {account.account_id}/{region.region}/{vpc.vpc_id}")

                        if config.add_vpc_cidr == True:
                            allow_list = config.allow_vpc_cidrs
                            avtx_cidr = getattr(vpc, "avtx_cidr")
                            if avtx_cidr is not None and not cls.isExpectedVpcPrefix(avtx_cidr,allow_list):
                                # log error if avtx_cidr is NOT in allow_vpc_cidrs list
                                avtx_cidr_errors.append(
                                    (account.account_id, region.region, vpc.vpc_id)
                                )
                        if getattr(vpc, "avtx_cidr") is None or getattr(vpc, "avtx_subnets") is not None:
                            # log error if avtx_cidr is not defined or avtx_subnets is defined in non-HS mode
                            errors.append(
                                (account.account_id, region.region, vpc.vpc_id)
                            )
                    enable_jumbo_frame = getattr(vpc, "enable_jumbo_frame")
                    if enable_jumbo_frame is not None and config.configure_jumbo_frame == False:
                        enable_jumbo_frame_errors.append((account.account_id,region.region,vpc.vpc_id))

        if avtx_cidr_prefixlen_errors:
            error_vpc_str = "; ".join(
                f"account: {account_id}, region: {region}, vpc: {vpc_id}"
                for account_id, region, vpc_id in avtx_cidr_prefixlen_errors
            )
            raise ValueError(
                    f"avtx_cidr - number of bits in network mask needs to be 24 or smaller: "
                    f"{error_vpc_str}"
                )
        if avtx_cidr_errors:
            error_vpc_str = "; ".join(
                f"account: {account_id}, region: {region}, vpc: {vpc_id}"
                for account_id, region, vpc_id in avtx_cidr_errors
            )
            raise ValueError(
                    f"avtx_cidr is NOT in allow_vpc_cidrs list: "
                    f"{error_vpc_str}"
                )
        if eips_errors:
            error_vpc_str = "; ".join(
                    mess
                    for mess in eips_errors
                )
            raise ValueError(
                    error_vpc_str
                )
        if eips_hs_errors:
            error_vpc_str = "; ".join(
                f"account: {account_id}, region: {region}, vpc: {vpc_id}"
                for account_id, region, vpc_id in eips_hs_errors
            )
            raise ValueError(
                    f"The number of eips should match the number of avtx_subnets: "
                    f"{error_vpc_str}"
                )
            
        if errors:
            error_vpc_str = "; ".join(
                f"account: {account_id}, region: {region}, vpc: {vpc_id}"
                for account_id, region, vpc_id in errors
            )
            if config.configure_spoke_gw_hs:
                raise ValueError(
                    f"'config.configure_spoke_gw_hs' is {config.configure_spoke_gw_hs}, "
                    "avtx_subnets cannot be empty. "
                    "List of nonconforming VPCs: "
                    f"{error_vpc_str}"
                )
            else:
                raise ValueError(
                    f"'config.configure_spoke_gw_hs' is {config.configure_spoke_gw_hs}, "
                    "avtx_cidr must be used instead of avtx_subnets. "
                    "List of nonconforming VPCs: "
                    f"{error_vpc_str}"
                )
        if gw_zones_errors:
            error_vpc_str = "; ".join(
                f"account: {account_id}, region: {region}, vpc: {vpc_id}"
                for account_id, region, vpc_id in gw_zones_errors
            )
            raise ValueError(
                "length of gw_zones must be longer than or equal to the length of avtx_subnets. "
                "List of nonconforming VPCs: "
                f"{error_vpc_str}"
            )
        
        if avtx_cidr_missing_errors:
            error_vpc_str = "; ".join(
                f"account: {account_id}, region: {region}, vpc: {vpc_id}"
                for account_id, region, vpc_id in avtx_cidr_missing_errors
            )
            raise ValueError(
                "missing avtx_cidr. "
                "List of nonconforming VPCs: "
                f"{error_vpc_str}"
            )
        
        if enable_jumbo_frame_errors:
            error_vpc_str = "; ".join(
                f"account: {account_id}, region: {region}, vpc: {vpc_id}"
                for account_id, region, vpc_id in enable_jumbo_frame_errors
            )
            raise ValueError(
                "Set config/configure_jumbo_frame to True before setting enable_jumbo_frame. "
                "List of nonconforming VPCs: "
                f"{error_vpc_str}"
            )

        # 6. check configure_spoke_advertisement and spoke_advertisement dependences
        #    check empty spoke_advertisement
        errors = []
        for account in account_info:
            for region in account.regions:
                for vpc in region.vpcs:
                    spoke_advertisement_list = getattr(vpc, "spoke_advertisement")
                    if spoke_advertisement_list is not None:
                        if config.configure_spoke_advertisement is False:
                            raise ValueError(
                                "configure_spoke_advertisement in config section must be set to True to use spoke_advertisement. "
                            )
                        if len(spoke_advertisement_list) == 0:                    
                            errors.append(
                                (account.account_id, region.region, vpc.vpc_id)
                            )
                    
        if errors:
            error_vpc_str = "; ".join(
                f"account: {account_id}, region: {region}, vpc: {vpc_id}"
                for account_id, region, vpc_id in errors
            )
            raise ValueError(
                "spoke_advertisement cannot be empty. Add a CIDR or remove it. "
                "List of nonconforming VPCs: "
                f"{error_vpc_str}"
            )

        return config

    @validator("cleanup")
    def check_cleanup(cls, val, values):

        # if discovery_only, skip validation
        #
        if cls.discovery_only:
            return val

        cleanup = val
        config = values.get("config")
        # config is not available if previous validation failed
        if config == None:
            return val

        # check configure_gw_name and cleanup.resource["PEERING"] dependence
        if config.configure_gw_name == False:
            if "PEERING" in cleanup.resources:
                raise ValueError(
                   f"Delete 'PEERING' is only supported when config.configure_gw_name is set to True."
                )

        return val

def load_from_dict(
    config_dict: t.Dict, discovery_only: bool = False
) -> DiscoveryConfiguration:
    """Load discovery migration settings from a python dictionary.

    Args:
        config_dict: Python dictionary in which to load configuration
            settings from.

    Returns:
        Parsed discovery migration settings.
    """
    _BaseModel.discovery_only = discovery_only

    try:
        config = DiscoveryConfiguration(**config_dict)
    except ValidationError as e:
        print(e.json())
        raise SystemExit(1) from e
    return config


def dump_to_dict(config: DiscoveryConfiguration) -> t.Dict:
    """Dump discovery migration settings to a python dictionary.

    Args:
        config: Discovery migration settings.

    Returns:
        Configuration dictionary.
    """
    json_data = config.json()
    data = json.loads(json_data)

    return data


def load_from_yaml(
    yml_path: pathlib.Path, discovery_only: bool = False
) -> DiscoveryConfiguration:
    """Load discovery migration settings from a yaml.

    Args:
        yml_path: Path to location of discovery migration yaml.

    Returns:
        Parsed discovery migration settings.
    """
    with open(yml_path, "r") as fh:
        data = yaml.load(fh, Loader=yaml.FullLoader)

    return load_from_dict(data, discovery_only=discovery_only)


def dump_to_yaml(config: DiscoveryConfiguration, dest: pathlib.Path) -> pathlib.Path:
    """Dump discovery migration settings to a yaml file.

    Args:
        config: Discovery migration settings.
        dest: Path to destination location of discovery migration yaml.

    Returns:
        Path to destination location of discovery migration yaml.
    """
