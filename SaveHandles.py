import os
import xml.etree.ElementTree
from collections import namedtuple
from datetime import datetime
from typing import List

from zippy.zComp import CompressLib
import xml.etree.ElementTree as Et
from xml.dom import minidom

backup_root = ".\\backups\\"

Backup = namedtuple("Backup", ["name", "date"])


class GameSave:
    def __init__(self, name: str = ""):
        self.game_name = name
        self.folder_targets: List[str] = []
        self.backups: List[Backup] = []

    def make_backup(self, backup_name: str):
        time_str = datetime.now().strftime("%Y/%m/%d-%H:%M")
        new_backup = Backup(name=backup_name, date=time_str)
        game_backup_path = backup_root + self.game_name + '\\'
        if not os.path.exists(game_backup_path):
            os.makedirs(game_backup_path)

        CompressLib.compress(game_backup_path + backup_name + " " + time_str, self.folder_targets)
        self.backups.append(new_backup)

    @staticmethod
    def file_name(path: str) -> str:
        slash_index = path.rfind('\\')
        if slash_index != -1:
            return path[slash_index + 1:]
        else:
            return path

    def print_info(self):
        print(f"Title: {self.game_name}\n")
        for n, target in enumerate(self.folder_targets):
            print(f"    Path: {target}")


class SaveHandler:

    def __init__(self):
        self.xml_name: str = "archive.xml"
        self.SaveList: List[GameSave] = []
        if not os.path.exists(self.xml_name):
            with open(self.xml_name, 'w') as file:
                file.write("")

    def __getitem__(self, item: int) -> GameSave:
        return self.SaveList[item]

    def load_from_file(self):
        self.SaveList.clear()
        try:
            tree = Et.parse(self.xml_name)
        except xml.etree.ElementTree.ParseError:
            print("Invalid archive.xml. A valid file will be generated after at least 1 game is added")
            return
        root = tree.getroot()

        for element in root.findall("Game"):
            game = GameSave(element.find("Name").text)
            game.folder_targets.clear()
            paths = element.find("Paths")
            for path in paths.findall("Path"):
                game.folder_targets.append(path.text)
            backup_info = element.find("Backups")
            for backup in backup_info.findall("Backup"):
                new_backup = Backup(backup.find("Name").text, backup.find("Time").text)
                game.backups.append(new_backup)

            self.SaveList.append(game)

    def write_out(self):
        root = Et.Element("GameSaves")

        for game in self.SaveList:
            game_root = Et.SubElement(root, "Game")

            game_name = Et.SubElement(game_root, "Name")
            game_name.text = game.game_name

            file_paths = Et.SubElement(game_root, "Paths")
            for path in game.folder_targets:
                path_element = Et.SubElement(file_paths, "Path")
                path_element.text = path

            backup_root = Et.SubElement(game_root, "Backups")
            for backup in game.backups:
                backup_element = Et.SubElement(backup_root, "Backup")
                name_element = Et.SubElement(backup_element, "Name")
                name_element.text = backup.name
                time_element = Et.SubElement(backup_element, "Time")
                time_element.text = backup.date

        rough_string = Et.tostring(root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        root = reparsed.toprettyxml(indent="  ")

        with open(self.xml_name, "w", encoding="utf-8") as file:
            file.write(root)
