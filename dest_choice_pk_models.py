import numpy as np


def set_model_variables(matrix, socio):
    socio['tothh'] = socio.sfdu + socio.mfdu
    matrix["avgtt"] = 0.5 * matrix['amtime'] + 0.5 * matrix['optime']
    matrix["distance2"] = matrix['dist'].T
    matrix["distance"] = 0.5 * matrix['dist'] + 0.5 * matrix['distance2']
    socio['enroll'] = socio.es_enr + socio.ms_enr + socio.enrl_priem + socio.enroll_cha
    socio['gqpop'] = socio['pop'] - socio.hhpop + socio.dormpop
    socio['tot_inc'] = socio.inc_1 + socio.inc_2 + socio.inc_3
    socio['propp2'] = socio.gqpop.div(socio['pop']).fillna(0)
    return matrix, socio


def hbw_auto_0(matrix, socio, result):

    mfilter = socio.total_emp > 0
    result = result.add(np.log(socio.basic_emp + 1).mul(0.24160834), axis=0)
    result = result.add(np.log(socio.ser_emp + 1).mul(0.36310718), axis=0)
    result = result.add(np.log(socio.ret_emp + 1).mul(-0.09360441), axis=0)
    result = result.add(socio.hhpop.div(socio.acres).mul(-.07379568).fillna(0), axis=0)
    result = result.add(socio.total_emp.div(socio.acres).mul(0.00410132).fillna(0), axis=0)
    result += matrix['mc_hbw_auto_0_logsum_pk'].T * 0.31493654
    result += matrix['avgtt'].T * -0.05689183
    result += (matrix["dist"].T <= 1) * 2.7
    result += ((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5)) * 1.5
    result += (matrix["dist"].T > 5) * -2.5
    return result, mfilter


def hbw_auto_deficient_inc1(matrix, socio, result):
    mfilter = socio.total_emp > 0
    result = result.add(np.log(socio.basic_emp + 1).mul(0.24160834), axis=0)
    result = result.add(np.log(socio.ser_emp + 1).mul(0.36310718), axis=0)
    result = result.add(np.log(socio.ret_emp + 1).mul(-0.09360441), axis=0)
    result = result.add(socio.hhpop.div(socio.acres).mul(-.07379568).fillna(0), axis=0)
    result = result.add(socio.total_emp.div(socio.acres).mul(0.00410132).fillna(0), axis=0)
    result += matrix['mc_hbw_auto_deficient_logsum_pk'].T * 0.31493654
    result += matrix['avgtt'].T * -0.05689183
    result += (matrix["dist"].T <= 1) * 1.5
    result += ((matrix["dist"].T > 2.5) & (matrix["dist"].T <= 7.5)) * 0.7
    return result, mfilter


def hbw_auto_deficient_inc2(matrix, socio, result):
    mfilter = socio.total_emp > 0
    result = result.add(np.log(socio.basic_emp + 1).mul(0.24160834), axis=0)
    result = result.add(np.log(socio.ser_emp + 1).mul(0.36310718), axis=0)
    result = result.add(np.log(socio.ret_emp + 1).mul(-0.09360441), axis=0)
    result = result.add(socio.hhpop.div(socio.acres).mul(-.07379568).fillna(0), axis=0)
    result = result.add(socio.total_emp.div(socio.acres).mul(0.00410132).fillna(0), axis=0)
    result += matrix['mc_hbw_auto_deficient_logsum_pk'].T * 0.31493654
    result += matrix['avgtt'].T * -0.05689183
    result += (matrix["dist"].T <= 1) * 1.5
    result += ((matrix["dist"].T > 5) & (matrix["dist"].T <= 7.5)) * 0.7
    return result, mfilter


def hbw_auto_deficient_inc3(matrix, socio, result):
    mfilter = socio.total_emp > 0
    result = result.add(np.log(socio.basic_emp + 1).mul(0.24160834), axis=0)
    result = result.add(np.log(socio.ser_emp + 1).mul(0.36310718), axis=0)
    result = result.add(np.log(socio.ret_emp + 1).mul(-0.09360441), axis=0)
    result = result.add(socio.hhpop.div(socio.acres).mul(-.07379568).fillna(0), axis=0)
    result = result.add(socio.total_emp.div(socio.acres).mul(0.00410132).fillna(0), axis=0)
    result += matrix['mc_hbw_auto_deficient_logsum_pk'].T * 0.31493654
    result += matrix['avgtt'].T * -0.05689183
    result += (matrix["dist"].T <= 2.5) * 1.2
    result += ((matrix["dist"].T > 5) & (matrix["dist"].T <= 7.5)) * 0.5
    return result, mfilter


def hbw_auto_sufficient_inc1(matrix, socio, result):
    mfilter = socio.total_emp > 0
    result = result.add(np.log(socio.basic_emp + 1).mul(0.24160834), axis=0)
    result = result.add(np.log(socio.ser_emp + 1).mul(0.36310718), axis=0)
    result = result.add(np.log(socio.ret_emp + 1).mul(-0.09360441), axis=0)
    result = result.add(socio.hhpop.div(socio.acres).mul(-.07379568).fillna(0), axis=0)
    result = result.add(socio.total_emp.div(socio.acres).mul(0.00410132).fillna(0), axis=0)
    result += matrix['mc_hbw_auto_sufficient_logsum_pk'].T * 0.31493654
    result += matrix['avgtt'].T * -0.05689183
    result += ((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5)) * 0.75
    result += ((matrix["dist"].T > 2.5) & (matrix["dist"].T <= 5)) * 0.5
    return result, mfilter


def hbw_auto_sufficient_inc2(matrix, socio, result):
    mfilter = socio.total_emp > 0
    result = result.add(np.log(socio.basic_emp + 1).mul(0.24160834), axis=0)
    result = result.add(np.log(socio.ser_emp + 1).mul(0.36310718), axis=0)
    result = result.add(np.log(socio.ret_emp + 1).mul(-0.09360441), axis=0)
    result = result.add(socio.hhpop.div(socio.acres).mul(-.07379568).fillna(0), axis=0)
    result = result.add(socio.total_emp.div(socio.acres).mul(0.00410132).fillna(0), axis=0)
    result += matrix['mc_hbw_auto_sufficient_logsum_pk'].T * 0.31493654
    result += matrix['avgtt'].T * -0.05689183
    result += ((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5)) * 0.75
    return result, mfilter


def hbw_auto_sufficient_inc3(matrix, socio, result):
    mfilter = socio.total_emp > 0
    result = result.add(np.log(socio.basic_emp + 1).mul(0.24160834), axis=0)
    result = result.add(np.log(socio.ser_emp + 1).mul(0.36310718), axis=0)
    result = result.add(np.log(socio.ret_emp + 1).mul(-0.09360441), axis=0)
    result = result.add(socio.hhpop.div(socio.acres).mul(-.07379568).fillna(0), axis=0)
    result = result.add(socio.total_emp.div(socio.acres).mul(0.00410132).fillna(0), axis=0)
    result += matrix['mc_hbw_auto_sufficient_logsum_pk'].T * 0.31493654
    result += matrix['avgtt'].T * -0.05689183
    return result, mfilter


def nhbw_all(matrix, socio, result):
    mfilter = socio.total_emp > 0
    result = result.add(np.log(socio.basic_emp + 1).mul(0.1586466), axis=0)
    result = result.add(np.log(socio.ser_emp + 1).mul(0.26027281), axis=0)
    result = result.add(np.log(socio.naics722 + 1).mul(0.16760461), axis=0)
    result = result.add(socio.hhpop.div(socio.acres).mul(-0.04472726).fillna(0), axis=0)
    result = result.add(socio.total_emp.div(socio.acres).mul(0.0047546).fillna(0), axis=0)
    result += matrix['mc_nhbw_all_logsum_pk'].T * 0.26692736
    result += matrix['amtime'].T * -0.18759527
    result += np.power(matrix['dist'].T, 2) * 0.00549642
    result += np.power(matrix['dist'].T, 3) * -0.0000466333
    result += (matrix["dist"].T <= 1) * 1.3
    result += ((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5)) * 0.5
    return result, mfilter


def hbrec_auto_0(matrix, socio, result):
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))
    result = result.add(np.log(socio.naics71 + 1).mul(0.329), axis=0)
    result = result.add(np.log(socio.naics722 + 1).mul(0.266), axis=0)
    result += matrix['mc_hbrec_auto_0_logsum_pk'].T * 0.247
    result += matrix['amtime'].T * -0.228
    result += np.power(matrix['dist'].T, 2) * 0.007
    result += np.power(matrix['dist'].T, 3) * -0.0000668
    result += (matrix["dist"].T <= 1) * 2.2
    result += ((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5)) * 0.25
    return result, mfilter


def hbrec_auto_deficient(matrix, socio, result):
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))
    result = result.add(np.log(socio.naics71 + 1).mul(0.329), axis=0)
    result = result.add(np.log(socio.naics722 + 1).mul(0.266), axis=0)
    result += matrix['mc_hbrec_auto_deficient_logsum_pk'].T * 0.247
    result += matrix['amtime'].T * -0.228
    result += np.power(matrix['dist'].T, 2) * 0.007
    result += np.power(matrix['dist'].T, 3) * -0.0000668
    result += (matrix["dist"].T <= 1) * 2.2
    result += ((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5)) * 0.25
    return result, mfilter


def hbrec_auto_sufficient(matrix, socio, result):
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))
    result = result.add(np.log(socio.naics71 + 1).mul(0.329), axis=0)
    result = result.add(np.log(socio.naics722 + 1).mul(0.266), axis=0)
    result += matrix['mc_hbrec_auto_sufficient_logsum_pk'].T * 0.247
    result += matrix['amtime'].T * -0.228
    result += np.power(matrix['dist'].T, 2) * 0.007
    result += np.power(matrix['dist'].T, 3) * -0.0000668
    result += (matrix["dist"].T <= 1) * 2
    result += ((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5)) * 0.65
    return result, mfilter


def hbshop_auto_0(matrix, socio, result):
    mfilter = socio.ret_emp > 0
    result = result.add(np.log(socio.naics44 + 1).mul(0.467), axis=0)
    result = result.add(np.log(socio.naics722 + 1).mul(0.361), axis=0)
    result = result.add(socio.ret_emp.div(socio.total_emp).mul(.304).fillna(0), axis=0)
    result += matrix['mc_hbshop_auto_0_logsum_pk'].T * 0.639
    result += matrix['amtime'].T * -0.252
    result += np.power(matrix['dist'].T, 2) * 0.009
    result += np.power(matrix['dist'].T, 3) * -0.0000797
    result += (matrix["dist"].T <= 1) * 2.8
    result += ((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5)) * 1
    result += (matrix["dist"].T > 15) * -1.5
    return result, mfilter


def hbshop_auto_deficient(matrix, socio, result):
    mfilter = socio.ret_emp > 0
    result = result.add(np.log(socio.naics44 + 1).mul(0.467), axis=0)
    result = result.add(np.log(socio.naics722 + 1).mul(0.361), axis=0)
    result = result.add(socio.ret_emp.div(socio.total_emp).mul(.304).fillna(0), axis=0)
    result += matrix['mc_hbshop_auto_deficient_logsum_pk'].T * 0.639
    result += matrix['amtime'].T * -0.252
    result += np.power(matrix['dist'].T, 2) * 0.009
    result += np.power(matrix['dist'].T, 3) * -0.0000797
    result += ((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5)) * 1
    result += (matrix["dist"].T > 15) * -1.5
    return result, mfilter


def hbshop_auto_sufficient(matrix, socio, result):
    mfilter = socio.ret_emp > 0
    result = result.add(np.log(socio.naics44 + 1).mul(0.467), axis=0)
    result = result.add(np.log(socio.naics722 + 1).mul(0.361), axis=0)
    result = result.add(socio.ret_emp.div(socio.total_emp).mul(.304).fillna(0), axis=0)
    result += matrix['mc_hbshop_auto_sufficient_logsum_pk'].T * 0.639
    result += matrix['amtime'].T * -0.252
    result += np.power(matrix['dist'].T, 2) * 0.009
    result += np.power(matrix['dist'].T, 3) * -0.0000797
    result += (matrix["dist"].T <= 1) * 1
    result += ((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5)) * 1
    result += (matrix["dist"].T > 15) * -1.5
    return result, mfilter


def hbo_auto_0(matrix, socio, result):
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))
    result = result.add(np.log(socio.naics722 + 1).mul(0.186), axis=0)
    result = result.add(np.log(socio.naics61 + 1).mul(0.158), axis=0)
    result = result.add(socio.ser_emp.div(socio.acres).mul(0.011).fillna(0), axis=0)
    result = result.add(socio.ret_emp.div(socio.acres).mul(-0.043).fillna(0), axis=0)
    result = result.add(socio.hhpop.div(socio.acres).mul(0.022).fillna(0), axis=0)
    result += matrix['mc_hbo_auto_0_logsum_pk'].T * 0.253
    result += matrix['amtime'].T * -0.203
    result += np.power(matrix['dist'].T, 2) * 0.004
    result += np.power(matrix['dist'].T, 3) * -0.0000449
    result += (matrix["dist"].T <= 1) * 2.8
    result += ((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5)) * 1.1
    return result, mfilter


def hbo_auto_deficient(matrix, socio, result):
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))
    result = result.add(np.log(socio.naics722 + 1).mul(0.186), axis=0)
    result = result.add(np.log(socio.naics61 + 1).mul(0.158), axis=0)
    result = result.add(socio.ser_emp.div(socio.acres).mul(0.011).fillna(0), axis=0)
    result = result.add(socio.ret_emp.div(socio.acres).mul(-0.043).fillna(0), axis=0)
    result = result.add(socio.hhpop.div(socio.acres).mul(0.022).fillna(0), axis=0)
    result += matrix['mc_hbo_auto_deficient_logsum_pk'].T * 0.253
    result += matrix['amtime'].T * -0.203
    result += np.power(matrix['dist'].T, 2) * 0.004
    result += np.power(matrix['dist'].T, 3) * -0.0000449
    result += (matrix["dist"].T <= 1) * 1.7
    result += ((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5)) * 0.45
    return result, mfilter


def hbo_auto_sufficient(matrix, socio, result):
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))
    result = result.add(np.log(socio.naics722 + 1).mul(0.186), axis=0)
    result = result.add(np.log(socio.naics61 + 1).mul(0.158), axis=0)
    result = result.add(socio.ser_emp.div(socio.acres).mul(0.011).fillna(0), axis=0)
    result = result.add(socio.ret_emp.div(socio.acres).mul(-0.043).fillna(0), axis=0)
    result = result.add(socio.hhpop.div(socio.acres).mul(0.022).fillna(0), axis=0)
    result += matrix['mc_hbo_auto_sufficient_logsum_pk'].T * 0.253
    result += matrix['amtime'].T * -0.203
    result += np.power(matrix['dist'].T, 2) * 0.004
    result += np.power(matrix['dist'].T, 3) * -0.0000449
    result += (matrix["dist"].T <= 1) * 1.3
    result += ((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5)) * 0.25
    return result, mfilter


def nhbo_all(matrix, socio, result):
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))
    result = result.add(np.log(socio.naics722 + 1).mul(0.285), axis=0)
    result = result.add(np.log(socio.naics61 + 1).mul(0.097), axis=0)
    result = result.add(np.log(socio.naics54 + 1).mul(0.071), axis=0)
    result = result.add(socio.ret_emp.div(socio.acres).mul(0.066).fillna(0), axis=0)
    result = result.add(socio.hhpop.div(socio.acres).mul(-0.01).fillna(0), axis=0)
    result += matrix['mc_nhbo_all_logsum_pk'].T * 0.287
    result += matrix['amtime'].T * -0.266
    result += np.power(matrix['dist'].T, 2) * 0.01
    result += np.power(matrix['dist'].T, 3) * -0.000116
    result += (matrix["dist"].T <= 1) * 1.25
    result += ((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5)) * 0.4
    return result, mfilter


def hbesms_all(matrix, socio, result):
    mfilter = socio.enroll > 0
    result = result.add(np.log(socio.es_enr + 1).mul(0.218), axis=0)
    result = result.add(np.log(socio.ms_enr + 1).mul(0.152), axis=0)
    result = result.add(np.log(socio.enrl_priem + 1).mul(0.222), axis=0)
    result = result.add(np.log(socio.enroll_cha + 1).mul(0.092), axis=0)
    result = result.add(socio.ser_emp.div(socio.acres).mul(0.015).fillna(0), axis=0)
    result += matrix['mc_hbesms_all_logsum_pk'].T * 0.747
    result += matrix['amtime'].T * -0.171
    result += np.power(matrix['dist'].T, 2) * 0.002
    result += (matrix["dist"].T <= 1) * 1.9
    result += ((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5)) * 0.8
    result += ((matrix["dist"].T > 2.5) & (matrix["dist"].T <= 5)) * 0.3
    return result, mfilter


def hbhigh_all(matrix, socio, result):
    mfilter = ((socio.hs_enr > 0) | (socio.enrl_prihs > 0))
    result = result.add(np.log(socio.hs_enr + 1).mul(1.632), axis=0)
    result = result.add(np.log(socio.enrl_prihs + 1).mul(1.694), axis=0)
    result = result.add(socio.ser_emp.div(socio.acres).mul(0.227).fillna(0), axis=0)
    result += matrix['amtime'].T * -0.274
    result += np.power(matrix['dist'].T, 2) * 0.007
    result += np.power(matrix['dist'].T, 3) * -0.0000506
    result += (matrix["dist"].T <= 1) * 2.9
    result += ((matrix["dist"].T > 1) & (matrix["dist"].T <= 2.5)) * 1
    return result, mfilter


def hbuniv_all(matrix, socio, result):
    mfilter = socio.hhpop > 0
    result += matrix['mc_hbo_auto_deficient_logsum_pk'] * 0.4
    result = result.add(socio.hhpop.mul(0.000272), axis=0)
    result = result.add((socio.gqpop).mul(-0.000244), axis=0)
    result = result.add((socio.ret_emp).mul(0.00015), axis=0)
    result = result.add((socio.ser_emp).mul(-0.000221), axis=0)
    result = result.add(socio.mfdu.div(socio.du).mul(0.52).fillna(0), axis=0)
    result = result.add(socio.inc_3.div(socio.tot_inc).mul(1.715).fillna(0), axis=0)
    result = result.add((socio.popden1).mul(0.106), axis=0)
    result = result.add((socio.total_empden4).mul(-0.756), axis=0)
    result += (matrix["distance"] <= 2.5) * 2.8
    result += ((matrix["distance"] > 2.5) & (matrix["distance"] <= 5)) * 1.4
    result += (matrix["distance"] > 30) * -1.5
    result = result.add((socio.p_dev).mul(0.00614), axis=0)
    return result, mfilter


def nhbuniv_all(matrix, socio, result):
    mfilter = ((socio.total_emp > 0) | (socio.hhpop > 0))
    result += matrix['mc_nhbo_all_logsum_pk'] * 0.783
    result = result.add(socio.hhpop.mul(0.00012610634), axis=0)
    result = result.add((socio.ret_emp).mul(0.0009855646), axis=0)
    result = result.add((socio.inc_1).mul(-0.00122747077), axis=0)
    result = result.add(socio.sfdu.div(socio.du).mul(-0.52263259).fillna(0), axis=0)
    result += (matrix["distance"] <= 2.5) * 4.5
    result += (matrix["distance"] > 15) * -2
    result = result.add((socio.ser_emp).mul(-0.00008365862), axis=0)
    result += matrix["distance"].mul(socio.propp2, axis=0).mul(0.1300047)
    result += matrix["distance"].mul(socio.popden1, axis=0).mul(0.01541049)
    result = result.add((socio.popden4).mul(-0.560306), axis=0)
    result = result.add((socio.total_empden3).mul(0.17449616), axis=0)
    result = result.add((socio.p_dev).mul(1.18155152), axis=0)
    return result, mfilter
