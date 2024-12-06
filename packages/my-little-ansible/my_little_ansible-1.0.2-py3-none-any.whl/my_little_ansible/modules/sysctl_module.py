import logging
from .base_module import BaseModule

class SysctlModule(BaseModule):
    name = "sysctl"

    def process(self, ssh_client):
        """Modifie les paramètres du kernel sur un hôte distant."""
        attribute = self.params.get("attribute")
        value = self.params.get("value")
        permanent = self.params.get("permanent", False)
        ssh_password = ssh_client.ssh_password

        if not attribute or value is None:
            logging.error("Les paramètres 'attribute' et 'value' sont requis pour le module sysctl.")
            return

        try:
            # Commande pour appliquer la modification immédiatement
            command = f"echo {ssh_password} | sudo -S sysctl -w {attribute}={value}"
            self._execute_command(ssh_client, command)

            if permanent:
                # Commande pour rendre la modification permanente
                add_command = f"echo {ssh_password} | sudo -S tee -a /etc/sysctl.conf > /dev/null && echo '{attribute} = {value}' | sudo -S tee -a /etc/sysctl.conf > /dev/null"
                self._execute_command(ssh_client, add_command)

                # Recharger les paramètres persistants
                reload_command = f"echo {ssh_password} | sudo -S sysctl -p"
                self._execute_command(ssh_client, reload_command)

            logging.info("Paramètre '%s' modifié avec succès à '%s'. Permanent: %s", attribute, value, permanent)
        except Exception as e:
            logging.error("Erreur lors de la modification de l'attribut '%s': %s", attribute, str(e))

    def _execute_command(self, ssh_client, command):
        """Exécute une commande sur l'hôte distant."""
        stdin, stdout, stderr = ssh_client.exec_command(command, get_pty=True)
        stdin.write(f"{ssh_client.ssh_password}\n")
        stdin.flush()

        exit_status = stdout.channel.recv_exit_status()

        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()

        if exit_status != 0:
            logging.error("Erreur : %s", error)
            raise Exception(f"Commande échouée : {command}, Erreur : {error}")

        logging.info("Commande exécutée avec succès : %s", command)
        if output:
            logging.info("Sortie : %s", output)
