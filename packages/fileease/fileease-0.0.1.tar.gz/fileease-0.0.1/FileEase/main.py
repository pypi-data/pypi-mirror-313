import os
import sys
import pikepdf
from PIL import Image
from tqdm import tqdm
import subprocess
from pypdf import PdfMerger, PdfReader, PdfWriter


class FileEase:
    def __init__(self):
        self.libreoffice_path = os.getenv("LIBREOFFICE_PATH")
        if self.libreoffice_path is None:
            self.libreoffice_path: str = "libreoffice"
        if sys.platform == "win32":
            self.libreoffice_path: str = self.__get_libreoffice_path()

    def __convert_to_pdf(self, input_file: str, output_folder: str, output_file_name: str = None) -> bool:
        if not os.path.isfile(input_file):
            raise FileNotFoundError(f"Input file '{input_file}' not found.")
        if not os.path.isdir(output_folder):
            raise FileNotFoundError(f"Output folder '{output_folder}' not found.")
        try:
            subprocess.run(
                [self.libreoffice_path, "--headless", "--convert-to", "pdf", input_file, "--outdir", output_folder],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            if output_file_name is not None:
                os.rename(os.path.join(output_folder, os.path.basename(input_file)), os.path.join(output_folder, output_file_name))
            return True
        except (FileNotFoundError, Exception):
            return False

    @staticmethod
    def __get_libreoffice_path() -> str | None:
        for path in os.getenv("PATH").split(os.pathsep):
            full_path: str = os.path.join(path, "soffice.exe")
            if os.path.isfile(full_path):
                return full_path
        return ""

    @staticmethod
    def image_to_pdf(input_path: list[str], output_path: str, output_pdf_name: str) -> bool:
        images: list[Image] = []
        if not output_pdf_name:
            output_pdf_name = "output"
        for img_path in input_path:
            img: Image = Image.open(img_path)
            if img.mode != "RGB":
                img: Image = img.convert("RGB")
            images.append(img)
        images[0].save(output_path + os.path.basename(output_pdf_name) + ".pdf", save_all=True, append_images=images[1:], resolution=100.0, quality=95)
        return True

    def doc_to_pdf(self, input_file: str, output_folder: str) -> bool:
        return self.__convert_to_pdf(input_file, output_folder)

    def ppt_to_pdf(self, input_file: str, output_folder: str) -> bool:
        return self.__convert_to_pdf(input_file, output_folder)
 