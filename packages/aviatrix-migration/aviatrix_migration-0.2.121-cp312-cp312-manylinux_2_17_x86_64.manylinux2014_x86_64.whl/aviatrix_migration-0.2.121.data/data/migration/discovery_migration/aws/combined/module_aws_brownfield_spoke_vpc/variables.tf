variable "region" {}

variable "account_name" {}

variable "role_arn" {}

variable "vpc_name" {}

{% if data.configure_spoke_gw_hs %}
variable "advertised_vpc_cidr" {
  default = null
  type = string
}

{% else %}
variable "advertised_vpc_cidr" {
  type = list(string)
}

variable "gw_zones" {
  type = list(any)
}

variable "avtx_gw_size" {
  default = ""
}
{% endif %}
variable "vpc_id" {}

variable "avtx_cidr" {
  default     = ""
  description = "CIDR used by the Aviatrix gateways"
}

variable "hpe" {
  default = false
}

variable "igw_id" {
  default = ""
}

variable "route_tables" {}

variable "gw_name_suffix" {
  default = ""
}

variable "switch_traffic" {
  type    = bool
  default = false
}

variable "spoke_gw_name" {
  default = ""
}

variable "transit_gw" {
  default = ""
}

{% if data.configure_transit_gw_egress %}
variable "transit_gw_egress" {
  default = ""
}

{% endif %}
variable "tgw_name" {
  default = ""
}

variable "tags" {
  description = "Map of tags to assign to the gateway."
  type        = map(any)
  default     = null
}

variable "domain" {
  description = "Provide security domain name to which spoke needs to be deployed. Transit gateway mus tbe attached and have segmentation enabled."
  type        = string
  default     = ""
}

variable "inspection" {
  description = "Set to true to enable east/west Firenet inspection. Only valid when transit_gw is East/West transit Firenet"
  type        = bool
  default     = false
}

variable "spoke_routes" {
  description = "A list of comma separated CIDRs to be customized for the spoke VPC routes. When configured, it will replace all learned routes in VPC routing tables, including RFC1918 and non-RFC1918 CIDRs. It applies to this spoke gateway only"
  type        = string
  default     = ""
}

variable "spoke_adv" {
  description = "A list of comma separated CIDRs to be advertised to on-prem as Included CIDR List. When configured, it will replace all advertised routes from this VPC."
  type        = string
  default     = ""
}

variable "encrypt" {
  description = "Enable EBS volume encryption for Gateway. Only supports AWS and AWSGOV provider. Valid values: true, false. Default value: false"
  type        = bool
  default     = false
}

variable "encrypt_key" {
  description = "The encryption key name for EBS volume encryption."
  type        = string
  default     = null
}

variable "enable_spoke_egress" {
  type    = bool
  default = false
}

variable "vpc_cidr_for_snat" {
  type = list(string)
  default = []
}

{% if not data.pre_v2_22_3 %}
variable "max_hpe_performance" {
  type        = bool
  default     = true
  description = "False causes creation of only one spoke-transit tunnel (4 total) over a private peering"
}

{% endif %}
output aws_route_table_aviatrix_managed {
  value = aws_route_table.aviatrix_managed
}

variable "spoke_ha" {
  type        = bool
  default     = true
  description = "Set to false to skip spoke HA gateway creation"
}

{% if data.configure_spoke_gw_hs %}
variable "spoke_gws" {
  type = list(object({ 
    avtx_cidr = string
    gw_zone = string
    eip = string
    avtx_gw_size = string
  }))
}

  {% if data.snat_policies or data.snat_policies == [] %}
variable "deploy_2_spokes_only" {
  type = bool
  default = false
}
  {% endif %}
{% endif %}

{% if data.migrate_natgw_eip and (data.snat_policies or data.snat_policies == []) %}
variable "deploy_dummy_spokes" {
  type    = bool
  default = false
}
{% endif %}

variable "eips" {
  type = list(string)
  default = []
}

{% if data.configure_jumbo_frame %}
variable "enable_jumbo_frame" {
  type    = bool
  default = null
}
{% endif %}