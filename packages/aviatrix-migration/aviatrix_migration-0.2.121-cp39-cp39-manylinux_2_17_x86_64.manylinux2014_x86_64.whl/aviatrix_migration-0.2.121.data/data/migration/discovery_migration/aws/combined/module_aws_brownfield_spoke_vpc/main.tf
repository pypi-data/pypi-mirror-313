{% if data.add_vpc_cidr %}
resource "aws_vpc_ipv4_cidr_block_association" "aviatrix_cidr" {
  vpc_id     = var.vpc_id
  cidr_block = var.avtx_cidr
}
{% endif %}

resource "aws_internet_gateway" "IGW" {
  count  = var.igw_id == "" ? 1 : 0
  vpc_id = var.vpc_id
  tags = {
    Name                        = "aviatrix-${var.vpc_name}"
    "Aviatrix-Created-Resource" = "Do-Not-Delete-Aviatrix-Created-Resource"
  }
}

{% if not data.configure_spoke_gw_hs %}
resource "aws_subnet" "aviatrix_public" {
  count             = var.hpe ? 0 : (var.spoke_ha ? 2 : 1)
  vpc_id            = var.vpc_id
  {% if data.add_vpc_cidr %}
  cidr_block        = cidrsubnet(aws_vpc_ipv4_cidr_block_association.aviatrix_cidr.cidr_block, 1, count.index)
  {% else %}
  cidr_block        = cidrsubnet(var.avtx_cidr, 1, count.index)
  {% endif %}
  availability_zone = var.gw_zones[count.index]
  tags = {
    Name                        = count.index == 0 ? "aviatrix-${var.vpc_name}-gw" : "aviatrix-${var.vpc_name}-gw-hagw"
    "Aviatrix-Created-Resource" = "Do-Not-Delete-Aviatrix-Created-Resource"
  }
}

resource "aws_route_table_association" "aviatrix_public" {
  count          = var.hpe ? 0 : (var.spoke_ha ? 2 : 1)
  subnet_id      = aws_subnet.aviatrix_public[count.index].id
  route_table_id = aws_route_table.aviatrix_public[0].id
}

{% else %}
locals {
  {% if data.snat_policies or data.snat_policies == [] %}
  gateway_count      = var.deploy_2_spokes_only ? 2 : length(var.spoke_gws)
  ha_private_ip = [
    aviatrix_spoke_ha_gateway.ha1,
    aviatrix_spoke_ha_gateway.ha2,
    aviatrix_spoke_ha_gateway.ha3,
    aviatrix_spoke_ha_gateway.ha4,
    aviatrix_spoke_ha_gateway.ha5,
  ]
  {% else %}
  gateway_count      = length(var.spoke_gws)
  {% endif %}
  avtx_cidrs = [ for spoke_gw in var.spoke_gws: spoke_gw["avtx_cidr"] ]
}

resource "aws_vpc_ipv4_cidr_block_association" "aviatrix_cidr" {
  count      = var.avtx_cidr == "" ? 0 : 1
  vpc_id     = var.vpc_id
  cidr_block = var.avtx_cidr
}

resource "aws_subnet" "aviatrix_public" {
  {% if data.migrate_natgw_eip and (data.snat_policies or data.snat_policies == []) %}
  count             = var.hpe ? 0 : (var.deploy_dummy_spokes ? length(var.spoke_gws) : local.gateway_count)
  {% else %}
  count             = var.hpe ? 0 : local.gateway_count
  {% endif %}
  vpc_id            = var.vpc_id
  cidr_block        = var.spoke_gws[count.index]["avtx_cidr"]
  availability_zone = var.spoke_gws[count.index]["gw_zone"]
  map_public_ip_on_launch = false
  tags = {
    "Name"                      = "aviatrix-${var.vpc_name}-gw-az-${substr(var.spoke_gws[count.index]["gw_zone"],-1,1)}"
    "Aviatrix-Created-Resource" = "Do-Not-Delete-Aviatrix-Created-Resource"
  }

  depends_on        = [ aws_vpc_ipv4_cidr_block_association.aviatrix_cidr ]
  lifecycle {
    ignore_changes = [availability_zone_id]
  }
}

resource "aws_route_table_association" "aviatrix_public" {
  {% if data.migrate_natgw_eip and (data.snat_policies or data.snat_policies == []) %}
  count = var.hpe ? 0 : (var.deploy_dummy_spokes ? length(var.spoke_gws) : local.gateway_count)
  {% else %}
  count = var.hpe ? 0 : local.gateway_count
  {% endif %}

  subnet_id      = aws_subnet.aviatrix_public[count.index].id
  route_table_id = aws_route_table.aviatrix_public[0].id
}

{% endif %}
resource "aws_route_table" "aviatrix_public" {
  count  = var.hpe ? 0 : 1
  vpc_id = var.vpc_id
  tags = {
    Name                        = "aviatrix-${var.vpc_name}-gw"
    "Aviatrix-Created-Resource" = "Do-Not-Delete-Aviatrix-Created-Resource"
  }
}

resource "aws_route" "aviatrix_default" {
  count                  = var.hpe ? 0 : 1
  route_table_id         = aws_route_table.aviatrix_public[0].id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = var.igw_id == "" ? aws_internet_gateway.IGW[0].id : var.igw_id
}

resource "aviatrix_spoke_gateway" "gw" {
  cloud_type                        = 1
  account_name                      = var.account_name
  {% if data.configure_jumbo_frame %}
  enable_jumbo_frame                = var.enable_jumbo_frame
  {% endif %}
  {% if data.configure_gw_name %}
  gw_name                           = var.spoke_gw_name
  {% else %}
  gw_name                           = "aws-${local.region[var.region]}-${join("", formatlist("%02x", split(".", split("/", var.avtx_cidr)[0])))}-gw"
  {% endif %}
  vpc_id                            = var.vpc_id
  vpc_reg                           = var.region
  insane_mode                       = var.hpe
  {% if not data.configure_spoke_gw_hs %}
  gw_size                           = var.avtx_gw_size
  ha_gw_size                        = var.spoke_ha ? var.avtx_gw_size : null
  {% else %}
  gw_size                           = var.spoke_gws[0]["avtx_gw_size"]
  manage_ha_gateway                 = false
  {% endif %}

  {% if data.add_vpc_cidr %}
  subnet                            = cidrsubnet(aws_vpc_ipv4_cidr_block_association.aviatrix_cidr.cidr_block, 1, 0)
  ha_subnet                         = var.spoke_ha ? cidrsubnet(aws_vpc_ipv4_cidr_block_association.aviatrix_cidr.cidr_block, 1, 1) : null
  allocate_new_eip                  = try(var.eips[0],null) == null ? true : false
  eip                               = try(var.eips[0],null)
  insane_mode_az                    = var.hpe ? var.gw_zones[0] : null
  {% else %}
    {% if not data.configure_spoke_gw_hs %}
  subnet                            = cidrsubnet(var.avtx_cidr, 1, 0)
  ha_subnet                         = var.spoke_ha ? cidrsubnet(var.avtx_cidr, 1, 1) : null
  allocate_new_eip                  = try(var.eips[0],null) == null ? true : false
  eip                               = try(var.eips[0],null)
  insane_mode_az                    = var.hpe ? var.gw_zones[0] : null
    {% else %}
  subnet                            = var.spoke_gws[0]["avtx_cidr"]
  allocate_new_eip                  = try(var.spoke_gws[0]["eip"],null) == null ? true : false
  eip                               = try(var.spoke_gws[0]["eip"],null)
  insane_mode_az                    = var.hpe ? var.spoke_gws[0]["gw_zone"] : null
    {% endif %}
  {% endif %}

  {% if not data.configure_spoke_gw_hs %}
  ha_insane_mode_az                 = var.spoke_ha ? (var.hpe ? var.gw_zones[1] : null) : null
  ha_eip                            = var.spoke_ha ? (try(var.eips[1],null)) : null
  {% endif %}
  {% if data.configure_spoke_gw_hs %}
  # controller advertises the whole VPC cidrs if advertised_vpc_cidr is set to null.
  included_advertised_spoke_routes  = var.switch_traffic ? (var.advertised_vpc_cidr == null ? null : var.advertised_vpc_cidr) : join(",", local.avtx_cidrs)
  {% else %}
    {% if data.add_vpc_cidr %}
  included_advertised_spoke_routes  = var.switch_traffic ?  join(",", concat(var.advertised_vpc_cidr, [var.avtx_cidr])) : var.avtx_cidr
    {% elif data.configure_spoke_advertisement %}
  included_advertised_spoke_routes  = var.switch_traffic ? (var.spoke_adv != "" ? var.spoke_adv : join(",", var.advertised_vpc_cidr)): var.avtx_cidr
    {% else %}
  included_advertised_spoke_routes  = var.switch_traffic ? join(",", var.advertised_vpc_cidr) : var.avtx_cidr
    {% endif %}
  {% endif %}
  customized_spoke_vpc_routes       = var.spoke_routes != "" ? var.spoke_routes : null
  {% if data.pre_v3_0_0 %}
  manage_transit_gateway_attachment = false
  {% endif %}
  {% if data.pre_v2_21_0 %}
  enable_active_mesh                = true
  {% endif %}
  {% if not data.snat_policies and not data.snat_policies == [] %}
  single_ip_snat                    = var.switch_traffic && var.enable_spoke_egress
  {% endif %}
  single_az_ha                      = true
  customer_managed_keys             = var.encrypt_key
  enable_encrypt_volume             = var.encrypt
  tags                              = var.tags
  depends_on = [aws_route.aviatrix_default, aws_route_table_association.aviatrix_public, aws_route.pre_migration, aws_internet_gateway.IGW]
}

{% if data.configure_spoke_gw_hs %}
resource "aviatrix_spoke_ha_gateway" "ha1" {
  {% if data.migrate_natgw_eip %}
  count           = var.switch_traffic ? 1 : 0
  {% else %}
  count           = local.gateway_count > 1 ? 1 : 0
  {% endif %}
  primary_gw_name = aviatrix_spoke_gateway.gw.id
  gw_name         = "${aviatrix_spoke_gateway.gw.gw_name}-${1}"
  insane_mode     = var.hpe
  subnet          = var.spoke_gws[1]["avtx_cidr"]
  eip             = try(var.spoke_gws[1]["eip"],null)
  insane_mode_az  = var.spoke_gws[1]["gw_zone"]
  gw_size         = var.spoke_gws[1]["avtx_gw_size"]

  lifecycle {
    ignore_changes = [insane_mode_az]
  }
}

resource "aviatrix_spoke_ha_gateway" "ha2" {
  count           = local.gateway_count > 2 ? 1 : 0
  primary_gw_name = aviatrix_spoke_gateway.gw.id
  gw_name         = "${aviatrix_spoke_gateway.gw.gw_name}-${2}"
  insane_mode     = var.hpe
  subnet          = var.spoke_gws[2]["avtx_cidr"]
  eip             = try(var.spoke_gws[2]["eip"],null)
  insane_mode_az  = var.spoke_gws[2]["gw_zone"]
  gw_size         = var.spoke_gws[2]["avtx_gw_size"]
  depends_on      = [aviatrix_spoke_ha_gateway.ha1]

  lifecycle {
    ignore_changes = [insane_mode_az]
  }
}

resource "aviatrix_spoke_ha_gateway" "ha3" {
  count           = local.gateway_count > 3 ? 1 : 0
  primary_gw_name = aviatrix_spoke_gateway.gw.id
  gw_name         = "${aviatrix_spoke_gateway.gw.gw_name}-${3}"
  insane_mode     = var.hpe
  subnet          = var.spoke_gws[3]["avtx_cidr"]
  eip             = try(var.spoke_gws[3]["eip"],null)
  insane_mode_az  = var.spoke_gws[3]["gw_zone"]
  gw_size         = var.spoke_gws[3]["avtx_gw_size"]
  depends_on      = [aviatrix_spoke_ha_gateway.ha2]

  lifecycle {
    ignore_changes = [insane_mode_az]
  }
}

resource "aviatrix_spoke_ha_gateway" "ha4" {
  count           = local.gateway_count > 4 ? 1 : 0
  primary_gw_name = aviatrix_spoke_gateway.gw.id
  gw_name         = "${aviatrix_spoke_gateway.gw.gw_name}-${4}"
  insane_mode     = var.hpe
  subnet          = var.spoke_gws[4]["avtx_cidr"]
  eip             = try(var.spoke_gws[4]["eip"],null)
  insane_mode_az  = var.spoke_gws[4]["gw_zone"]
  gw_size         = var.spoke_gws[4]["avtx_gw_size"]
  depends_on      = [aviatrix_spoke_ha_gateway.ha3]

  lifecycle {
    ignore_changes = [insane_mode_az]
  }
}

resource "aviatrix_spoke_ha_gateway" "ha5" {
  count           = local.gateway_count > 5 ? 1 : 0
  primary_gw_name = aviatrix_spoke_gateway.gw.id
  gw_name         = "${aviatrix_spoke_gateway.gw.gw_name}-${5}"
  insane_mode     = var.hpe
  subnet          = var.spoke_gws[5]["avtx_cidr"]
  eip             = try(var.spoke_gws[5]["eip"],null)
  insane_mode_az  = var.spoke_gws[5]["gw_zone"]
  gw_size         = var.spoke_gws[5]["avtx_gw_size"]
  depends_on      = [aviatrix_spoke_ha_gateway.ha4]

  lifecycle {
    ignore_changes = [insane_mode_az]
  }
}

{% endif %}
{% if data.snat_policies or data.snat_policies == [] %}
resource "aviatrix_gateway_snat" "internet" {
  {% if data.configure_spoke_gw_hs %}
  count      = var.switch_traffic ? local.gateway_count : 0
  gw_name    = count.index == 0 ? "${aviatrix_spoke_gateway.gw.gw_name}" : "${aviatrix_spoke_gateway.gw.gw_name}-${count.index}"
  {% else %}
  count      = var.switch_traffic ? (var.spoke_ha ? 2 : 1) : 0
  gw_name    = count.index == 0 ? aviatrix_spoke_gateway.gw.gw_name : aviatrix_spoke_gateway.gw.ha_gw_name
  {% endif %}  
  snat_mode  = "customized_snat"
  sync_to_ha = false
  {% for policy in data.snat_policies %}
  snat_policy {
    {% if policy.src_ip %}
    src_cidr          = "{{policy.src_ip}}"
    {% endif %}
    {% if policy.src_port %}
    src_port          = "{{policy.src_port}}"
    {% endif %}
    {% if policy.dst_ip %}
    dest_cidr         = "{{policy.dst_ip}}"_ip
    {% endif %}
    {% if policy.dst_port %}
    dest_port         = "{{policy.dst_port}}"
    {% endif %}
    {% if policy.protocol %}
    protocol          = "{{policy.protocol}}"
    {% endif %}
    {% if policy.interface %}
    interface         = "{{policy.interface}}"
    {% endif %}
    {% if policy.connection.startswith("$") %}
    connection        = aviatrix_spoke_transit_attachment.attachment.transit_gw_name
    {% else %}
    connection        = "{{policy.connection}}"
    {% endif %}
    {% if policy.mark %}
    mark              = "{{policy.mark}}"
    {% endif %}
    {% if policy.new_src_ip.startswith("$") %}
      {% if data.configure_spoke_gw_hs %}
    snat_ips          = count.index == 0 ? aviatrix_spoke_gateway.gw.private_ip : local.ha_private_ip[count.index -1][0].private_ip
      {% else %}
    snat_ips          = count.index == 0 ? aviatrix_spoke_gateway.gw.private_ip : aviatrix_spoke_gateway.gw.ha_private_ip
      {% endif %}
    {% else %}
    snat_ips          = "{{policy.new_src_ip}}"
    {% endif %}
    {% if policy.new_src_port %}
    snat_port         = "{{policy.new_src_port}}"
    {% endif %}
    {% if policy.exclude_rtb %}
    exclude_rtb       = "{{policy.exclude_rtb}}"
    {% endif %}
    apply_route_entry = {{policy.apply_route_entry}}
  }
  {% endfor %}
  dynamic "snat_policy" {
    for_each = var.enable_spoke_egress ? var.vpc_cidr_for_snat : []

    content {
      src_cidr          = snat_policy.value
      protocol          = "all"
      interface         = "eth0"
      connection        = "None"
      {% if data.configure_spoke_gw_hs %}
      snat_ips          = count.index == 0 ? aviatrix_spoke_gateway.gw.private_ip : local.ha_private_ip[count.index -1][0].private_ip
      {% else %}
      snat_ips          = count.index == 0 ? aviatrix_spoke_gateway.gw.private_ip : aviatrix_spoke_gateway.gw.ha_private_ip
      {% endif %}      
      apply_route_entry = true
    }
  }
}
{% endif %}

resource "aviatrix_spoke_transit_attachment" "attachment" {
  spoke_gw_name   = aviatrix_spoke_gateway.gw.gw_name
  {% if data.configure_gw_name %}
  transit_gw_name = var.transit_gw
  {% else %}
  transit_gw_name = "aws-${local.region[var.region]}-transit-gw"
  {% endif %}
  {% if not data.pre_v2_22_3 %}
  enable_max_performance = var.hpe ? var.max_hpe_performance : null
  {% endif %}
  {% if data.configure_spoke_gw_hs %}
  depends_on = [
    aviatrix_spoke_ha_gateway.ha1, 
    aviatrix_spoke_ha_gateway.ha2,
    aviatrix_spoke_ha_gateway.ha3,
    aviatrix_spoke_ha_gateway.ha4,
    aviatrix_spoke_ha_gateway.ha5,
  ]
  {% endif %}  
  route_tables    = [for k, v in var.route_tables : aws_route_table.aviatrix_managed[k].id if var.route_tables[k].ctrl_managed == "True"]
}

{% if data.configure_transit_gw_egress %}
resource "aviatrix_spoke_transit_attachment" "attachment_egress" {
  count = var.transit_gw_egress == "" ? 0 : 1
  spoke_gw_name   = aviatrix_spoke_gateway.gw.gw_name
  transit_gw_name = var.transit_gw_egress
  {% if not data.pre_v2_22_3 %}
  enable_max_performance = var.hpe ? var.max_hpe_performance : null
  {% endif %} 
  route_tables    = [for k, v in var.route_tables : aws_route_table.aviatrix_managed[k].id if var.route_tables[k].ctrl_managed == "True"]
}
{% endif %}

resource "aws_route_table" "aviatrix_managed" {
  for_each = var.route_tables
  vpc_id   = var.vpc_id
  tags     = merge(each.value.tags, { Org_RT = each.key })
}

resource "aviatrix_transit_firenet_policy" "spoke" {
  count                        = var.inspection ? 1 : 0
  transit_firenet_gateway_name = aviatrix_spoke_transit_attachment.attachment.transit_gw_name
  inspected_resource_name      = "SPOKE:${aviatrix_spoke_gateway.gw.gw_name}"
}

{% if data.pre_v2_23_0 %}
resource "aviatrix_segmentation_security_domain_association" "spoke" {
  count                = var.domain != "" ? 1 : 0
  transit_gateway_name = aviatrix_spoke_transit_attachment.attachment.transit_gw_name
  security_domain_name = var.domain
  attachment_name      = aviatrix_spoke_gateway.gw.gw_name
}
{% else %}
resource "aviatrix_segmentation_network_domain_association" "spoke" {
  count                = var.domain != "" ? 1 : 0
  transit_gateway_name = aviatrix_spoke_transit_attachment.attachment.transit_gw_name
  network_domain_name  = var.domain
  attachment_name      = aviatrix_spoke_gateway.gw.gw_name
}
{% endif %}

resource "aws_route" "pre_migration" {
  for_each = {
    for route in local.routes : "${route.destination}.${route.key}" => route
    if substr(route["target"], 0, 5) != "vpce-"
  }
  route_table_id            = aws_route_table.aviatrix_managed[each.value.key].id
  destination_cidr_block    = each.value.destination
  {% if data.filter_vgw_routes %}
  gateway_id                = split("-", each.value.target)[0] == "igw" ? (var.igw_id == "" ? aws_internet_gateway.IGW[0].id : var.igw_id) : null
  {% else %}
  gateway_id                = split("-", each.value.target)[0] == "vgw" ? each.value.target : (split("-", each.value.target)[0] == "igw" ? (var.igw_id == "" ? aws_internet_gateway.IGW[0].id : var.igw_id) : null)
  {% endif %}
  {% if data.filter_tgw_routes == false %}
  transit_gateway_id        = split("-", each.value.target)[0] == "tgw" ? each.value.target : null
  {% endif %}
  nat_gateway_id            = split("-", each.value.target)[0] == "nat" ? each.value.target : null
  local_gateway_id          = split("-", each.value.target)[0] == "Igw" ? each.value.target : null # outpost gateway
  network_interface_id      = split("-", each.value.target)[0] == "eni" ? each.value.target : null
  vpc_peering_connection_id = split("-", each.value.target)[0] == "pcx" ? each.value.target : null
  {% if data.configure_gw_lb_ep %}
  vpc_endpoint_id           = split("-", each.value.target)[0] == "glb" ? substr(each.value.target,4,-1) : null
  {% endif %}

  # VPC gateway endpoints routes can't be added here, endpoint manages RTs

}

resource "aws_vpc_endpoint_route_table_association" "vpce_route" {
  for_each = {
    for route in local.routes : "${route.destination}.${route.key}" => route
    if substr(route["target"], 0, 5) == "vpce-"
  }
  route_table_id  = aws_route_table.aviatrix_managed[each.value.key].id
  vpc_endpoint_id = each.value["target"]
}

locals {
  routes = flatten([
    for rt_key, rt_val in var.route_tables : [
      for route in rt_val.routes : {
        key         = rt_key
        destination = route.destination
        target      = route.target
      }
    ]
  ])
  {% if not data.configure_gw_name %}
  region = {
    us-west-1      = "usw1"
    us-west-2      = "usw2"
    us-east-1      = "use1"
    us-east-2      = "use2"
    ca-central-1   = "cac1"
    sa-east-1      = "sae1"
    eu-west-1      = "euw1"
    eu-west-2      = "euw2"
    eu-west-3      = "euw3"
    eu-central-1   = "euc1"
    eu-north-1     = "eun1"
    ap-south-1     = "aps1"
    ap-southeast-1 = "apse1"
    ap-southeast-2 = "apse2"
    ap-northeast-1 = "apne1"
    ap-northeast-2 = "apne2"
    ap-northeast-3 = "apne3"
    cn-north-1     = "cnn1"
    cn-northwest-1 = "cnnw1"
  }
  {% endif %}
}

{% if data.migrate_natgw_eip and (data.snat_policies or data.snat_policies == []) %}
data "aws_ami" "ubuntu_server" {
  count = var.deploy_dummy_spokes ? 1 : 0

  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-lunar-23.04-amd64-server-*"]
  }
  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

data "aws_eip" "dummy_spoke" {
  count = var.deploy_dummy_spokes ? length(var.spoke_gws) - 2 : 0

  public_ip = var.spoke_gws[count.index + 2]["eip"]
}

resource "aws_network_interface" "dummy_spoke" {
  count = var.deploy_dummy_spokes ? length(var.spoke_gws) - 2 : 0

  subnet_id = aws_subnet.aviatrix_public[count.index + 2].id
  tags = merge(var.tags, {
    "Name"                      = "Aviatrix-eni@${aviatrix_spoke_gateway.gw.gw_name}-${count.index + 2}_eth0"
    "Aviatrix-Created-Resource" = "Do-Not-Delete-Aviatrix-Created-Resource"
    "Description"               = "Created by Aviatrix gateway ${aviatrix_spoke_gateway.gw.gw_name}-${count.index + 2}, please do NOT remove it."
  })
}

resource "aws_eip_association" "dummy_spoke" {
  count = var.deploy_dummy_spokes ? length(var.spoke_gws) - 2 : 0

  network_interface_id = aws_network_interface.dummy_spoke[count.index].id
  allocation_id        = data.aws_eip.dummy_spoke[count.index].id
}

resource "aws_instance" "dummy_for_aviatrix_spoke" {
  count = var.deploy_dummy_spokes ? length(var.spoke_gws) - 2 : 0

  ami           = data.aws_ami.ubuntu_server[0].id
  instance_type = "t3.micro"

  network_interface {
    network_interface_id = aws_network_interface.dummy_spoke[count.index].id
    device_index         = 0
  }

  tags = merge(var.tags, {
    "Name"                      = "aviatrix-${aviatrix_spoke_gateway.gw.gw_name}-${count.index + 2}"
    "Aviatrix-Created-Resource" = "Do-Not-Delete-Aviatrix-Created-Resource"
    "HA"                        = "True"
    "Type"                      = "gateway"
  })
}
{% endif %}