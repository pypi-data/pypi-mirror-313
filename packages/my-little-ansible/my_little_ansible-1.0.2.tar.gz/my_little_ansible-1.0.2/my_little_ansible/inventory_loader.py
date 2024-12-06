import yaml


def load_inventory(filename):
    """Charge le fichier d'inventaire."""
    with open(filename, 'r', encoding='utf-8') as file:
        inventory = yaml.safe_load(file)
    return inventory
