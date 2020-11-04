import subprocess
import os
import bs4
from bs4 import Tag

class BioformatsFileConversion:
    def run_showinf_get_xml_images(self, target_file_path):
        if os.path.isfile(target_file_path):
            input_norm_path = os.path.normpath(target_file_path)

            output = subprocess.run(["showinf", "-novalid", "-no-upgrade", "-omexml-only", "-nopix", "{}".format(input_norm_path)], shell=True, capture_output=True)

            output_string = output.stdout.decode(encoding='windows-1252')

            soup = bs4.BeautifulSoup(output_string, "lxml")

            children = soup.find_all("OME")

            ome_images = soup.find_all("image")

            image_dicts = []

            for image in ome_images:
                output_dict = self.recusrively_generate_output_dict_from_tag(image, {})
                image_dicts.append(output_dict)

            return image_dicts

        else:
            raise(Exception("Could not process file metadata"))



    def recusrively_generate_output_dict_from_tag(self, input_tag: Tag, output_dict: dict):
        if isinstance(input_tag, Tag):
            output_dict.update(input_tag.attrs)

            for content in input_tag.contents:
                sub_output_dict = self.recusrively_generate_output_dict_from_tag(content, {})
                if content.name is not None and len(sub_output_dict) > 0:
                    if content.name in output_dict:
                        output_dict[content.name].append(sub_output_dict)
                    else:
                        output_dict[content.name] = [sub_output_dict]

        return output_dict


    def run_bfconvert_tiff(self, target_input_path, target_output_dir):
        if not os.path.isdir(target_output_dir):
            os.mkdir(target_output_dir)

        if os.path.isfile(target_input_path):

            path_split = os.path.split(target_input_path)
            path_ext_split = os.path.splitext(path_split[1])

            images = self.run_showinf_get_xml_images(target_input_path)

            print("Begin output of {} images from {}".format(len(images), target_input_path))

            for image in images:
                image_index = int(image['id'].split(":")[1])

                output_path = "{}\\{}_{}_{}.tiff".format(target_output_dir, path_ext_split[0], image['name'], image_index)
                norm_output_path = os.path.normpath(output_path)
                input_norm_path = os.path.normpath(target_input_path)

                subprocess.run(["bfconvert", "-series", "{}".format(image_index), "{}".format(input_norm_path), "{}".format(norm_output_path)], shell=True, capture_output=True)
                print("Dumped {} from {}".format(norm_output_path, input_norm_path))

            print("Completed output of {} images from {}".format(len(images), target_input_path))

        else:
            raise(Exception("Input must be OME images"))


    def __init__(self):
        pass


file_converter = BioformatsFileConversion()

input_path = os.path.join("C:\\", "temp", "Images", "Library.mvd2")
output_path = os.path.join("C:\\", "temp", "Images", "Library_Output")

file_converter.run_bfconvert_tiff(input_path, output_path)