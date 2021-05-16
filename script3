"""
Take the YAML file and corresponding data structure 
From this YAML data input source, use Jinja templating to generate configuration 

Exppected output 
-------------------
interface Ethernet10
  switchport mode access
  description "ACCESS PORT"
  switchport access vlan 10
  !
interface Ethernet20
  switchport mode access
  description "ACCESS PORT"
  switchport access vlan 20
  !
interface Ethernet30
  switchport mode trunk
  description "Trunk PORT"
  switchport trunk native vlan 1
  switchport trunk allowed vlan all
----
"""
import yaml
import jinja2

# place holder for full configuration
generate_config =''

# Open the Yaml file
yaml_file = "New_Vlan.yml"
with open(yaml_file) as f:
    template_vars = yaml.safe_load(f)
#print(template_vars)

# Open the J2 file  and create a J2 Object
template_file = "config2_template.j2"
with open(template_file) as f:
    jinja_template = f.read()
#print(jinja_template)
template = jinja2.Template(jinja_template)

# Save the final configuraiton to interface_configs
generate_config = template.render(template_vars)
with open("generate_config.txt", "w") as f:
      f.write(generate_config)
#print(template.render(template_vars))
