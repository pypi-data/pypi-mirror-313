import logging
import argparse
from .inventory_loader import load_inventory
from .ssh_client import connect_to_host
from .modules.copy_module import CopyModule
from .modules.apt_module import AptModule
from .modules.template_module import TemplateModule
from .modules.service_module import ServiceModule
from .modules.command_module import CommandModule
from .modules.sysctl_module import SysctlModule

# Configuration des logs
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


def execute_todos(inventory, todos):
    for host, info in inventory["hosts"].items():
        logging.info("Connexion au host '%s' (%s)...", host, info['ssh_address'])
        ssh_client = connect_to_host(info)
        if ssh_client:
            for task in todos:
                module_name = task["module"]
                params = task["params"]
                # Préparation du module à exécuter
                if module_name == "copy":
                    module = CopyModule(params)
                elif module_name == "apt":
                    module = AptModule(params)
                elif module_name == "template":
                    module = TemplateModule(params)
                elif module_name == "service":
                    module = ServiceModule(params)
                elif module_name == "command":
                    module = CommandModule(params)
                elif module_name == "sysctl":
                    module = SysctlModule(params)
                else:
                    logging.error("Module inconnu: %s", module_name)
                    continue

                module.process(ssh_client)
            ssh_client.close()
            logging.info("Connexion fermée pour %s", info['ssh_address'])


def main():
    parser = argparse.ArgumentParser(description="MyLittleAnsible")
    parser.add_argument("-i", "--inventory", required=True,
                        help="Fichier d'inventaire YAML")
    parser.add_argument("-f", "--todos", required=True,
                        help="Fichier de tâches YAML")
    args = parser.parse_args()

    # Charger l'inventaire et les tâches
    i_inventory = load_inventory(args.inventory)
    t_todos = load_inventory(args.todos)

    # Exécution des tâches
    execute_todos(i_inventory, t_todos)
