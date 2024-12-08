import os
import ntpath
import math
from pathlib import Path
from exif import Image
import json
import re


class Process:
    """
    Classe pour traiter des images et extraire leurs données EXIF.

    Attributes:
        USER (str): Nom de l'utilisateur courant.
        result_json_file (JsonFile): Fichier JSON pour sauvegarder les données EXIF extraites.
        nbFile (int): Nombre de fichiers traités.
        listTraitee (list): Liste des fichiers déjà traités.
        path (str): Chemin du répertoire contenant les images.
        photo_files_list (list): Liste des chemins des fichiers images valides.
    """
    USER = os.environ.get("USER")

    def __init__(self, path: str = f"/Users/{USER}/Desktop/images") -> None:
        """
        Initialise l'objet Process.

        Args:
            path (str): Chemin vers le répertoire contenant les images.
        """
        self.result_json_file = None
        self.nbFile = 0
        self.listTraitee = []
        self.path = None
        self.photo_files_list = None
        if path:
            self.__set_path(path)
        self.__print_log()

    def __print_log(self) -> None:
        """
        Affiche des informations de diagnostic lors de l'initialisation.
        """
        print(f"initialisation :")
        print(f"chemin : {self.path}")
        print(f"{len(self.photo_files_list)} images trouvées.")

    def __set_path(self, path: str) -> None:
        """
        Définit le chemin du répertoire contenant les images.

        Args:
            path (str): Chemin du répertoire.

        Raises:
            Exception: Si le chemin spécifié n'existe pas.
        """
        if os.path.exists(path):
            self.path = path
            self.__filtered_file_list()
            self.result_json_file = JsonFile(self.path)
        else:
            raise Exception(f"le chemein '{path}' n'existe pas.")

    def __filtered_file_list(self) -> None:
        """
        Filtre les fichiers du répertoire pour ne conserver que les images au format JPG.
        """
        files = os.listdir(self.path)
        self.photo_files_list = [
            f"{self.path}/{f}" for f in files if not f.startswith('.') and re.match(pattern=r'.*\.(jpg|JPG)$', string=f)
        ]
        if len(self.photo_files_list) == 0:
            raise Exception("Aucune image trouvé!")

    def __get_dir(self) -> str:
        """
        Récupère le nom du répertoire courant.

        Returns:
            str: Nom du répertoire courant.
        """
        return self.path.split('/')[-1]

    def get_exif(self) -> int:
        """
        Extrait les données EXIF des images et les sauvegarde dans un fichier JSON.

        Returns:
            int: Nombre d'images traitées.

        Raises:
            Exception: En cas d'erreur lors du traitement des images.
        """
        try:
            next_id = AutoId()  # gère les id
            for img_path in self.photo_files_list:
                image = OneImage(path=img_path, next_id=next_id.get_id())
                self.result_json_file.addFileContent(image.extractExif())
            self.result_json_file.writeFile()
            return len(self.result_json_file.fileContent)
        except Exception as e:
            raise Exception(f"get_exif : {str(e)}")


class AutoId():
    """
    Classe pour générer des identifiants uniques incrémentaux.

    Attributes:
        current_id (int): Dernier identifiant généré.
    """

    def __init__(self):
        """
        Initialise la classe AutoId avec un identifiant de départ à 0.
        """
        self.current_id = 0

    def get_id(self) -> int:
        """
        Retourne un nouvel identifiant unique incrémenté.

        Returns:
            int: L'identifiant unique.
        """
        unique_id = self.current_id
        self.current_id += 1
        return unique_id


class OneImage():
    def __init__(self, path: str, next_id: int):
        self.next_id = next_id
        self.path = path

    def extractExif(self):
        with open(self.path, 'rb') as src:
            img = Image(src)
            exifDict = {}
            try:
                exifDict["id"] = self.next_id
                exifDict["fichier"] = ntpath.basename(self.path)
                exifDict["nom"] = f"Mon image {Path(self.path).stem}"
                exifDict["focale"] = f"{img.get('focal_length')} mm"
                exifDict["Vitesse"] = f"{self.get_exposure_time(img=img)} sec."
                exifDict["ouverture"] = f"F/{img.get('f_number')}"
                exifDict["iso"] = f"{img.get('photographic_sensitivity')} iso"
                exifDict["comment"] = ""
            except:
                with open(self.path, 'rb') as src1:
                    img = Image(src1)
                    exifDict["id"] = self.next_id()
                    exifDict["fichier"] = ntpath.basename(self.path)
                    exifDict["nom"] = Path(self.path).stem
                    exifDict["comment"] = "pas de données exif trouvées sur cette image."
            finally:
                return exifDict

    def get_exposure_time(self, img:Image) -> str:
        exposure_time = img.get('exposure_time')
        if exposure_time and exposure_time < 1:
            expt = f"1/{math.floor(1 / exposure_time)}"
        elif exposure_time:
            expt = math.floor(exposure_time)
        else:
            expt = 0
        return str(expt)


class JsonFile():
    def __init__(self, path: str):
        self.fileContent = []
        self.path = f"{path}/data.JSON"

    def addFileContent(self, objet):
        self.fileContent.append(objet)

    def getFile(self):
        return self.fileContent

    def writeFile(self):
        tab = json.dumps(self.fileContent)
        f = open(self.path, "w")  # ecrase le contenu précédent
        f.write(tab)
        f.close()
