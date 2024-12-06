import logging
from .base_module import BaseModule


class AptModule(BaseModule):
    name = "apt"

    def process(self, ssh_client):
        """Installe ou désinstalle un paquet APT sur l'hôte distant."""
        package_name = self.params.get("name")
        state = self.params.get("state", "present")  # Par défaut, "present"
        ssh_password = ssh_client.ssh_password  # Récupérer le mot de passe SSH

        logging.info(
            "APT: Traitement du paquet '%s' avec état '%s'.", package_name, state)

        if not package_name:
            logging.error("Le paramètre 'name' est requis pour le module APT.")
            return

        # Vérification de l'état du paquet
        check_command = f"dpkg -l | grep -w {package_name}"
        stdin, stdout, stderr = ssh_client.exec_command(check_command)
        package_installed = stdout.read().decode().strip() != ""

        # If present and already installed, or absent and not installed, do nothing
        # Otherwise, install or remove the package
        if state == "present" and package_installed:
            logging.info(
                "APT: Paquet '%s' déjà installé. Status: OK.", package_name)
        elif state == "absent" and not package_installed:
            logging.info(
                "APT: Paquet '%s' déjà absent. Status: OK.", package_name)
        else:
            # Définir la commande en fonction de l'état souhaité
            if ssh_client.ssh_password is not None:
                command = f"echo {ssh_password} | sudo -S apt-get {'install' if state == 'present' else 'remove'} -y {package_name}"
            else:
                command = f"sudo apt-get {'install' if state == 'present' else 'remove'} -y {package_name}"

            try:
                stdin, stdout, stderr = ssh_client.exec_command(command)
                exit_code = stdout.channel.recv_exit_status()

                # Vérification du statut de la commande
                if exit_code == 0:
                    logging.info("APT: Paquet '%s' %s avec succès.",
                                 package_name, state)
                else:
                    logging.error("APT: Échec de l'opération '%s' pour '%s'. Erreur: %s",
                                  state, package_name, stderr.read(200).decode())
            except Exception as e:
                logging.error(
                    "Erreur lors de l'exécution du module APT: %s", str(e))
