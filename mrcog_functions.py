import pysal as ps
import pandas as pd
import numpy as np
import os
import csv

#function that averages all the values inside the uni id zones
#it gets the sum of rows, columns and zones that both rows and columns are in uni id list
#set all the values in targeted ids to 0
#set super zone rows, columns and intrazone to correspodning values
#get average value of rows, columns and superzone. 
def avg_uni(matrix, uni_ids, univ_super):
    row_value = matrix.loc[uni_ids].sum() 
    col_value = matrix[uni_ids].sum(axis = 1) 
    in_zones =  matrix.ix[uni_ids, uni_ids].values.sum()

    matrix.loc[uni_ids] = 0
    matrix[uni_ids] = 0
    matrix.ix[uni_ids, uni_ids] = 0

    matrix.loc[univ_super] = row_value
    matrix[univ_super] = col_value
    matrix.ix[uni_ids, univ_super] = 0
    matrix.ix[univ_super, uni_ids] = 0
    
    matrix.set_value(univ_super, univ_super, in_zones)

    matrix.loc[univ_super] = matrix.loc[univ_super] / len(uni_ids)
    matrix[univ_super] = matrix[univ_super] / len(uni_ids)
    return matrix

#boolean to indentify if the model run is for the submodel unm dc_mc_property
#If true return True and ends function scope
#else retrun False
def is_uni(id):
    if id in [3,4]:
        return True
    return False
    
# Creates a df from a dbf
def dbf2df(dbfile, lower=True):  # Reads in DBF files and returns Pandas DF
    db = ps.open(dbfile)  # Pysal to open DBF
    d = {col: db.by_col(col) for col in db.header}  # Convert dbf to dictionary
    pandasDF = pd.DataFrame(d)  # Convert to Pandas DF
    if lower: #Make columns uppercase if wanted 
        pandasDF.columns = pandasDF.columns.str.lower()    
    db.close()
    return pandasDF


# functions that reads a txt file and return a dataframe matrix
# it creates a 919x919 dataframe
# reads the input file
# updates the 919 df with file values
def load_skim(skim, frame):
    with open(skim) as f:
        all_zones = pd.DataFrame(0.0, index=frame, columns=frame)
        df = pd.read_table(f, delim_whitespace=True,
                           dtype={'A': np.int64,
                                  'B': np.int64, 'C': np.float64},
                           names=('A', 'B', 'C'))
        df = df.pivot(index="A", columns="B", values="C")
        df = df.rename_axis(None)
        df.columns.name = None
        all_zones.update(df)
    return all_zones

# Retruns the name of the file, no extensions and path
def get_file_name(path):
    return os.path.basename(path).split(".")[0].strip().lower()

    
# Reads input files and returns the proper dataframe
# after reding the file it lower all column names
# set index to passed field
# updates to a dataframe with the  919 zones from 14 to 907
def read_file(file_input, frame, index_field=None):
    filename, file_extension = os.path.splitext(file_input)
    if file_extension == ".dbf":
        df = dbf2df(file_input)

    elif file_extension == ".csv":
        df = pd.read_csv(file_input)

    try:
        df.columns = map(str.lower, df.columns.values)
        df.index = df[index_field].astype(int)
        df.sort_index()
        all_zones = pd.DataFrame(0.0, index=frame, columns=df.columns.values)
        all_zones.update(df)
        return all_zones
    except ValueError:
        df = df[df[index_field] != 0]
        df.index = df[index_field].astype(int)
        df = df.rename_axis(None)
        return df


# creates a zeries of 1 and 0 depending if the zone is a model zone or not
# currenly zone models are 14 to 907
def get_model_zones(start=1, end=917, model_start=14, model_end=919):
    model_zones_list = []
    for i, x in enumerate(range(start, end + 1), 1):
        if model_start <= i <= model_end:
            z = 1
        else:
            z = 0
        model_zones_list.append(z)
    return pd.Series(data=model_zones_list, index=[i for i in range(start, end + 1)])


# set density variable
def set_denisty_variables(df, variable, area, numbin=4):
    # 1- it creates a new density column by dividing the vari_name by area.
    # 1.a vari_name comes from the dc_mc_property.xml Create_Density_Quartile_Variable tag.
    # 1.b area comes from the dc_mc_property.xml Area_Variable_Name tag.
    df.density = df['{}'.format(variable)].div(df['{}'.format(area)]).fillna(0)

    # 2 creates an ascending sorted list of the density field
    dsort = df.density.copy()
    dsort.sort_values(inplace=True)
    dsort = dsort.tolist()

    # Step3: Find density values at the location of 25%, 50%, and 75% in dsort
    # for bins it uses the number of rows of the socio table / num of bins
    bins = len(df.index) / numbin
    # treshold is  a list of 4 ranges value, each value is depending on evry
    # bins value.
    threshold = dsort[::bins]
    # by default is uses the last value of dsort +1 to ensure that we have a
    # max number for comparison
    threshold[-1] = dsort[-1] + 1
    return df.density, threshold


def emp_within(min, source, emp_vari, frame):
    empwithin = pd.Series(data=0.0, index=frame)
    for index, row in source.iterrows():
        temp = ((source.loc[index] > 0) & (source.loc[index] < min)) * 1
        indices = [key for key, value in temp.iteritems() if value == 1]
        try:
            numemp = emp_vari[indices].sum()
            empwithin[index] = np.float(numemp)
        except IndexError:
            empwithin[index] = np.float(0.0)        
    return empwithin.divide(emp_vari.sum()).fillna(0)       
    
# set density variable
# uses a threshold time such as 30 or 50 min
# It adds different skims to get total time stored in timedata
# temp is a pd series of 1 or 0 depending if the timedata.row[i] is less than the min threshold
# indices is a list that holds all the zones that are whitin the time treshold
# empvari is a series of the tot_emp field in the socio table. it sums all the emp inside indices
# for example if zone 17 and 18 are accesible within 30 min, it get totemp
# for zone 17 and 18 as empwithin
def set_accessibility_variables(min, matrices, skims_vari, emp_vari, frame):
    timedata = pd.DataFrame(0.0, index=frame, columns=frame)
    for i in skims_vari:
        timedata += matrices[i]
    empwithin = emp_within(min, timedata, emp_vari, frame)   
    return empwithin


# return the model attributes from the xml file
#is uni and enrollment attributes needed for uni submodel 
# enrollmnet values come from the dc_property xml via model enrollment value
def get_model_attributes(model, doubly=None, is_uni = False, enr_val = None):
    name = model.get('Name')
    model_id = model.get('Id')
    model_desc = model.get('Description')
    if is_uni:
        enroll_type =  model.get("Enrollment").lower()
        enrollment = enr_val[enroll_type]
        trip_rate = float(model.get("TripRate"))
        trip_count = trip_rate * enrollment
        if model.attrib.get("PandA") == 'Attraction':
            isPro = False
        else:
            isPro = True
        
        return {"name": model.get('Name'), "model_id": model.get('Id'), "model_desc": model_desc,
                "enrollment": enrollment, "isProduct": isPro, "trip_rate": trip_rate, "trip_count": trip_count}
    else:
        if model.get("Productions"):
            product = model.get("Productions").split(",")
            isPro = True
            if model.get("Attractions"):
                doubly = model.get("Attractions").split(",")
        else:
            product = model.get("Attractions").split(",")
            isPro = False

        return {"name": model.get('Name'), "model_id": model.get('Id'), "model_desc": model_desc,
                "product_columns": product, "isProduct": isPro, "doubly_columns": doubly}


            
# function that aggregates either productions or attracations based of product or doubly columns
# the columns come from the xml file through the get model attribute function
def get_panda(columns, panda_table, taz_start_id, taz_end_id):
    serie = pd.Series(
        data=0.0, index=[i for i in range(taz_start_id, taz_end_id + 1)])
    for col in columns:
        serie += panda_table[col.lower()]
    return serie


# Function to balance a matrix by doing an IPF
# it will balance rows for productions
# it will balance cols for attractions
def balancing_matrix(matrix, product, attract, log):
    tol = 0.005
    maxiter = 20
    relative = 1.0
    numzones = len(matrix.index)
    numiter = 0
    result = matrix

    while numiter < maxiter and relative > tol:

        normal_row = nomral_factor(result, attract)
        result = result.mul(normal_row, axis=1)

        log.msg("Iteration {}".format(numiter))
        normal_col = nomral_factor(result, product, index=1)
        result = result.mul(normal_col, axis=0)

        relative = computeErrors(result, attract,log)

        numiter += 1

    return result.fillna(0)


# Function used in the balancing matrix functions
# it gets the row or columns total depending on the sum index.
# index=0 means sumrows and index=1 means colsums
# it divides prod or attractions by sumtotal depending.
def nomral_factor(matrix, target, index=0):
    np.seterr(invalid='ignore')
    targetsum = matrix.sum(axis=index)
    return target.divide(targetsum).fillna(0)

# get the absolute and relative error for the ipf process
def computeErrors(matrix, attract,log):
    rowsum = matrix.sum(axis=0)
    adifference = pd.Series.abs(rowsum - attract)
    lowvalue = np.minimum(rowsum, attract)
    rdifference = adifference.div(lowvalue).fillna(0).max()
    log.msg("Relative error: {}".format(rdifference))
    log.msg("Absolute error: {}".format(adifference.max()))
    return rdifference

# function that aggregates any dataframe by area types.
# it groups by row then it groups by column
# manipulates the dataframe to exclude the 0 group which is usally non existent
def aggregated_result(matrix, group):
    max_group = int(group.max())
    if int(group.min()) <= 0:
        min_group = 1
    else:
        min_group = int(group.min())
    
    matrix = matrix.groupby(group).sum().groupby(group, axis=1).sum()
    matrix = matrix.rename_axis(None)
    matrix.columns = matrix.columns.astype(int)
    matrix.index = matrix.index.astype(int)
    return matrix.ix[:, min_group:max_group].loc[min_group:max_group]


def aggregated_result_validation(result, dis_mtx, socio, output_name, is_uni = False, superzone = None):
    #get index of the / to add aggregate to the name
    sindex = output_name.rfind("/", 1)
    output_file = output_name[:sindex + 1] + \
        '_aggregated_' + output_name[sindex + 1:]

    bins = {1: [0.0, 1.0], 2: [1.0, 2.5], 3: [2.5, 5.0], 4: [5.0, 7.5], 5: [7.5, 10.0], 6: [10.0, 15.0], 7: [15.0, 20.0],
            8: [20.0, 25.0], 9: [25.0, 30.0], 10: [30.0, 35.0], 11: [35.0, 40.0], 12: [40.0, 45.0], 13: [45.0, 30000.0]}
    
    labels = {1: '<=1.0', 2: '1.0>,<=2.5', 3: '2.5>,<=5.0', 4: '5.0>,<=7.5', 5: '7.5>,<=10', 6: '10>,<=15',
              7: '15>,<=20', 8: '20>,<=25', 9: '25>,<=30', 10: '30>,<=35', 11: '35>,<=40', 12: '40>,<=45', 13: '>45'}

    if is_uni:
        aggregated_result_dc_uni(result,output_file,dis_mtx,socio,bins,labels,superzone)
    else :
        aggregated_result_dc(result,output_file,dis_mtx,socio,bins,labels)          
    

#Writes summary report for the aggregated pk,op files
def  aggregated_result_dc_uni(result, output_file, dis_mtx, socio, bins, labels, superzone):   
    with open(output_file, "wb") as f:
        writer = csv.writer(f)
        ### finish this later. i dont think result series need to be transposed
        if result[superzone].sum() < result.loc[superzone].sum():
            result_series = result.loc[superzone]
            dis_mtx = dis_mtx.loc[superzone]
        else:
            result_series = result[superzone]
            dis_mtx = dis_mtx[superzone]           

            
        # Writes distance summary        
        for key in bins.keys():
            bin_ = bins[key]
            label = labels[key]
            temp = result_series.mul(((dis_mtx <= bin_[1]) & (dis_mtx > bin_[0])) * 1)
            trips = temp.values.sum()
            if key == 1:
                trips = result_series[superzone]
            if key == 2:
                trips = trips - result_series[superzone]
            writer.writerow([label,trips])
        intra_camp_trips = result_series.ix[superzone,superzone]  
        writer.writerow(["Intra_Campus",intra_camp_trips])
            


        writer.writerow([])
        writer.writerow([])

        # Wrties aggregation by district summary
        agg_district = aggregated_result(result, socio.district)
        writer.writerow(["district"] + agg_district.columns.tolist())
        for row in agg_district.iterrows():
            index, data = row
            writer.writerow([index] + data.tolist())

        writer.writerow([])
        writer.writerow([])

        # Wrties aggregation by area type
        #since there a two county fields in the socio df, the country filed with int
        #is county_y. since it was read second. in order to change this, county from the socio dbf 
        #needs have a different name
        agg_areatypes = aggregated_result(result, socio.county_y)
        writer.writerow(["county"] + agg_areatypes.columns.tolist())
        for row in agg_areatypes.iterrows():
            index, data = row
            writer.writerow([index] + data.tolist())


    
#Writes summary report for the aggregated pk,op files
def  aggregated_result_dc(result,output_file,dis_mtx,socio,bins,labels):   
    with open(output_file, "wb") as f:
        writer = csv.writer(f)
        # Writes distance summary
        for key in bins.keys():
            bin_ = bins[key]
            label = labels[key]
            temp = result.mul(((dis_mtx <= bin_[1]) & (dis_mtx > bin_[0])) * 1)
            trips = temp.values.sum()
            writer.writerow([label, trips])
        total_miles = result * dis_mtx
        avg_miles = total_miles.values.sum() / result.values.sum()
        writer.writerow(['average distance', avg_miles])

        writer.writerow([])
        writer.writerow([])

        # Wrties aggregation by district summary
        agg_district = aggregated_result(result, socio.district)
        writer.writerow(["district"] + agg_district.columns.tolist())
        for row in agg_district.iterrows():
            index, data = row
            writer.writerow([index] + data.tolist())

        writer.writerow([])
        writer.writerow([])

        # Wrties aggregation by area type
        agg_areatypes = aggregated_result(result, socio["at"])
        writer.writerow(["areatypes"] + agg_areatypes.columns.tolist())
        for row in agg_areatypes.iterrows():
            index, data = row
            writer.writerow([index] + data.tolist())

#mode choice functions to determine walk times and shares from zone to zone            
def intra_walk_share(zone, df, field):
    val = df[field].loc[df.index == zone].values[0]
    temp = df[field] * val
    return temp.values.tolist()

def external_walk_share(zone, df, field1, field2):
    val1 = df[field1].loc[df.index == zone].values[0]
    val2 = df[field2].loc[df.index == zone].values[0]
    temp = df[field2] * val1 +  df[field1] * val2
    return temp.values.tolist()

def intra_walk_time(zone, df, field):
    val = df[field].loc[df.index == zone].values[0]
    temp = df[field] + val
    return temp.values.tolist()

def external_walk_time(zone, df, field1, field2, field3, field4):
    val1 = df[field1].loc[df.index == zone].values[0]
    val2 = df[field2].loc[df.index == zone].values[0]
    val3 = df[field3].loc[df.index == zone].values[0]
    val4 = df[field4].loc[df.index == zone].values[0]
    temp = ((df[field3] + val1) * (df[field4] * val2) + (df[field1] + val3)  * (df[field2] * val4))
    return temp.values.tolist()

def drive_access_transit_shares(zone, df, field):
    val = 1 - df.sh_share.loc[df.index == zone].values[0] - df.md_share.loc[df.index == zone].values[0] - df.lg_share.loc[df.index == zone].values[0]
    temp = val * df[field]
    return temp.values.tolist()
    
#create walking time,share base dataframe
def create_walking_share_time_df(d):
    df = pd.DataFrame(index=pd.MultiIndex.from_product([d.index, d.index])).reset_index()
    df.columns = ['i', 'j']

    col = ["s_s_walk_share" ,"s_s_walk_time","s_m_walk_share","s_m_walk_time",    
           "s_l_walk_share","s_l_walk_time","m_m_walk_share","m_m_walk_time",
           "m_l_walk_share","m_l_walk_time","l_l_walk_share","l_l_walk_time",
           "d_access_t_short_walk_share","d_access_t_short_walk_time",
           "d_access_t_med_walk_share","d_access_t_med_walk_time",
           "d_access_t_long_walk_share","d_access_t_long_walk_time","drive_only"]

    for c in col:  
        df[c] = -99 
    
    return df

    
#Function that deletes success file to run python script
def del_checker(file):
    filename = os.path.join(file, "01_Inputs/common/success.txt")
    if os.path.exists(filename):
        os.remove(filename) 

def create_checker(file):
    filename = os.path.join(file, "01_Inputs/common/success.txt")
    with open(filename,"w") as f:
        f.write("1")    
