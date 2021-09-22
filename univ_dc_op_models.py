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
    socio["pop_dev"] = socio['pop'] * socio.p_dev   
    return matrix,socio

def Grad_HB_OP(matrix, socio, result, superzone): 
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
    
def Grad_NHB_OP(matrix, socio, result, superzone): 
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))
    result += matrix['logsum_grad_op']* 3.55
    result = result.add(socio.ser_emp.div(socio.total_emp).mul(2.803).fillna(0), axis = 0)
    result = result.add(socio.ret_emp.div(socio.total_emp).mul(1.511).fillna(0), axis = 0)
    result = result.add((socio["pop"]).mul(0.000276), axis = 0)    
    result = result.add(socio.hhpop.div(socio["pop"]).mul(-1.201).fillna(0), axis = 0)
    result +=((matrix["distance"] > 2.5) & (matrix["distance"] <= 5))  * -0.804
    result = result.add((socio.inc_3).mul(0.000945), axis = 0)
    result = result.add((socio.total_empden1).mul(0.568), axis=0)
    result = result.add((socio.p_dev).mul(0.02222), axis=0)
    result +=((matrix["distance"] > 1) & (matrix["distance"] <= 2.5))  * -0.2    
    intravalue = result.get_value(superzone,superzone) + 1.75
    result.set_value(superzone,superzone,intravalue)
    return result,mfilter
    
def Offcam_UG_HB_OP(matrix, socio, result, superzone): 
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

def Offcam_UG_NHB_OP(matrix, socio, result, superzone): 
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))
    result += matrix['logsum_offcam_op']* 4.15
    result = result.add((socio.ret_emp).mul(0.001006), axis=0)
    result = result.add((socio.ser_emp).mul(-0.000099), axis=0)
    result = result.add(socio.mfdu.div(socio.du).mul(-0.556).fillna(0), axis = 0)
    result +=((matrix["distance"] > 1) & (matrix["distance"] <= 2.5))  * -3.01
    result +=((matrix["distance"] > 2.5) & (matrix["distance"] <= 20))  * -3.352
    #variable that is actually in the code
    result = result.add(socio.tothh.mask(socio.tothh != 0).fillna(socio.gqpop.div(socio["pop"]).fillna(0)).mul(0.14), axis = 0)
    #the current model code does not multiply dist matrix * gqpop / ["pop"]
    #it only uses the division result constant *.14 plue result#
    #might have to be revides
    #result += matrix['dist'].mul(socio.gqpop.div(socio["pop"]).mul(0.14).fillna(0), axis = 0) 
    result = result.add(socio.inc_3.div(socio.tot_inc).mul(0.00053).fillna(0), axis = 0)
    result = result.add((socio.popden1).mul(0.511), axis=0)
    result = result.add((socio.total_empden1).mul(0.183), axis=0)
    result = result.add((socio.p_dev).mul(0.01733), axis=0)
    intravalue = result.get_value(superzone,superzone) + 6.7
    result.set_value(superzone,superzone,intravalue)
    return result,mfilter    
    
def Oncam_UG_DB_OP(matrix, socio, result, superzone): 
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))
    result += matrix['logsum_dbu_op'].T * 1.25
    result = result.add(socio.pop_dev.div(socio.acres).mul(0.000041).fillna(0), axis = 0)
    result = result.add((socio.ret_emp).mul(0.000654), axis=0)
    result = result.add(socio.mfdu.div(socio.du).mul(0.884).fillna(0), axis = 0)
    result = result.add(socio.basic_emp.div(socio.total_emp).mul(-1.091).fillna(0), axis = 0)
    result = result.add((socio.total_emp).mul(0.000225), axis=0)
    result +=((matrix["distance"].T > 2.5) & (matrix["distance"].T <= 5))  * -0.074
    result += matrix["dist"].T.mul(socio.propp2, axis=0) * 0.135 
    result = result.add(socio.inc_3.div(socio.tot_inc).mul(1.214).fillna(0), axis = 0)
    result = result.add((socio.popden4).mul(-1.214), axis=0)
    result = result.add((socio.total_empden4).mul(-2.256), axis=0)
    result +=((matrix["distance"].T > 1) & (matrix["distance"].T <= 2.5))  * 1
    intravalue = result.get_value(superzone,superzone)  -1.6
    result.set_value(superzone,superzone,intravalue)    
    return result,mfilter

def Oncam_UG_NDB_OP(matrix, socio, result, superzone): 
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))
    result += matrix['logsum_ndbu_op']* 2.8   
    result = result.add(socio.ser_emp.div(socio.total_emp).mul(2.478).fillna(0), axis = 0)
    result = result.add(socio.hhpop.div(socio["pop"]).mul(-1.492).fillna(0), axis = 0)
    result = result.add((socio["pop"]).mul(0.000367), axis=0)  
    result = result.add(socio.ret_emp.div(socio.total_emp).mul(1.411).fillna(0), axis = 0)    
    result += matrix["dist"].mul(socio.propp2, axis=0) * 0.144
    result = result.add((socio.total_empden4).mul(-3.443), axis=0) 
    result = result.add((socio.transit30).mul(26.883), axis=0)
    result = result.add((socio.p_dev).mul(0.01952), axis=0)    
    result +=((matrix["distance"] > 2.5) & (matrix["distance"] <= 5))  * -2.25
    result +=((matrix["distance"] > 1) & (matrix["distance"] <= 2.5))  * -0.5
    intravalue = result.get_value(superzone,superzone) + 2.2
    result.set_value(superzone,superzone,intravalue)
    return result,mfilter
    
def Faculty_HBW_OP(matrix, socio, result, superzone): 
    mfilter = ((socio.housezero < 1) & (socio.hhpop > 0))
    result = result.add((socio.hhpop).mul(0.00050504796), axis=0)
    result = result.add((socio.sfdu).mul(0.00056117793), axis=0)
    result = result.add(socio.hhpop.div(socio.acres).mul(-0.01674349).fillna(0), axis = 0)
    result = result.add(socio.inc_2.div(socio.tot_inc).mul(1.09690484).fillna(0), axis = 0)
    result = result.add((socio["at"] == 4).mul(0.75498181), axis = 0)
    result += matrix["avglogsum"].mul(0.1502715)
    result += matrix['avgtt'] * -0.0507327
    result += np.power(matrix['distance'], 2) * 0.00066708
    result += (matrix["distance"] <= 5) * 1.4
    result +=((matrix["distance"] > 5) & (matrix["distance"] <= 7.5))  * 0.5
    result +=((matrix["distance"] > 10) & (matrix["distance"] <= 15))  * 1
    return result,mfilter 
    
def NHBW_Faculty_OP(matrix, socio, result, superzone): 
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))
    result = result.add(np.log(socio.ret_emp + 1).mul(0.16747638), axis=0)
    result = result.add(np.log(socio.ser_emp + 1).mul(0.24211584), axis=0)
    result = result.add((socio["at"] == 1).mul(0.3575172), axis = 0)
    result = result.add(socio.hhpop.div(socio.acres).mul(-0.01838079).fillna(0), axis = 0)    
    result = result.add(socio.ret_emp.div(socio.acres).mul(0.08341678).fillna(0), axis = 0)  
    result += matrix['mc_nhbw_all_logsum_op'] * 0.90072732
    result += matrix['optime'] * -0.23786923
    result += np.power(matrix['distance'], 2) * 0.01487863
    result += np.power(matrix['distance'], 3) * -0.00023106
    result +=((matrix["distance"] > 7.5) & (matrix["distance"] <= 15))  * -0.1
    result +=((matrix["distance2"] > 2.5) & (matrix["distance2"] <= 7.5))  * -0.6    
    result +=((matrix["distance"] > 1) & (matrix["distance"] <= 2.5))  * -1.2
    intravalue = result.get_value(superzone,superzone) + 5.25
    result.set_value(superzone,superzone,intravalue)  
    return result,mfilter
    
def Staff_HBW_OP(matrix, socio, result, superzone): 
    mfilter = ((socio.housezero < 1) & (socio.hhpop > 0))
    result = result.add((socio.hhpop).mul(0.00050504796), axis=0)
    result = result.add((socio.sfdu).mul(0.00056117793), axis=0)
    result = result.add(socio.hhpop.div(socio.acres).mul(-0.01674349).fillna(0), axis = 0)
    result = result.add(socio.inc_2.div(socio.tot_inc).mul(1.09690484).fillna(0), axis=0)
    result = result.add((socio["at"] == 4).mul(0.75498181), axis = 0)
    result += matrix["avglogsum"]* 0.1502715
    result += matrix['avgtt'] * -0.0507327
    result += np.power(matrix['distance'], 2) * 0.00066708
    result += (matrix["distance"] <= 5) * 1.2
    result +=((matrix["distance"] > 5) & (matrix["distance"] <= 7.5))  * 0.2
    result +=((matrix["distance"] > 10) & (matrix["distance"] <= 15))  * 0.5 
    return result,mfilter
    
def NHBW_Staff_OP(matrix, socio, result, superzone): 
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))    
    result = result.add(np.log(socio.ret_emp + 1).mul(0.16747638), axis=0)
    result = result.add(np.log(socio.ser_emp + 1).mul(0.24211584), axis=0)
    result = result.add((socio["at"] == 1).mul(0.3575172), axis = 0)
    result = result.add(socio.hhpop.div(socio.acres).mul(-0.01838079).fillna(0), axis = 0) 
    result = result.add(socio.ret_emp.div(socio.acres).mul(0.08341678).fillna(0), axis = 0) 
    result += matrix["mc_nhbw_all_logsum_op"]* 0.90072732
    result += matrix['optime'] * -0.23786923
    result += np.power(matrix['distance'], 2) * 0.01487863
    result += np.power(matrix['distance'], 3) * -0.00023106
    result +=((matrix["dist"] > 7.5) & (matrix["dist"] <= 15))  * -0.25
    result +=((matrix["dist"] > 2.5) & (matrix["dist"] <= 7.5))  * -0.6    
    result +=((matrix["distance"] > 1) & (matrix["distance"] <= 2.5))  * -1
    intravalue = result.get_value(superzone,superzone) + 4.8
    result.set_value(superzone,superzone,intravalue)  
    return result,mfilter
    
