{{ data.var_route_tables }}

module "{{ data.vnet_name }}" {
  source                  = "{{ data.module_source }}"
{% if data.spoke_ha == "false" %}
  spoke_ha                = false
{% endif %}
{% if data.configure_gw_name %}
  spoke_gw_name           = "{{ data.spoke_gw_name }}"
  transit_gw              = "{{ data.transit_gw_name }}"
{% endif %}
  vnet_name               = "{{ data.vnet_name }}"
  vnet_cidr               = {{ data.vnet_cidr }}
  avtx_cidr               = "{{ data.avtx_cidr }}"
  hpe                     = {{ data.hpe }}
  avtx_gw_size            = "{{ data.avtx_gw_size }}"
  region                  = "{{ data.region }}"
  use_azs                 = {{ data.use_azs }} # Set to false if region above doesn't support AZs
  resource_group_name     = "{{ data.resource_group }}"
  main_rt_count           = {{ data.main_rt_count }}
{% if data.onboard_account %}
  account_name            = aviatrix_account.azure_{{data.account_name}}.account_name
{% else %}
  account_name            = var.account_name
{% endif %}
  route_tables            = {{ data.route_tables }}
{% if data.domain is not none %}
  domain                  = "{{data.domain}}"
{% endif %}
{% if data.inspection is not none %}
  inspection              = {{data.inspection}}
{% endif %}
{% if not data.pre_v2_22_3 and data.max_hpe_performance is not none %}
  max_hpe_performance     = {{ data.max_hpe_performance }}
{% endif %}
  switch_traffic          = false
  disable_bgp_propagation = {{ data.disable_bgp_propagation }} # Used to configure aviatrix_managed_main RTs
{% if data.spoke_gw_tags is defined %}
  tags                    = {{data.spoke_gw_tags}}
{% endif %}
{% if data.configure_subnet_groups %}
  subnet_groups = {
    {% if data.subnet_groups %}
    {% for grp in data.subnet_groups %}
    {{grp["group_name"]}} = {
      group_name = "{{grp["group_name"]}}"
      subnet_name = "{{grp["subnet_name"]}}"
      cidr = "{{grp["cidr"]}}"
    },
    {% endfor %}
    {% endif %}
  }
  inspected_subnet_groups = [
    {% if data.subnet_groups_inspected %}
    {% for grp in data.subnet_groups_inspected %}
      "{{grp}}",
    {% endfor %}
    {% endif %}
  ]
{% endif %}
{% if data.spoke_advertisement %}
  spoke_adv           = "{{data.spoke_advertisement}}"
{% endif %}
{% if data.spoke_routes %}
  spoke_routes        = "{{data.spoke_routes}}"
{% endif %}
{% if data.configure_main_route_table_prefix | length > 0 %}
  main_route_table_prefix = "{{data.main_route_table_prefix}}"
{% endif %}
  providers = {
    azurerm = azurerm.{{ data.provider }}
  }
}
