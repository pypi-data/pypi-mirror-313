import os
import logging
import paramiko
import posixpath
from .base_module import BaseModule

class CopyModule(BaseModule):
    name = "copy"

    def process(self, ssh_client):
        """Copie un fichier ou dossier vers un hôte distant."""
        src = self.params.get("src")
        dest = self.params.get("dest")
        backup = self.params.get("backup", False)
        ssh_password = ssh_client.ssh_password
        temp_dir = "/tmp"
        temp_dest = posixpath.join(temp_dir, os.path.basename(dest))
        isFile = os.path.isfile(src)

        if not src or not dest:
            logging.error("Les paramètres 'src' et 'dest' sont requis pour le module copy.")
            return

        try:
            # Établir une session SFTP pour la copie initiale
            sftp = ssh_client.open_sftp()
            self._upload_to_temp(sftp, src, temp_dest)
            sftp.close()

            # Gestion du backup et déplacement vers la destination finale
            self._handle_backup_and_move(ssh_client, temp_dest, dest, ssh_password, backup)

            logging.info("Fichier/dossier copié avec succès de %s vers %s.", src, dest)

        except Exception as e:
            logging.error("Erreur lors de la copie : %s", str(e))

    def _upload_to_temp(self, sftp, src, temp_dest):
        """Télécharge un fichier ou un dossier (avec son propre nom) vers un répertoire temporaire."""
        if not os.path.exists(src):
            raise FileNotFoundError(f"Le chemin local {src} n'existe pas.")

        if os.path.isdir(src):
            # Inclure le dossier source lui-même dans temp_dest
            remote_dir = posixpath.join(temp_dest, os.path.basename(src))
            self._upload_directory(sftp, src, remote_dir)
        else:
            # Copier un fichier directement dans temp_dest
            logging.info("Téléchargement du fichier %s vers %s.", src, temp_dest)
            sftp.put(src, temp_dest)
            remote_dir_without_file = posixpath.dirname(remote_dir)
            logging.info("Création du répertoire distant : %s", remote_dir_without_file)
            _mkdir_recursive(sftp, remote_dir_without_file)



    def _upload_directory(self, sftp, local_dir, remote_dir):
        """Upload récursif d'un répertoire, y compris son propre nom."""
        _mkdir_recursive(sftp, remote_dir)

        for item in os.listdir(local_dir):
            local_path = os.path.join(local_dir, item)
            remote_path = posixpath.join(remote_dir, item)

            if os.path.isdir(local_path):
                # Appel récursif pour les sous-dossiers
                self._upload_directory(sftp, local_path, remote_path)
            else:
                # Upload des fichiers
                logging.info("Téléchargement du fichier %s vers %s.", local_path, remote_path)
                sftp.put(local_path, remote_path)



    def _handle_backup_and_move(self, ssh_client, temp_dest, dest, password, backup):
        """Gère le déplacement avec backup via sudo."""
        commands = []

        # Vérifier si un backup est requis
        if backup:
            backup_dest = dest + ".bak"
            commands.append(f"if [ -e {dest} ]; then echo {password} | sudo -S mv {dest} {backup_dest}; fi")

        # Ajuster la commande mv en fonction de la structure
        if os.path.basename(temp_dest) == os.path.basename(dest):
            # Le fichier ou dossier doit être déplacé directement à la destination finale
            move_command = f"echo {password} | sudo -S mv {temp_dest} {dest}"
        else:
            # Le chemin cible est un répertoire, insérez le fichier ou dossier dedans
            move_command = f"echo {password} | sudo -S mv {temp_dest} {posixpath.join(dest, os.path.basename(temp_dest))}"

        commands.append(move_command)

        # Exécuter les commandes sur l'hôte distant
        for command in commands:
            logging.info("Exécution de la commande : %s", command)
            stdin, stdout, stderr = ssh_client.exec_command(command, get_pty=True)
            stdout.channel.recv_exit_status()

            errors = stderr.read().decode().strip()
            if errors:
                logging.error("Erreur lors de l'exécution de '%s' : %s", command, errors)
            else:
                logging.info("Commande exécutée avec succès : %s", command)

def _move_file(temp_dest, final_dest, ssh_client, password):
    """Déplace un fichier du répertoire temporaire vers la destination finale."""
    logging.info("Déplacement du fichier %s vers %s.", temp_dest, final_dest)





def _mkdir_recursive(sftp, remote_path):
    """Crée récursivement les répertoires sur le host distant."""
    dirs = []
    while True:
        try:
            sftp.stat(remote_path)
            break
        except IOError:
            dirs.append(remote_path)
            remote_path = posixpath.dirname(remote_path)
    for dir in reversed(dirs):
        try:
            sftp.mkdir(dir)
            logging.info("Création du répertoire distant : %s", dir)
        except IOError as e:
            logging.error("Erreur lors de la création du répertoire %s : %s", dir, str(e))
