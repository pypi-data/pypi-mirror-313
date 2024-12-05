# temp fix to reduce annoying warnings
import warnings
warnings.filterwarnings(action='ignore', module='.*paramiko.*')

from . import __app_name__

from thestage.controllers import base_controller, container_controller, instance_controller, project_controller, \
    config_controller

base_controller.app.add_typer(container_controller.app, name="container")
base_controller.app.add_typer(instance_controller.app, name="instance")
base_controller.app.add_typer(project_controller.app, name="project")
base_controller.app.add_typer(config_controller.app, name="config")


def main():
    import thestage.config
    base_controller.app(prog_name=__app_name__)
