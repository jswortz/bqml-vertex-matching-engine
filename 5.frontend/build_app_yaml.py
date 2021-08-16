import os
import jinja2

template_loader = jinja2.FileSystemLoader(searchpath="./")
template_env = jinja2.Environment(loader=template_loader)
template_file = "./app.yaml.template"
template = template_env.get_template(template_file)
output = template.render(env=os.environ)

of_flags = os.O_RDWR | os.O_CREAT
of = os.open('./app.yaml', flags=of_flags)
os.write(of, output.encode())
os.close(of)
