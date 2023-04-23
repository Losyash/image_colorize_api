import os
import requests
import _thread as thread
from uuid import uuid4
import urllib

import numpy as np
from skimage.filters import gaussian
from PIL import Image

def get_model_bin(url, output_path):
    # print('Getting model dir: ', output_path)
    if not os.path.exists(output_path):
        create_directory(output_path)

        urllib.request.urlretrieve(url, output_path)

        # cmd = "wget -O %s %s" % (output_path, url)
        # print(cmd)
        # os.system(cmd)

    return output_path