import os
import sys

# Inserta el directorio raíz del proyecto (el que contiene la carpeta "app") en sys.path
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)
