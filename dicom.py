import datetime
import pydicom
import numpy as np
from pydicom.data import get_testdata_files
from skimage import img_as_uint, img_as_ubyte

def save_dicom(filename, patient, image):

    filename = filename + '.dcm'
    print(image.min(), image.max())
    image = img_as_ubyte(image)
    image = img_as_uint(image)
    image = np.asarray(image, dtype=np.uint16)

    filename_s = get_testdata_files("CT_small.dcm")[0]
    ds = pydicom.dcmread(filename_s)

    ds.Modality = 'CT'
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PixelRepresentation = 0

    ds.Columns = image.shape[1]
    ds.Rows = image.shape[0]
    ds.Width = image.shape[1]
    ds.Height = image.shape[0]

    name, age, weight, sex, comment = patient
    ds.PatientName = name
    ds.PatientAge = age
    ds.PatientWeight = weight
    ds.PatientSex = sex
    ds.AdditionalPatientHistory = comment

    # Set creation date/time
    dt = datetime.datetime.now()
    ds.ContentDate = dt.strftime('%Y%m%d')
    ds.ContentTime = dt.strftime('%H%M%S.%f')  # long format with micro seconds
    ds.SeriesInstanceUID = '1.3.6.1.4.1.5962.1.3.1.1.20040119072730.12322'
    ds.SOPInstanceUID = '1.3.6.1.4.1.9590.100.1.1.111165684411017669021768385720736873780'
    ds.SOPClassUID = 'Secondary Capture Image Storage'
    ds.StudyInstanceUID = '1.3.6.1.4.1.5962.1.2.1.20040119072730.12322'

    ds.PixelData = image.tobytes()

    ds.save_as(filename)


def load_dicom(filename):
    ds = pydicom.dcmread(filename)
    image = np.array(ds.pixel_array, dtype=np.uint8)
    name = ds.PatientName
    age = ds.PatientAge
    weight = ds.PatientWeight
    sex = ds.PatientSex
    comment = ds.AdditionalPatientHistory
    patient = (name, age, weight, sex, comment)
    print(patient)
    return image, patient


