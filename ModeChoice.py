from read_control_file import ReadControl
from load_model_specifications import LoadModelSpecificationsMC
from logger import Logger
import mrcog_functions as cog
import dest_choice_pk_models as pk
import dest_choice_op_models as op
import univ_dc_pk_models as uni_pk
import univ_dc_op_models as uni_op
import pandas as pd
from scipy import exp
import sys
import os


class ModeChocie(object):
    """
    This is the base class for Mode Choice models

    Inputs:
    property_file - path and file name of "../dc_mc_property.txt"
    tod - Peak or Off-Peak
    model_id - 5 or 6 (5: main mode choice model for peak hour, 6: main mode choice model for off-peak hour)
    """
    def __init__(self, property_file, tod, model_id):

        self.file = property_file   
        self.id = int(model_id)
        self.data = None
        self.isautocalibrate = False
        self.isautozerocalibrate = False
        self.tol = 0.01
        self.damp = 1.0
        self.tod = tod
        self.aggregated_results = []
        self.bias_results = []

    def load_values(self,log):    
        self.values = ReadControl(self.file, self.id) #'mrcog_mc_control.txt')
    
        #range list from 1 to 919 that is used for columns and row indexs through out the script
        self.frame = [zone for zone in range(self.values.taz_start_id, self.values.taz_end_id + 1)]

        #Retruns all the specifications from the xml file
        self.control = LoadModelSpecificationsMC(self.values.model_specs)
        log.ini_log(self.control.xml_root.attrib["Name"])
        log.write_values(self.control, "control")                                               
                                

        ##Creates a 0/1 vector for zones that are inside the model zones 
        self.model_zones = cog.get_model_zones(start=self.values.taz_start_id,
                                               end=self.values.taz_end_id,
                                               model_start=self.values.taz_model_start_id,
                                               model_end=self.values.taz_model_end_id) 
                                               
    #Method that iterates the skims file list and loads all the matrices into a dict object
    def load_skims(self):
        for skim in (self.control.input_skims):
            name = cog.get_file_name(skim)
            self.matrix[name] = cog.load_skim(skim, self.frame)                                               
    
if __name__ == '__main__':
    from datetime import datetime
    log = Logger(os.getcwd())    
    ars = ["T:/tbd_mrcog/xml_files/dc_mc_property.xml", "pk" ,5]
    #try:
        # mc = ModeChocie(sys.argv[1],sys.argv[2],sys.argv[3])
    mc = ModeChocie(ars[0],ars[1],ars[2])
    mc.load_values(log)
    mc.load_skims()
        # dc.set_denisty()
        # dc.set_accessibility()
        # dc.run_models(log)
    # except Exception, e:
       ###If an error occurred, print line number and error message
       # import traceback, sys
       # tb = sys.exc_info()[2]
       # log.error("Line {}".format(tb.tb_lineno))
       # log.error(e.message)    
       # log.close()
      