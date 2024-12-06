import logging
from .base_module import BaseModule

class ServiceModule(BaseModule):
    name = "service"

    def process(self, ssh_client):
        """Gère l'état d'un service Systemd sur un hôte distant."""
        service_name = self.params.get("name")
        desired_state = self.params.get("state")
        ssh_password = ssh_client.ssh_password

        if not service_name or not desired_state:
            logging.error("Les paramètres 'name' et 'state' sont requis pour le module service.")
            return

        # Traduire l'état souhaité en commande Systemd
        command = self._get_systemctl_command(service_name, desired_state, ssh_password)
        if not command:
            logging.error("État non supporté : %s", desired_state)
            return

        # Exécuter la commande sur l'hôte distant
        stdin, stdout, stderr = ssh_client.exec_command(command, get_pty=True)
        stdout.channel.recv_exit_status()

        errors = stderr.read().decode().strip()
        if errors:
            logging.error("Erreur lors de l'exécution de '%s' : %s", command, errors)
        else:
            logging.info("Service '%s' mis à jour à l'état '%s' avec succès.", service_name, desired_state)

    def _get_systemctl_command(self, service_name, state, password):
        """Traduit l'état souhaité en commande systemctl."""
        valid_states = {
            "started": f"echo {password} | sudo -S systemctl start {service_name}",
            "restarted": f"echo {password} | sudo -S systemctl restart {service_name}",
            "stopped": f"echo {password} | sudo -S systemctl stop {service_name}",
            "enabled": f"echo {password} | sudo -S systemctl enable {service_name}",
            "disabled": f"echo {password} | sudo -S systemctl disable {service_name}",
        }
        return valid_states.get(state)
