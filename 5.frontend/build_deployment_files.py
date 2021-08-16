import os
import jinja2

template_loader = jinja2.FileSystemLoader(searchpath="./")
template_env = jinja2.Environment(loader=template_loader)
deployment_files = ["./app.yaml", "./dispatch.yaml"]

for deployment_file in deployment_files:
    template = template_env.get_template(deployment_file + ".template")
    output = template.render(env=os.environ)

    of_flags = os.O_RDWR | os.O_CREAT
    of = os.open(deployment_file, flags=of_flags)
    os.write(of, output.encode())
    os.close(of)


environment_ts = """export const environment = {
  production: {{ env_mode }},
  RECAI_PROJECT: '{{ env['RECAI_PROJECT'] }}',
  HP_PLACEMENT: '{{ env['HP_PLACEMENT'] }}',
  OYML_PLACEMENT: '{{ env['OYML_PLACEMENT'] }}',
  FBT_PLACEMENT: '{{ env['FBT_PLACEMENT'] }}',
  RVD_PLACEMENT: 'recently_viewed_default',
  GTM_CONTAINER_ID: '{{ env['GTM_CONTAINER_ID'] }}'
};
"""

template_loader = jinja2.BaseLoader()
template_env = jinja2.Environment(loader=template_loader)
for env_mode in ["", ".prod"]:
    template = template_env.from_string(environment_ts)
    stringified_env_mode = 'true' if env_mode == '.prod' else 'false'
    output = template.render(env=os.environ, env_mode=stringified_env_mode)

    deployment_file = "./src/environments/environment" + env_mode + ".ts"
    of_flags = os.O_RDWR | os.O_CREAT
    of = os.open(deployment_file, flags=of_flags)
    os.write(of, output.encode())
    os.close(of)
