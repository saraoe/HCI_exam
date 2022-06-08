'''
util functions
'''
import streamlit as st
from zipfile import ZipFile
from glob import glob
import os
from PIL import Image


def v_spacer(height: int, sb: bool=False) -> None:
    '''
    creating vertical space in streamlit app

    Args:
        height (int): determines height of space
        sb (bool): if space should be added in sidebar
    '''
    for _ in range(height):
        if sb:
            st.sidebar.write('\n')
        else:
            st.write('\n')


def remove_files(folder: str):
    '''
    removes files in folder

    Args:
        folder (str): name of folder
    '''
    for file in glob(f'{folder}/*'):
        os.remove(file)


def create_zip():
    '''
    creating the zip with anonymized texts
    '''
    zipObj = ZipFile("anonymized_texts/texts.zip", "w")
    # Add multiple files to the zip
    for text in glob("anonymized_texts/*.txt"):
        zipObj.write(text)
    # close the Zip File
    zipObj.close()

    ZipfileDotZip = "anonymized_texts/texts.zip"

    with open(ZipfileDotZip, "rb") as f:
        bytes = f.read()
    return bytes


def resize_image(image, new_size):
    width, height = image.size
    new_sizes = int(width*new_size), int(height*new_size)
    return image.resize(new_sizes)