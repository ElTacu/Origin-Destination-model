#
# This code are developed for destination and mode choice models for MRCOG in an open-source language called Python by Daehyun You.
# Date: August 15, 2015
# Email: daehyun.you@gatech.edu
#
# Modifed by Daniel Jimenez to read inputs from a xml file instead of a txt file for control properties.
# djimenez@mrcog-nm.gov 12/22/16

from xml.etree import ElementTree as etree


class ReadControl(object):
    """
    This is the base class for storing information in "dc_mc_property.xml"

    Inputs:
    path - path of "dc_mc_property.xml"
    model_id - "Model_Identity_Number" in models tags in file
    """

    def __init__(self, path, model_id):
        root = etree.parse(path).getroot()
        self.model_id = model_id

        # Model Zone ID System tag variables
        # Check child string to know variable input name
        self.taz_start_id = int(root.findtext("Model_Zone_ID_System/TAZ_Start_ID"))
        self.taz_model_start_id = int(root.findtext("Model_Zone_ID_System/TAZ_Model_Start_ID"))
        self.taz_model_end_id = int(root.findtext("Model_Zone_ID_System/TAZ_Model_End_ID"))
        self.taz_end_id = int(root.findtext("Model_Zone_ID_System/TAZ_End_ID"))
        self.taz_log_id = int(root.findtext("Model_Zone_ID_System/TAZ_ID_Log"))

        # Independet variables
        # The below two variables are needed to create additional variables for
        # DC models
        self.density_variables = root.findtext("Create_Density_Quartile_Variable").strip().split(",")
        self.area_variable = root.findtext("Area_Variable_Name").strip()
        # The below two variables are needed to create accessibility variables
        # for DC models
        self.skim_data = root.findtext("Skim_Data_Names").strip().split(",")
        self.employment_variable = root.findtext("Employment_Variable_Name").strip()

        # Variable Specific for either destinacion choice or mode choice
        # model id is 1,2 model is Destinacion choice
        # model id is 3,4 model is unm sub Destinacion choice
        # model id > 4 are mode choice models.
        model = root.find(".//Model[@Model_Id='{}']".format(model_id))
        self.attributes = model.attrib
        # For destination choice models
        # Function University Zones not assigend in original code.
        # Look to see if is needed it the file
        self.model_specs = self.attributes.get("Model_Specifications", "")
        # List of models' id to run for each porpuse
        self.models_to_run = map(int, self.attributes.get("Models_Id_To_Run", "").split(","))
        self.output_path = self.attributes.get("Output_Directory", "")
        if int(model_id) in [3,4] :
            self.enrollment = {}
            # UNM & CNM Zone IDs tag variables
            self.univ_cubeid = map(int, root.findtext("UNM_CNM_Zone_IDs/UNM_CNM_CUBEID").split(","))
            self.univ_super = int(root.findtext("UNM_CNM_Zone_IDs/UNM_CNM_Super_CUBEID"))
            #UNM_CNM_Enrollment
            self.enrollment["graduate"] = int(root.findtext("UNM_CNM_Enrollment/Graduate"))
            self.enrollment["undergrad_off_campus"] = int(root.findtext("UNM_CNM_Enrollment/Undergrad_Off_campus"))
            self.enrollment["undergrad_on_campus"] = int(root.findtext("UNM_CNM_Enrollment/Undergrad_On_campus"))
            self.enrollment["faculty"] = int(root.findtext("UNM_CNM_Enrollment/Faculty"))
            self.enrollment["staff"] = int(root.findtext("UNM_CNM_Enrollment/Staff"))        

