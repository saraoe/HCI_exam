'''
util functions
'''
from zipfile import ZipFile
from glob import glob

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