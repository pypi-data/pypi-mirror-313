import logging
from .base_module import BaseModule

class CommandModule(BaseModule):
    name = "command"

    def process(self, ssh_client):
        """Exécute une commande shell arbitraire sur un hôte distant."""
        command = self.params.get("command")
        shell = self.params.get("shell", "/bin/bash")

        if not command:
            logging.error("Le paramètre 'command' est requis pour le module command.")
            return

        full_command = f"{shell} -c \"{command}\""
        logging.info("Exécution de la commande : %s", full_command)

        try:
            stdin, stdout, stderr = ssh_client.exec_command(full_command, get_pty=True)
            exit_status = stdout.channel.recv_exit_status()

            # Log outputs
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()

            if exit_status == 0:
                logging.info("Commande exécutée avec succès. Sortie :\n%s", output)
            else:
                logging.error("Erreur lors de l'exécution de la commande. Code : %d, Erreur :\n%s", exit_status, error)

        except Exception as e:
            logging.error("Erreur lors de l'exécution de la commande : %s", str(e))
