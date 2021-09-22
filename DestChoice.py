from read_control_file import ReadControl
from load_model_specifications import LoadModelSpecificationsDC
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

class DestChocie(object):
    """
    This is the base class for main destination choice model.

    Inputs:
        argv - path of "dc_mc_property.xml"
        model_id - index of "Model_Identity_Number" in "dc_mc_property.xml"
    """

    def __init__(self, property_file, model_id):

        #initializing variables
        self.file = property_file        
        self.id = int(model_id)
        self.socio = None
        self.matrix = {}
        self.keepresult = {}
        self.is_uni = cog.is_uni(self.id)
        
    def load_values(self,log):    
        #Get values from the dc_mc_property.xml file
        #returns an object with many attributes
        self.values = ReadControl(self.file, self.id)
        
        #range list from 1 to 919 that is used for columns and row indexs through out the script
        self.frame = [zone for zone in range(self.values.taz_start_id, self.values.taz_end_id + 1)]
        
        #Retruns all the specifications from the xml file
        self.control = LoadModelSpecificationsDC(self.values.model_specs)
        log.ini_log(self.control.xml_root.attrib["Name"])
        log.write_values(self.control, "control")
                                               

        #Creates a 0/1 vector for zones that are inside the model zones 
        self.model_zones = cog.get_model_zones(start=self.values.taz_start_id,
                                               end=self.values.taz_end_id,
                                               model_start=self.values.taz_model_start_id,
                                               model_end=self.values.taz_model_end_id)
                                               
        #If panda is None type load pandas table
        if self.control.input_panda:
            #Loads panda table into memory as a df
            self.panda = cog.read_file(self.control.input_panda, self.frame, "zone")
            

    #Method that read all the socio tables inputs
    #iterates through the socio file list and check if is a df instance to join to data to the main se df 
    def load_socio(self):
        for t in self.control.input_socio:            
            input_f, index = t
            if isinstance(self.socio, pd.DataFrame):
                temp = cog.read_file(input_f, self.frame, index.lower())
                self.socio = self.socio.merge(temp, how="left", left_index=True, right_index=True)
            else:
                self.socio = cog.read_file(input_f, self.frame, index.lower())
            
            if self.is_uni and index.lower() == "zone":
                uni_vals = self.socio.loc[self.values.univ_cubeid].sum()
                self.socio.loc[self.values.univ_cubeid] = 0
                self.socio.loc[self.values.univ_super] = uni_vals     
        self.socio = self.socio.fillna(0)
   
        
    #Method that iterates the skims file list and loads all the matrices into a dict object
    def load_skims(self):
        for skim in self.control.input_skims:
            name = cog.get_file_name(skim)
            self.matrix[name] = cog.load_skim(skim, self.frame)
            if self.is_uni:
                self.matrix[name] = cog.avg_uni(self.matrix[name], self.values.univ_cubeid, self.values.univ_super)
                
    #method that creates pop and emp variables in the socio table df
    #it creates 4 bins and puts values of 1 or 0 according to the density of the zone
    #the 4th values is the lowest density where as the 1st is the higesht. popden4 would be the lowest denisty threshold
    def set_denisty(self):
        for vari in self.values.density_variables:
            numbin = 4
            density, threshold = cog.set_denisty_variables(self.socio, vari, self.values.area_variable, numbin)
            for i in range(0, numbin):
                den_id = "{}den{}".format(vari, numbin)
                # it creates a colulm of either 1 or 0 if density is between
                self.socio[den_id] = ((density >= threshold[i]) & (density < threshold[i + 1])) * 1
                numbin -= 1

    #Method that uses several skim times to determine the accesibility for each zone
    #it sums the emp total accessibility for each zone as a added variable in the socio df
    def set_accessibility(self):
        minute = [30, 50]
        emp_vari = self.values.employment_variable
        for m in minute:
            name = "transit{}".format(m)
            empwithin = cog.set_accessibility_variables(m, self.matrix,
                                                        self.values.skim_data,
                                                        self.socio[emp_vari], self.frame)
            self.socio[name] = empwithin
    
    
    #Method that runs each model
    def run_models(self, log):

        #Get the xml specifications from control object
        root = self.control.xml_root

        #Determines if the modle is peak, offpeak, uni_pk etc and load the required module for each period 
        if "DestinationChoicePeakModel" == self.control.xml_root.attrib["Name"]:
            module = pk            

        elif "DestinationChoiceOffPeakModel" == self.control.xml_root.attrib["Name"]:
            module = op
        
        elif "UNMDestinationChoicePeakModel" == self.control.xml_root.attrib["Name"]:
            module = uni_pk
        
        elif "UNMDestinationChoiceOffPeakModel" == self.control.xml_root.attrib["Name"]:
            module = uni_op
 
        else:
            raw_input( "XML input file not found. Make sure the xml file exists\nThe program will exit after any key press")
            log.msg("XML input file not found. Make sure the xml file exists")
            sys.exit() 
                     
            
        print "Running models from {}.xml file".format(self.control.xml_root.attrib["Name"])
        self.matrix, self.socio = module.set_model_variables(self.matrix, self.socio)
        # Iterates trhough all the models that are set to run from the value xml tag
        for model_id in self.values.models_to_run:
            
            #Load model specifications by model id
            model = root.find(".//Model[@Id='{}']".format(model_id))
            log.msg("Running {} model".format(model.attrib.get("Name")))
            
            #Creates a df that will hold the values
            df = pd.DataFrame(0.0, index=self.frame, columns=self.frame)
            
            #Get the name of the model to call that function from the pk or op modules
            model_name = model.attrib.get("Name")
            
            #cretaes method that will be called according to name and module specifications
            methodToCall = getattr(module, model_name)
            
            #Load model attributes such as productions and attractions names
            if self.is_uni:
                attributes = cog.get_model_attributes(model,is_uni = True, enr_val = self.values.enrollment)
                result, model_filter = methodToCall(self.matrix, self.socio, df, self.values.univ_super)
            else:
                attributes = cog.get_model_attributes(model)
                result, model_filter = methodToCall(self.matrix, self.socio, df)
            log.write_values(attributes,model_name)
            #Loads into memory the products fieds from the panda table if the input panda field exists is not None
            if self.control.input_panda:                
                product = cog.get_panda(attributes["product_columns"], self.panda, self.values.taz_start_id, self.values.taz_end_id)

            #Normalization of the results and apply the filter and modelzones variables
            result = result.mask(result != 0).fillna(exp(result))
            result = result.mul(self.model_zones, axis=0)
            result = result.mul((model_filter), axis=0)
            
            #Get final results
            result = result.div(result.sum(), axis=1).fillna(0)
            
            if self.is_uni:
                univ_zone = pd.DataFrame(0.0, index=self.frame, columns=self.frame)
                univ_zone[self.values.univ_super] = 1
                if attributes["isProduct"]:
                    result = result.T
                    univ_zone = univ_zone.T
                result = univ_zone * result * attributes['trip_count']
                
            else:    
                result = result.T            
                #Results times productions, values are by row
                result = result.mul(product, axis=0)
                if attributes["isProduct"] is False:
                    result = result.T
                # Doubly constrained matrix balancing using the IPF procedure
                # Only does the ipf balancing if the model has attractoions
                if attributes.get("doubly_columns"):
                    rowtarget = cog.get_panda(attributes["doubly_columns"], self.panda, self.values.taz_start_id, self.values.taz_end_id)
                    log.msg("\nProcessing doubly constrained growth factor approach...\n")
                    result = cog.balancing_matrix(result, product, rowtarget, log)

            #Check if the model has an outputfile
            #If not its added to the keepresult variable
            if model_id in self.control.output_files.keys():
                
                #Check if the model needs to aggregate other results from the index specification from the xml file
                if self.control.output_files[model_id].get("index"):
                    for index in self.control.output_files[model_id].get("index").split(","):
                        result += self.keepresult[int(index)]

                log.msg("Total trips: {}\n\n".format(result.sum().sum()))
                
                #results exported to csv
                result.to_csv(self.control.output_files[model_id].get("path"), float_format='%.5f')
               
                if self.is_uni:
                    cog.aggregated_result_validation(result, self.matrix["dist"], self.socio, self.control.output_files[model_id].get("path"),is_uni = True, superzone = self.values.univ_super)
                else:
                    #creates summary aggregation of each result
                    cog.aggregated_result_validation(result, self.matrix["dist"], self.socio, self.control.output_files[model_id].get("path"))
            else:
                self.keepresult[model_id] = result

if __name__ == '__main__':
    from datetime import datetime
    log = Logger(os.getcwd())
    try:
        dc = DestChocie(sys.argv[1], sys.argv[2])
        dc.load_values(log)
        dc.load_socio()
        dc.load_skims()
        dc.set_denisty()
        dc.set_accessibility()
        dc.run_models(log)
    except Exception, e:
       # If an error occurred, print line number and error message
       import traceback, sys
       tb = sys.exc_info()[2]
       log.error("Line {}".format(tb.tb_lineno))
       log.error(e.message)    
        log.close()
    log.close()    