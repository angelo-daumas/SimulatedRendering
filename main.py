import json
import time
from PIL import Image
from rasterspace import RasterSpace
import os
import traceback

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class Tags:
    SYS = bcolors.OKGREEN + "[SYSTEM]" + bcolors.ENDC
    ERR = bcolors.FAIL + "[ERROR]" + bcolors.ENDC
    IN = bcolors.OKBLUE + "[{}?]" + bcolors.ENDC + " "

def do_file(filename:str):
    with open(f'tests/{filename}.json') as f:
        data = json.load(f)

        screen = RasterSpace(data)
        
        start = time.process_time()
        screen.rasterize()
        end = time.process_time()
        print(f'{Tags.SYS} Finished rasterizing "{filename}". Took {end-start} seconds.')

        return Image.fromarray(screen.image)  # type: ignore

def main():
    while True:
        filename = input(f'{Tags.SYS} Please type in the name of a file in the "tests" folder to generate an image. Type /all to generate all images. Press enter to continue. \n{Tags.IN.format("file name")}')

        if not filename:
            break
        elif filename == "/all":
            for filename in os.listdir('tests/'):
                if filename.endswith('.json'):
                    filename = filename[:filename.rfind(".")]
                    print(f'{Tags.SYS} Rasterizing "{filename}"...')
                    do_file(filename).save(f'outputs/{filename}.png')
            break
        else:
            try:
                do_file(filename).show()
            except Exception:
                print(f"{Tags.ERR} Unable to process file. Please try again, or use another filename.")
                traceback.print_exc()

if __name__ == "__main__":
    main()