import os
import py7zr


class CompressLib:
    @staticmethod
    def compress(archive_path, file_list):
        clean_path = archive_path.replace(':', '.')
        clean_path = clean_path.replace('/', '_')
        with py7zr.SevenZipFile(clean_path + ".7z", 'w') as archive:
            for file in file_list:
                arc = os.path.basename(file)
                archive.writeall(file, arcname=arc)

    @staticmethod
    def extract(archive_path, output_path):
        clean_path = archive_path.replace(':', '.')
        clean_path = clean_path.replace('/', '_')
        with py7zr.SevenZipFile(clean_path + ".7z", mode='r') as archive:
            archive.extractall(path=output_path)
