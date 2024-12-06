import paramiko
import logging


def connect_to_host(host_info):
    """Établit une connexion SSH avec l'hôte en utilisant Paramiko."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=host_info["ssh_address"],
            port=host_info.get("ssh_port", 22),
            username=host_info.get("ssh_user"),
            password=host_info.get("ssh_password"),
            key_filename=host_info.get("ssh_key_file"),
            passphrase=host_info.get("ssh_key_passphrase")
        )
        ssh.ssh_password = host_info.get("ssh_password")
        logging.info("Connexion établie avec %s", host_info['ssh_address'])
        return ssh
    except paramiko.AuthenticationException:
        logging.error("Échec d'authentification pour %s",
                      host_info['ssh_address'])
    except paramiko.SSHException as e:
        logging.error("Erreur SSH pour %s : %s", host_info['ssh_address'], {str(e)})
    return None
