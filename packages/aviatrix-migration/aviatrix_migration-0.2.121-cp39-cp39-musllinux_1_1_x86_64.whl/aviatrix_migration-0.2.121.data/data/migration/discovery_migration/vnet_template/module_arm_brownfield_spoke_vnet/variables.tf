variable "region" {}
variable "account_name" {}
variable "resource_group_name" {}
variable "vnet_name" {}
variable "vnet_cidr" {
  description = "CIDR used by the applications"
}
variable "avtx_cidr" {
  default     = ""
  description = "CIDR used by the Aviatrix gateways"
}
variable "avtx_gw_size" {}
variable "hpe" {
  default = true
}
variable "use_azs" {
  type = bool
}
variable "route_tables" {}

variable "main_rt_count" {
  description = "Number of aviatrix main route table required.  It is assigned to subnet without a user-defined route table"
  type        = number
  default     = 2
}

variable "switch_traffic" {
  type    = bool
  default = false
}
variable "disable_bgp_propagation" {
  type        = bool
  default     = true
  description = "Used to configure aviatrix_managed_main RTs"
}
variable "spoke_gw_name" {
  default = ""
}
variable "transit_gw" {
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

{% if not data.configure_subnet_groups %}
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
{% endif %}

variable "spoke_ha" {
  type        = bool
  default     = true
  description = "Set to false to skip spoke HA gateway creation"
}

{% if not data.pre_v2_22_3 %}
variable "max_hpe_performance" {
  type        = bool
  default     = true
  description = "False causes creation of only one spoke-transit tunnel (4 total) over a private peering"
}

{% endif %}

{% if data.configure_subnet_groups %}
variable "subnet_groups" {
}
variable "inspected_subnet_groups" {}
{% endif %}

{% if data.configure_main_route_table_prefix | length > 0 %}
variable "main_route_table_prefix" {}
{% endif %}

output azurerm_route_table_aviatrix_managed {
  value = azurerm_route_table.aviatrix_managed
}

output azurerm_route_table_aviatrix_managed_main {
  value = azurerm_route_table.aviatrix_managed_main
}
