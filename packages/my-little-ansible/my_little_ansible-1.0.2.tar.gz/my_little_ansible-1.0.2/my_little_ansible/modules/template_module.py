import os
import logging
import posixpath
from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError
from .base_module import BaseModule

class TemplateModule(BaseModule):
    name = "template"

    def process(self, ssh_client):
        """Rend un template Jinja2 et le copie sur un hôte distant."""
        src = self.params.get("src")
        dest = self.params.get("dest")
        variables = self.params.get("vars", {})

        logging.info("Rendu du template %s vers %s avec les variables %s.", src, dest, variables)

        ssh_password = ssh_client.ssh_password
        temp_dir = "/tmp"
        temp_dest = posixpath.join(temp_dir, os.path.basename(dest))

        if not src or not dest:
            logging.error("Les paramètres 'src' et 'dest' sont requis pour le module template.")
            return

        try:
            # Étape 1: Rendre le template avec Jinja2
            rendered_content = self._render_template(src, variables)

            # Étape 2: Écrire le contenu rendu dans un fichier temporaire local
            local_temp_file = self._write_temp_file(rendered_content)

            # Étape 3: Copier le fichier temporaire local sur l'hôte distant
            sftp = ssh_client.open_sftp()
            sftp.put(local_temp_file, temp_dest)
            # remove local temp file
            os.remove(local_temp_file)
            sftp.close()

            # Étape 4: Déplacer le fichier temporaire vers la destination finale avec sudo
            self._move_to_final_destination(ssh_client, temp_dest, dest, ssh_password)

            logging.info("Template rendu et copié avec succès de %s vers %s.", src, dest)

        except TemplateSyntaxError as e:
            logging.error("Erreur de syntaxe dans le template %s : %s", src, str(e))
        except Exception as e:
            logging.error("Erreur lors du rendu ou de la copie du template : %s", str(e))

    def _render_template(self, src, variables):
        """Rend un template Jinja2 avec les variables fournies."""
        try:
            env = Environment(loader=FileSystemLoader(os.path.dirname(src)))
            template = env.get_template(os.path.basename(src))
            rendered_content = template.render(variables)
            logging.info("Template %s rendu avec succès.", src)
            return rendered_content
        except Exception as e:
            logging.error("Erreur lors du rendu du template : %s", str(e))
            raise

    def _write_temp_file(self, content):
        """Écrit le contenu rendu dans un fichier temporaire local."""
        temp_file_path = "./temp_rendered_template"
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(content)
        logging.info("Fichier temporaire local écrit à %s.", temp_file_path)
        return temp_file_path

    def _move_to_final_destination(self, ssh_client, temp_dest, dest, password):
        """Déplace un fichier de /tmp vers la destination finale en utilisant sudo."""
        command = f"echo {password} | sudo -S mv {temp_dest} {dest}"
        stdin, stdout, stderr = ssh_client.exec_command(command, get_pty=True)
        stdout.channel.recv_exit_status()

        errors = stderr.read().decode().strip()
        if errors:
            logging.error("Erreur lors du déplacement vers %s : %s", dest, errors)
        else:
            logging.info("Déplacement effectué avec succès vers %s.", dest)
