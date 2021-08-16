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
