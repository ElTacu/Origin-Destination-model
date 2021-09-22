#
# This code are developed for destination and mode choice models for MRCOG in an open-source language called Python by Daehyun You.
# Date: August 15, 2015
# Email: daehyun.you@gatech.edu
#
# Modifed by Daniel Jimenez to read inputs from a xml file instead of an excel file
# All attributes come from the read dc_mc_property.xml file through the read_control class.
# djimenez@mrcog-nm.gov 12/22/16

# Notes
from xml.etree import ElementTree as etree
import os


class LoadModelSpecificationsDC(object):
    """
    This is the base class for reading an xml control file.

    Inputs: 
        filename - File name of the xml specification file        
    """

    def __init__(self, filename):

        self.filename = filename

        self.xml_root = etree.parse(filename).getroot()

        # Skims are the matrix data tabs in the xml
        self.input_skims = []
        self.input_socio = []
        self.input_panda = None
        self.output_files = {}

        self.read_input_data()

    """
    Read information of input and output data such as file name, file path (directory), and file extension
    """

    def read_input_data(self):

        inputData = self.xml_root.find("InputData")
        outputData = self.xml_root.find("OutputData")

        for skim in inputData.findall(".//SkimData/Source"):
            skim_file = os.path.join(
                skim.attrib["Folder"], skim.attrib["FileName"])
            self.input_skims.append(skim_file)

        for se in inputData.findall(".//SocioEconomicData/Source"):
            se_file = os.path.join(se.attrib["Folder"], se.attrib["FileName"])
            self.input_socio.append([se_file, se.attrib["CubeID"]])

        for panda in inputData.findall(".//ProductionAttraction/Source"):
            panda_file = os.path.join(
                panda.attrib["Folder"], panda.attrib["FileName"])
            self.input_panda = panda_file

        for ouput in outputData.findall(".//Output"):
            if ouput.attrib.get("FileName"):
                model_key = int(ouput.attrib["Id"])
                output_path = os.path.join(ouput.attrib["Folder"], ouput.attrib["FileName"])
                if ouput.attrib.get("Index"):
                    self.output_files[model_key] = {"path": output_path, "index": ouput.attrib["Index"]}
                else:
                    self.output_files[int(model_key)] = {"path": output_path}               

                    
class LoadModelSpecificationsMC(object):
    """
    This is the base class for reading an xml control file.

    Inputs: 
        filename - File name of the xml specification file        
    """

    def __init__(self, filename):

        self.filename = filename

        self.xml_root = etree.parse(filename).getroot()

        # Skims are the matrix data tabs in the xml
        self.input_skims = []
        self.input_walk = []
        self.trip_data = {}
        self.output_files = {}

        self.read_input_data()

    """
    Read information of input and output data such as file name, file path (directory), and file extension
    """

    def read_input_data(self):

        inputData = self.xml_root.find("InputData")
        outputData = self.xml_root.find("OutputData")

        for skim in inputData.findall(".//SkimData/Source"):
            skim_file = os.path.join(
                skim.attrib["Folder"], skim.attrib["FileName"])
            self.input_skims.append(skim_file)
            
        for walk in inputData.findall(".//WalkRelatedData/Source"):
            walk_file = os.path.join(
                walk.attrib["Folder"], walk.attrib["FileName"])
            self.input_walk.append(walk_file)

        for trip in inputData.findall(".//TripData/Input"):
            model_key = int(trip.attrib["Id"])
            trip_path = os.path.join(trip.attrib["Folder"], trip.attrib["FileName"])
            self.trip_data[int(model_key)] = {"path": trip_path}

        for ouput in outputData.findall(".//Output"):
            model_key = int(ouput.attrib["Id"])
            output_path = os.path.join(ouput.attrib["Folder"], ouput.attrib["FileName"])
            self.output_files[int(model_key)] = {"path": output_path}