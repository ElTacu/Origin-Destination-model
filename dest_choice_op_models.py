# Equation specifications for each op model
#if the model has productions, the matrices are transposed
#if not the matrices do not need to be transposed 

import numpy as np


def set_model_variables(matrix,socio):
    socio['tothh'] = socio.sfdu + socio.mfdu
    matrix["avgtt"] = 0.5 * matrix['amtime'] + 0.5 * matrix['optime']
    matrix["distance2"] = matrix['dist'].T
    matrix["distance"] =  0.5 * matrix['dist'] + 0.5 * matrix['distance2']    
    socio['enroll'] = socio.es_enr + socio.ms_enr + socio.enrl_priem + socio.enroll_cha    
    socio['gqpop'] = socio['pop'] - socio.hhpop + socio.dormpop
    socio['tot_inc'] = socio.inc_1 + socio.inc_2 + socio.inc_3    
    socio['propp2'] = socio.gqpop.div(socio['pop']).fillna(0)    
    return matrix,socio

def hbw_auto_0(matrix, socio, result): 
    mfilter = socio.total_emp > 0
    result = result.add(np.log(socio.basic_emp + 1).mul(0.24160834), axis=0)
    result = result.add(np.log(socio.ser_emp + 1).mul(0.36310718), axis = 0)
    result = result.add(np.log(socio.ret_emp + 1).mul(-0.09360441), axis = 0)
    result = result.add(socio.hhpop.div(socio.acres).mul(-0.07379568).fillna(0), axis = 0)
    result = result.add(socio.total_emp.div(socio.acres).mul(0.00410132).fillna(0), axis = 0)
    result += matrix['mc_hbw_auto_0_logsum_op'].T * 0.31493654
    result += matrix['avgtt'].T * -0.05689183
    result += (matrix["dist"].T <= 1) * 3
    result +=((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5))  * 1.2
    result += (matrix["dist"].T > 5) * -2
    return result,mfilter    
    
def hbw_auto_deficient_inc1(matrix, socio, result):
    mfilter = socio.total_emp > 0
    result = result.add(np.log(socio.basic_emp + 1).mul(0.24160834), axis=0)
    result = result.add(np.log(socio.ser_emp + 1).mul(0.36310718), axis = 0)
    result = result.add(np.log(socio.ret_emp + 1).mul(-0.09360441), axis = 0)
    result = result.add(socio.hhpop.div(socio.acres).mul(-0.07379568).fillna(0), axis = 0)
    result = result.add(socio.total_emp.div(socio.acres).mul(0.00410132).fillna(0), axis = 0)
    result += matrix['mc_hbw_auto_deficient_logsum_op'].T * 0.31493654
    result += matrix['avgtt'].T * -0.05689183
    result +=((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5))  * 0.8
    return result,mfilter
    
def hbw_auto_deficient_inc2(matrix, socio, result): 
    mfilter = socio.total_emp > 0
    result = result.add(np.log(socio.basic_emp + 1).mul(0.24160834), axis=0)
    result = result.add(np.log(socio.ser_emp + 1).mul(0.36310718), axis = 0)
    result = result.add(np.log(socio.ret_emp + 1).mul(-0.09360441), axis = 0)
    result = result.add(socio.hhpop.div(socio.acres).mul(-0.07379568).fillna(0), axis = 0)
    result = result.add(socio.total_emp.div(socio.acres).mul(0.00410132).fillna(0), axis = 0)
    result += matrix['mc_hbw_auto_deficient_logsum_op'].T * 0.31493654
    result += matrix['avgtt'].T * -0.05689183
    result += (matrix["dist"].T <= 1) * 2.5
    result +=((matrix["dist"].T > 10) & (matrix["dist"].T <= 15))  * -1
    return result,mfilter
    
def hbw_auto_deficient_inc3(matrix, socio, result): 
    mfilter = socio.total_emp > 0
    result = result.add(np.log(socio.basic_emp + 1).mul(0.24160834), axis=0)
    result = result.add(np.log(socio.ser_emp + 1).mul(0.36310718), axis = 0)
    result = result.add(np.log(socio.ret_emp + 1).mul(-0.09360441), axis = 0)
    result = result.add(socio.hhpop.div(socio.acres).mul(-0.07379568).fillna(0), axis = 0)
    result = result.add(socio.total_emp.div(socio.acres).mul(0.00410132).fillna(0), axis = 0)
    result += matrix['mc_hbw_auto_deficient_logsum_op'].T * 0.31493654
    result += matrix['avgtt'].T * -0.05689183
    result += (matrix["dist"].T <= 2.5) * 1.75
    result +=((matrix["dist"].T > 5) & (matrix["dist"].T <= 7.5))  * 1.25
    return result,mfilter
    
def hbw_auto_sufficient_inc1(matrix, socio, result): 
    mfilter = socio.total_emp > 0
    result = result.add(np.log(socio.basic_emp + 1).mul(0.24160834), axis=0)
    result = result.add(np.log(socio.ser_emp + 1).mul(0.36310718), axis = 0)
    result = result.add(np.log(socio.ret_emp + 1).mul(-0.09360441), axis = 0)
    result = result.add(socio.hhpop.div(socio.acres).mul(-0.07379568).fillna(0), axis = 0)
    result = result.add(socio.total_emp.div(socio.acres).mul(0.00410132).fillna(0), axis = 0)
    result += matrix['mc_hbw_auto_sufficient_logsum_op'].T * 0.31493654
    result += matrix['avgtt'].T * -0.05689183
    result += (matrix["dist"].T <= 1) * 2
    result +=((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5))  * 1
    result +=((matrix["dist"].T > 2.5) & (matrix["dist"].T <= 5))  * 0.25
    return result,mfilter
    
def hbw_auto_sufficient_inc2(matrix, socio, result): 
    mfilter = socio.total_emp > 0
    result = result.add(np.log(socio.basic_emp + 1).mul(0.24160834), axis=0)
    result = result.add(np.log(socio.ser_emp + 1).mul(0.36310718), axis = 0)
    result = result.add(np.log(socio.ret_emp + 1).mul(-0.09360441), axis = 0)
    result = result.add(socio.hhpop.div(socio.acres).mul(-0.07379568).fillna(0), axis = 0)
    result = result.add(socio.total_emp.div(socio.acres).mul(0.00410132).fillna(0), axis = 0)
    result += matrix['mc_hbw_auto_sufficient_logsum_op'].T * 0.31493654
    result += matrix['avgtt'].T * -0.05689183
    result += (matrix["dist"].T <= 5) * 0.7
    return result,mfilter
    
def hbw_auto_sufficient_inc3(matrix, socio, result): 
    mfilter = socio.total_emp > 0
    result = result.add(np.log(socio.basic_emp + 1).mul(0.24160834), axis=0)
    result = result.add(np.log(socio.ser_emp + 1).mul(0.36310718), axis = 0)
    result = result.add(np.log(socio.ret_emp + 1).mul(-0.09360441), axis = 0)
    result = result.add(socio.hhpop.div(socio.acres).mul(-0.07379568).fillna(0), axis = 0)
    result = result.add(socio.total_emp.div(socio.acres).mul(0.00410132).fillna(0), axis = 0)
    result += matrix['mc_hbw_auto_sufficient_logsum_op'].T * 0.31493654
    result += matrix['avgtt'].T * -0.05689183
    result += (matrix["dist"].T <= 2.5) * 0.7
    result +=((matrix["dist"].T > 10) & (matrix["dist"].T <= 20))  * -1
    return result,mfilter
    
def nhbw_all(matrix, socio, result): 
    mfilter = socio.total_emp > 0
    result = result.add(np.log(socio.basic_emp + 1).mul(0.138), axis=0)
    result = result.add(np.log(socio.ser_emp + 1).mul(0.23), axis = 0)
    result = result.add(np.log(socio.naics722 + 1).mul(0.169), axis = 0)
    result = result.add(socio.hhpop.div(socio.acres).mul(-0.047).fillna(0), axis = 0)
    result = result.add(socio.total_emp.div(socio.acres).mul(0.004).fillna(0), axis = 0)
    result += matrix['mc_nhbw_all_logsum_op'].T * 0.216
    result += matrix['optime'].T * -0.197
    result += np.power(matrix['dist'].T, 2) * 0.004
    result += np.power(matrix['dist'].T, 3) * -0.0000222
    result += (matrix["dist"].T <= 1) * 1.7
    result +=((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5))  * 0.7    
    result +=((matrix["dist"].T > 5) & (matrix["dist"].T <= 25))  * -0.5
    return result,mfilter
    
def hbrec_auto_0(matrix, socio, result): 
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))
    result = result.add(np.log(socio.naics71 + 1).mul(0.325), axis = 0)    
    result = result.add(np.log(socio.naics722 + 1).mul(0.247), axis = 0)
    result += matrix['mc_hbrec_auto_0_logsum_op'].T * 0.083   
    result += matrix['optime'].T * -0.297
    result += np.power(matrix['dist'].T, 2) * 0.008   
    result += np.power(matrix['dist'].T, 3) * -0.0000703 
    result += (matrix["dist"].T <= 1) * 2.8
    result +=((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5))  * 0.3    
    return result,mfilter
    
def hbrec_auto_deficient(matrix, socio, result): 
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))
    result = result.add(np.log(socio.naics71 + 1).mul(0.325), axis = 0)    
    result = result.add(np.log(socio.naics722 + 1).mul(0.247), axis = 0)
    result += matrix['mc_hbrec_auto_deficient_logsum_op'].T * 0.083    
    result += matrix['optime'].T * -0.297
    result += np.power(matrix['dist'].T, 2) * 0.008    
    result += np.power(matrix['dist'].T, 3) * -0.0000703 
    result += (matrix["dist"].T <= 1) * 1.05
    result +=((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5))  * -0.1    
    return result,mfilter
    
def hbrec_auto_sufficient(matrix, socio, result): 
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))
    result = result.add(np.log(socio.naics71 + 1).mul(0.325), axis = 0)    
    result = result.add(np.log(socio.naics722 + 1).mul(0.247), axis = 0)
    result += matrix['mc_hbrec_auto_sufficient_logsum_op'].T * 0.083    
    result += matrix['optime'].T * -0.297
    result += np.power(matrix['dist'].T, 2) * 0.008    
    result += np.power(matrix['dist'].T, 3) * -0.0000703 
    result += (matrix["dist"].T <= 1) * 0.9
    result +=((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5))  * 0.15   
    return result,mfilter
    
def hbshop_auto_0(matrix, socio, result): 
    mfilter = socio.ret_emp > 0
    result = result.add(np.log(socio.naics44 + 1).mul(0.453), axis = 0)     
    result = result.add(np.log(socio.naics722 + 1).mul(0.355), axis = 0)
    result = result.add(socio.ret_emp.div(socio.total_emp).mul(.692).fillna(0), axis = 0)    
    result += matrix['mc_hbshop_auto_0_logsum_op'].T * 0.448    
    result += matrix['optime'].T * -0.345    
    result += np.power(matrix['dist'].T, 2) * 0.01       
    result += np.power(matrix['dist'].T, 3) * -0.0000906   
    result += (matrix["dist"].T <= 1) * 2.2    
    result +=((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5))  * 1 
    return result,mfilter
    
def hbshop_auto_deficient(matrix, socio, result): 
    mfilter = socio.ret_emp > 0
    result = result.add(np.log(socio.naics44 + 1).mul(0.453), axis = 0)
    result = result.add(np.log(socio.naics722 + 1).mul(0.355), axis = 0)
    result = result.add(socio.ret_emp.div(socio.total_emp).mul(.692).fillna(0), axis = 0)   
    result += matrix['mc_hbshop_auto_deficient_logsum_op'].T * 0.448  
    result += matrix['optime'].T * -0.345    
    result += np.power(matrix['dist'].T, 2) * 0.01  
    result += np.power(matrix['dist'].T, 3) * -0.0000906  
    result += (matrix["dist"].T <= 1) * 0.25 
    result +=((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5))  * 0.4 
         
    return result,mfilter
    
def hbshop_auto_sufficient(matrix, socio, result): 
    mfilter = socio.ret_emp > 0
    result = result.add(np.log(socio.naics44 + 1).mul(0.453), axis = 0)
    result = result.add(np.log(socio.naics722 + 1).mul(0.355), axis = 0)
    result = result.add(socio.ret_emp.div(socio.total_emp).mul(.692).fillna(0), axis = 0)   
    result += matrix['mc_hbshop_auto_sufficient_logsum_op'].T * 0.448  
    result += matrix['optime'].T * -0.345    
    result += np.power(matrix['dist'].T, 2) * 0.01  
    result += np.power(matrix['dist'].T, 3) *-0.0000906
    result += (matrix["dist"].T <= 1) * 0.25
    result +=((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5))  * 0.25 
    return result,mfilter
    
def hbo_auto_0(matrix, socio, result): 
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))
    result = result.add(np.log(socio.naics722 + 1).mul(0.175), axis = 0)  
    result = result.add(np.log(socio.naics61 + 1).mul(0.167), axis = 0)
    result = result.add(socio.ser_emp.div(socio.acres).mul(0.008).fillna(0), axis = 0)   
    result = result.add(socio.ret_emp.div(socio.acres).mul(-0.052).fillna(0), axis = 0)   
    result = result.add(socio.hhpop.div(socio.acres).mul(0.019).fillna(0), axis = 0)    
    result += matrix['mc_hbo_auto_0_logsum_op'].T * 0.083
    result += matrix['optime'].T * -0.272
    result += np.power(matrix['dist'].T, 2) * 0.006  
    result += np.power(matrix['dist'].T, 3) * -0.0000577 
    result += (matrix["dist"].T <= 1) * 2.8
    result +=((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5))  * 0.25  
    return result,mfilter
    
def hbo_auto_deficient(matrix, socio, result): 
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))
    result = result.add(np.log(socio.naics722 + 1).mul(0.175), axis = 0)  
    result = result.add(np.log(socio.naics61 + 1).mul(0.167), axis = 0)
    result = result.add(socio.ser_emp.div(socio.acres).mul(0.008).fillna(0), axis = 0)   
    result = result.add(socio.ret_emp.div(socio.acres).mul(-0.052).fillna(0), axis = 0)   
    result = result.add(socio.hhpop.div(socio.acres).mul(0.019).fillna(0), axis = 0)    
    result += matrix['mc_hbo_auto_deficient_logsum_op'].T * 0.083
    result += matrix['optime'].T * -0.272
    result += np.power(matrix['dist'].T, 2) * 0.006  
    result += np.power(matrix['dist'].T, 3) * -0.0000577   
    result += (matrix["dist"].T <= 1) * 1.2
    result +=((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5))  * 0.3  
    return result,mfilter
    
def hbo_auto_sufficient(matrix, socio, result): 
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))
    result = result.add(np.log(socio.naics722 + 1).mul(0.175), axis = 0)  
    result = result.add(np.log(socio.naics61 + 1).mul(0.167), axis = 0)
    result = result.add(socio.ser_emp.div(socio.acres).mul(0.008).fillna(0), axis = 0)   
    result = result.add(socio.ret_emp.div(socio.acres).mul(-0.052).fillna(0), axis = 0)   
    result = result.add(socio.hhpop.div(socio.acres).mul(0.019).fillna(0), axis = 0)    
    result += matrix['mc_hbo_auto_sufficient_logsum_op'].T * 0.083
    result += matrix['optime'].T * -0.272
    result += np.power(matrix['dist'].T, 2) * 0.006  
    result += np.power(matrix['dist'].T, 3) * -0.0000577 
    result += (matrix["dist"].T <= 1) * 1.1
    result +=((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5))  * 0.15
    return result,mfilter
    
def nhbo_all(matrix, socio, result): 
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))    
    result = result.add(np.log(socio.naics722 + 1).mul(0.294), axis = 0)    
    result = result.add(np.log(socio.naics61 + 1).mul(0.105), axis = 0)
    result = result.add(socio.ret_emp.div(socio.acres).mul(0.064).fillna(0), axis = 0)    
    result = result.add(socio.hhpop.div(socio.acres).mul(-0.015).fillna(0), axis = 0)     
    result += matrix['mc_nhbo_all_logsum_op'].T * 0.195    
    result += matrix['optime'].T * -0.285    
    result += np.power(matrix['dist'].T, 2) * 0.007    
    result += np.power(matrix['dist'].T, 3) * -0.0000651 
    result += (matrix["dist"].T <= 1) * 1.5    
    result +=((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5))  * 0.5    
    return result,mfilter
    
def hbesms_all(matrix, socio, result): 
    mfilter = socio.enroll > 0
    result = result.add(np.log(socio.es_enr + 1).mul(0.216), axis = 0)    
    result = result.add(np.log(socio.ms_enr + 1).mul(0.153), axis = 0)    
    result = result.add(np.log(socio.enrl_priem + 1).mul(0.211), axis = 0)   
    result = result.add(np.log(socio.enroll_cha + 1).mul(0.083), axis = 0)    
    result += matrix['mc_hbesms_all_logsum_op'].T * 0.438    
    result += matrix['optime'].T * -0.25       
    result += np.power(matrix['dist'].T, 2) * 0.003     
    result += (matrix["dist"].T <= 1) * 1.7        
    result +=((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5))  * 1.7    
    return result,mfilter   

def hbhigh_all(matrix, socio, result): 
    mfilter =  ((socio.hs_enr > 0) | (socio.enrl_prihs > 0))
    result = result.add(np.log(socio.hs_enr + 1).mul(1.886), axis = 0) 
    result = result.add(np.log(socio.enrl_prihs + 1).mul(1.977), axis = 0) 
    result = result.add(socio.basic_emp.div(socio.acres).mul(0.841).fillna(0), axis = 0) 
    result += matrix['optime'].T * -0.341     
    result += np.power(matrix['dist'].T, 2) * 0.008 
    result += np.power(matrix['dist'].T, 3) * -0.0000547 
    result += (matrix["dist"].T <= 1) * 3        
    result +=((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5))  * 1
    result +=((matrix["dist"].T > 2.5) & (matrix["dist"].T <= 5))  * 0.8
    return result,mfilter
    
def hbuniv_all(matrix, socio, result):
    mfilter = socio.hhpop > 0
    result += matrix['mc_hbo_auto_deficient_logsum_op'] * 0.4
    result = result.add(socio.hhpop.mul(0.000272),axis=0)
    result = result.add((socio.gqpop).mul(-0.000244),axis = 0)
    result = result.add((socio.ret_emp).mul(0.00015), axis=0)
    result = result.add((socio.ser_emp).mul(-0.000221), axis=0)
    result = result.add(socio.mfdu.div(socio.du).mul(0.52).fillna(0), axis = 0)
    result = result.add(socio.inc_3.div(socio.tot_inc).mul(1.715).fillna(0), axis = 0)
    result = result.add((socio.popden1).mul(0.106), axis=0)
    result = result.add((socio.total_empden4).mul(-0.756), axis=0)
    result += (matrix["distance"] <= 2.5) * 2.8
    result +=((matrix["distance"] > 2.5) & (matrix["distance"] <= 5))  * 1.4
    result += (matrix["distance"] > 30) * -1.5 
    result = result.add((socio.p_dev).mul(0.00614), axis=0)
    return result,mfilter
    
def nhbuniv_all(matrix, socio, result): 
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))
    result += matrix['mc_nhbo_all_logsum_op'] * 0.95    
    result = result.add((socio.ret_emp).mul(0.001006), axis=0)
    result = result.add((socio.ser_emp).mul(-0.000099), axis=0)    
    result = result.add(socio.mfdu.div(socio.du).mul(-0.556).fillna(0), axis = 0)
    result += (matrix["distance"] <= 2.5) * 4.5
    result += (matrix["distance"] > 15) * -2
    result += matrix["dist"].mul(socio.propp2, axis = 0).mul(0.14)
    result = result.add(socio.inc_3.div(socio.tot_inc).mul(0.00053).fillna(0), axis = 0)
    result = result.add((socio.popden1).mul(0.511), axis=0) 
    result = result.add((socio.total_empden1).mul(0.183), axis=0) 
    result = result.add((socio.p_dev).mul(0.01733), axis=0)  
    return result,mfilter