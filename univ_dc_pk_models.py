# Equation specifications for each op model
#if the model has productions, the matrices are transposed
#if not the matrices do not need to be transposed 

import numpy as np

def set_model_variables(matrix,socio):
    socio['tothh'] = socio.sfdu + socio.mfdu
    matrix["avgtt"] = 0.5 * matrix['amtime'] + 0.5 * matrix['optime']
    matrix["distance2"] = matrix['dist'].T
    matrix["distance"] =  0.5 * matrix['dist'] + 0.5 * matrix['distance2']    
    socio['gqpop'] = socio['pop'] - socio.hhpop + socio.dormpop
    matrix["avglog1"] =  0.5 * matrix['logsum_grad_pk'] + 0.5 * matrix['logsum_grad_op'] 
    matrix["avglog2"] =  0.5 * matrix['logsum_offcam_pk'] + 0.5 * matrix['logsum_offcam_op'] 
    matrix["avglogsum"] =  0.5 * matrix['mc_hbw_auto_sufficient_logsum_op'] + 0.5 * matrix['mc_hbw_auto_sufficient_logsum_pk'] 
    socio['tot_inc'] = socio.inc_1 + socio.inc_2 + socio.inc_3    
    socio['propp2'] = socio.gqpop.div(socio['pop']).fillna(0)    
    return matrix,socio

def Grad_HBP(matrix, socio, result, superzone): 
    mfilter = socio.hhpop > 0
    result += matrix['avglog1']* 2.3    
    result = result.add((socio.hh).mul(0.00076165377), axis=0)
    result = result.add((socio.ret_emp).mul(0.00024910819), axis=0)
    result = result.add(socio.hhpop.div(socio["pop"]).mul(0.98689046).fillna(0), axis = 0)
    result = result.add(socio.inc_1.div(socio.hh).mul(-1.35303573).fillna(0), axis = 0)
    result +=((matrix["distance"] > 1) & (matrix["distance"] <= 2.5))  * 1.3
    result +=((matrix["distance"] > 2.5) & (matrix["distance"] <= 5))  * 0.258
    result +=((matrix["distance"] > 5) & (matrix["distance"] <= 10))  * -0.311
    intravalue = result.get_value(superzone,superzone) + 0.75
    result.set_value(superzone,superzone,intravalue)
    return result,mfilter    
    
def Grad_NHBP(matrix, socio, result, superzone): 
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))
    result += matrix['logsum_grad_pk']* 3.064
    result = result.add(socio.hhpop.div(socio["pop"]).mul(-0.66825584).fillna(0), axis = 0)
    result = result.add(socio.ser_emp.div(socio.total_emp).mul(2.24881973).fillna(0), axis = 0)
    result = result.add(socio.ret_emp.div(socio.total_emp).mul(1.06804248).fillna(0), axis = 0)
    result = result.add((socio.total_empden1).mul(0.59779986), axis=0)
    result +=((matrix["distance"] > 1) & (matrix["distance"] <= 10))  * -0.917
    result +=((matrix["distance"] > 1) & (matrix["distance"] <= 2.5))  * 0.15
    intravalue = result.get_value(superzone,superzone) + 4.5
    result.set_value(superzone,superzone,intravalue)
    return result,mfilter
    
def Offcam_UG_HBP(matrix, socio, result, superzone): 
    mfilter = socio.hhpop > 0
    result += matrix['avglog2']* 3.6
    result = result.add((socio.hhpop).mul(0.000272), axis=0)
    result = result.add((socio.gqpop).mul(-0.000244), axis=0)
    result = result.add((socio.ret_emp).mul(0.00015), axis=0)
    result = result.add((socio.ser_emp).mul(-0.000221), axis=0)
    result = result.add(socio.mfdu.div(socio.du).mul(0.52).fillna(0), axis = 0)
    result = result.add(socio.inc_3.div(socio.tot_inc).mul(1.715).fillna(0), axis = 0)
    result = result.add((socio.popden1).mul(0.106), axis=0)
    result = result.add((socio.total_empden4).mul(-0.756), axis=0)
    result +=((matrix["distance"] > 5) & (matrix["distance"] <= 10))  * -0.655    
    result +=((matrix["distance"] > 15) & (matrix["distance"] <= 25))  * 0.575    
    result +=((matrix["distance"] > 1) & (matrix["distance"] <= 2.5))  * 0.5
    result = result.add((socio.p_dev).mul(0.00614), axis=0)
    intravalue = result.get_value(superzone,superzone) + 7.6
    result.set_value(superzone,superzone,intravalue)
    return result,mfilter

def Offcam_UG_NHBP(matrix, socio, result, superzone): 
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))
    result += matrix['logsum_offcam_pk']* 5.383
    result = result.add((socio.hhpop).mul(0.00012610634), axis=0)
    result = result.add((socio.ret_emp).mul(0.0009855646), axis=0)
    result = result.add((socio.inc_1).mul(-0.00122747077), axis=0)
    result = result.add(socio.sfdu.div(socio.tothh).mul(-0.52263259).fillna(0), axis = 0)
    result +=((matrix["distance"] > 1) & (matrix["distance"] <= 2.5))  * -4.005
    result +=((matrix["distance"] > 2.5) & (matrix["distance"] <= 25))  * -3.1873426
    result = result.add((socio.ser_emp).mul(-0.00008365862), axis=0)
    result += matrix["distance"].mul(socio.propp2, axis=0).mul(0.1300047)
    result += matrix["distance"].mul(socio.popden1, axis=0).mul(0.01541049)
    result = result.add((socio.popden4).mul(-0.560306), axis=0)
    result = result.add((socio.total_empden3).mul(0.17449616), axis=0)
    intravalue = result.get_value(superzone,superzone) + 8.1
    result.set_value(superzone,superzone,intravalue)
    return result,mfilter    
    
def On_DBP(matrix, socio, result, superzone): 
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))
    result += matrix['logsum_dbu_pk'].T * 4.083
    result = result.add(socio.inc_3.div(socio.tot_inc).mul(1.63904576).fillna(0), axis = 0)  
    result += matrix["distance"].T.mul(socio.propp2, axis=0).mul(0.11172023)    
    result = result.add((socio.ret_emp).mul(0.00082747363), axis=0)
    result = result.add((socio.popden4).mul(-1.39510863), axis=0)
    result = result.add((socio.total_empden3).mul(0.71397406), axis=0)
    result +=((matrix["distance"].T > 2.5) & (matrix["distance"].T <= 15))  * -1.3
    intravalue = result.get_value(superzone,superzone) + 3.9
    result.set_value(superzone,superzone,intravalue)    
    return result,mfilter

def On_NDBP(matrix, socio, result, superzone): 
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))
    result += matrix['logsum_ndbu_pk']* 3.66061   
    result = result.add(socio.hhpop.div(socio["pop"]).mul(-1.68225797).fillna(0), axis = 0)    
    result = result.add(socio.ser_emp.div(socio.total_emp).mul(2.17464883).fillna(0), axis = 0)  
    result += matrix["distance"].mul(socio.propp2, axis=0).mul(0.11339093)  
    result = result.add((socio.transit50).mul(3.36802706), axis=0) 
    result = result.add((socio.popden4).mul(-0.7211346), axis=0)  
    result +=((matrix["distance"] > 1) & (matrix["distance"] <= 2.5))  * -0.15
    result +=((matrix["distance"] > 2.5) & (matrix["distance"] <= 5))  * -0.6
    intravalue = result.get_value(superzone,superzone) + 3
    result.set_value(superzone,superzone,intravalue)
    return result,mfilter
    
def Faculty_HBW_Peak(matrix, socio, result, superzone): 
    mfilter = ((socio.housezero < 1) & (socio.hhpop > 0))
    result = result.add((socio.hhpop).mul(0.00050504796), axis=0)
    result = result.add((socio.sfdu).mul(0.00056117793), axis=0)
    result = result.add(socio.hhpop.div(socio.acres).mul(-0.01674349).fillna(0), axis = 0)
    result = result.add(socio.inc_2.div(socio.tot_inc).mul(1.09690484).fillna(0), axis = 0)
    result = result.add((socio["at"] == 4).mul(0.75498181), axis = 0)
    result += matrix["avglogsum"].mul(0.1502715)
    result += matrix['avgtt'] * -0.0507327
    result += np.power(matrix['distance'], 2) * 0.00066708
    result += (matrix["distance"] <= 5) * 0.75
    result +=((matrix["distance"] > 7.5) & (matrix["distance"] <= 10))  * -0.5
    result +=((matrix["distance"] > 10) & (matrix["distance"] <= 15))  * 0.5
    return result,mfilter 
    
def NHBW_Faculty_Peak(matrix, socio, result, superzone): 
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))
    result = result.add(np.log(socio.ret_emp + 1).mul(0.16747638), axis=0)
    result = result.add(np.log(socio.ser_emp + 1).mul(0.24211584), axis=0)
    result = result.add((socio["at"] == 1).mul(0.3575172), axis = 0)
    result = result.add(socio.hhpop.div(socio.acres).mul(-0.01838079).fillna(0), axis = 0)    
    result = result.add(socio.ret_emp.div(socio.acres).mul(0.08341678).fillna(0), axis = 0)  
    result += matrix['mc_nhbw_all_logsum_pk'] * 0.90072732 
    result += matrix['amtime'] * -0.23786923
    result += np.power(matrix['distance'], 2) * 0.01487863
    result += np.power(matrix['distance'], 3) * -0.00023106 
    result +=((matrix["distance"] > 7.5) & (matrix["distance"] <= 15))  * -0.5
    result +=((matrix["distance"] > 2.5) & (matrix["distance"] <= 7.5))  * -1.8    
    result +=((matrix["distance"] > 1) & (matrix["distance"] <= 2.5))  * -1.9
    intravalue = result.get_value(superzone,superzone) + 4.65
    result.set_value(superzone,superzone,intravalue)  
    return result,mfilter
    
def Staff_HBW_Peak(matrix, socio, result, superzone): 
    mfilter = ((socio.housezero < 1) & (socio.hhpop > 0))
    result = result.add((socio.hhpop).mul(0.00050504796), axis=0)
    result = result.add((socio.sfdu).mul(0.00056117793), axis=0)
    result = result.add(socio.hhpop.div(socio.acres).mul(-0.01674349).fillna(0), axis = 0)
    result = result.add(socio.inc_2.div(socio.tot_inc).mul(1.09690484).fillna(0), axis=0)
    result = result.add((socio["at"] == 4).mul(0.75498181), axis = 0)
    result += matrix["avglogsum"]* 0.1502715
    result += matrix['avgtt'] * -0.0507327
    result += np.power(matrix['distance'], 2) * 0.00066708
    result += (matrix["distance"] <= 5) * 0.75
    result +=((matrix["distance"] > 7.5) & (matrix["distance"] <= 10))  * -0.5
    result +=((matrix["distance"] > 10) & (matrix["distance"] <= 15))  * 0.5 
    return result,mfilter
    
def NHBW_Staff_Peak(matrix, socio, result, superzone): 
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))    
    result = result.add(np.log(socio.ret_emp + 1).mul(0.16747638), axis=0)
    result = result.add(np.log(socio.ser_emp + 1).mul(0.24211584), axis=0)
    result = result.add((socio["at"] == 1).mul(0.3575172), axis = 0)
    result = result.add(socio.hhpop.div(socio.acres).mul(-0.01838079).fillna(0), axis = 0) 
    result = result.add(socio.ret_emp.div(socio.acres).mul(0.08341678).fillna(0), axis = 0) 
    result += matrix["mc_nhbw_all_logsum_pk"]* 0.90072732
    result += matrix['amtime'] * -0.23786923 
    result += np.power(matrix['distance'], 2) * 0.01487863
    result += np.power(matrix['distance'], 3) * -0.00023106
    result +=((matrix["distance"] > 7.5) & (matrix["distance"] <= 15))  * -0.5
    result +=((matrix["distance"] > 2.5) & (matrix["distance"] <= 7.5))  * -1.8    
    result +=((matrix["distance"] > 1) & (matrix["distance"] <= 2.5))  * -1.8
    intravalue = result.get_value(superzone,superzone) + 4.3
    result.set_value(superzone,superzone,intravalue)  
    return result,mfilter
    
