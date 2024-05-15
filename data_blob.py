#################################################################################
#                                                                               #
#  PURPOSE OF MODULE                                                            #
#-------------------------------------------------------------------------------#
# This MODULE produces a blob of data to populate the installer GUI             #
# The data blob describes every property of the host and identifies             #
#   invalid or inconsistant data                                                #
# Think of it as an API read backend for the installer GUI                      #
# It is not concerned about GUI or update operations                            #
#                                                                               #
#===============================================================================#
#                                                                               #
#  HOST STATUS                                                                  #
#-------------------------------------------------------------------------------#
# The program establishes a 'host-status' state for the host being run          #
#     a) 'host' is derived from the hostname of the host running the program    #
#     b) 'status' is based on                                                   #
#           i)  whether CIDATA USB is plugged in                                #
#           ii) if CIDATA is plugged in, whether podnet-b is enabled            #
#     There are seven possible 'host-status'                                    #
#                                                                               #
#===============================================================================#
#                                                                               #
#  DATA CONSTANT BIT MAPS                                                       #
#-------------------------------------------------------------------------------#
#   The program checks consistency by performing comparisons called tests       #
#   Each test has a function call and test limit values are passed in the call  #
#   Each test has an id from 0 up, called the test_id                           #
#   Each test has a test_bit uses to index bit strings test_bit = test_id ** 2  #
#   The test_bit is used for bitwise operations on binary numbers called maps   #
#     Data Constant Maps                                                        #
#       For each of the seven 'host-status'                                     #
#         A 'warn' map is hard coded to identify tests that are                 #
#            warning for this host-status                                       #
#         A 'fail' map is hard coded to identify tests that are                 #
#            failing for this host-status                                       #
#         A 'ignore' map is computed each test not a 'warn' or 'fail'           #
#                                                                               #
#   Thus this progam has 21 data constant bit maps (one bit per test)           #
#                                                                               #
#===============================================================================#
#                                                                               #
#  PER HOST-STATUS VALIDATION (Performing the Tests)                            #
#-------------------------------------------------------------------------------#
# The program checks the validity of the 'host-status' by a set of tests        #
#   Each test is a comparison. Six types of tests exist...                      #
#                                                                               #
# There are four data types to compare...                                       #
#    1) 'CIDATA' are the contents of the CIDATA USB Stick                       #
#         Loaded into dictionaries                                              #
#    2) 'instanciated infra' is the way the host is currently configured        #
#         Read by sys calles to the host                                        #
#    3) 'instanciated metadata' is the contents of the data files on the host   #
#         Loaded into dictionaries                                              #
#    4) 'test values', hard coded limits                                        #
#         Sent as params to the test procedures                                 #
#                                                                               #
# Graph theory suggests that with four nodes(data types) there are six edges    #
# plus four loop edges (= 10 test types):                                       #
#    1)  CIDATA                 versus instanciated infra                       #
#    2)  CIDATA                 versus instanciated metadata                    #
#    3)  CIDATA                 versus test values                              #
#    4)  instanciated infra     versus instanciated metadata                    #
#    5)  instanciated infra     versus test values                              #
#    6)  instanciated metadata  versus test values                              #
#    7)  CIDATA                 versus CIDATA                                   #
#    8)  instanciated infra     versus instanciated infra                       #
#    9)  instanciated metadata  versus instanciated metadata                    #
#    10) test value             versus test value                               #
#                                                                               #
#===============================================================================#
#                                                                               #
#  RETURNING VALIDATED DATA                                                     #
#-------------------------------------------------------------------------------#
#  This program is run as a function whose job is to return a blob of data      #
#  data to be utilised by the GUI. This is the returned data blob definition    #
#                                                                               #
#  i)    host_status and host_status_text                                       #
#  Bit Maps                                                                     #
#  ii)   The 'pass_map' showing the tests with a pass                           #
#  iii)  The 'warn_map' showing the tests with a warn                           #
#  iv)   The 'fail_map' showing the tests with a fail                           #
#  Test Result Dictionary                                                       #
#  v)    A list of test_result with key = test_id                               #
#                                                                               #
#################################################################################

# stdlib
# lib
# local
from sql_utils import (
    get_cidata,
    get_host_details,
    get_instanciated_infra,
    get_test_bit_map,
    get_test_results,
    insert_host_status,
    set_up_sqlite,
    update_fail_map,
    update_test_levels,
)
from tests import *


__all__ = [
    'data_blob',
]


##  Host Status Bitwise Encoding  ##
# hostname (bits 1 to 3 with 4 to 6 kept for future use)
podnet_a, podnet_b, appliance_a = 1, 2, 4

# status (bits 7 to 9)
validate, install, reinstall = 64, 128, 256

# host_status
podnet_a_validate    = podnet_a    + validate      # 65
podnet_a_install     = podnet_a    + install       # 129
podnet_a_reinstall   = podnet_a    + reinstall     # 257
podnet_b_validate    = podnet_b    + validate      # 66
podnet_b_install     = podnet_b    + install       # 130
appliance_a_validate = appliance_a + validate      # 68
appliance_a_install  = appliance_a + install       # 132


def data_blob():

    set_up_sqlite()

    # CIDATA dictionary will have content if CIDATA USB is mounted
    cidata = get_cidata()
    if cidata == {}:
        cidata_mountable = False
        podnet_b_enabled = False
    else:
        cidata_mountable = True
        podnet_b_enabled = cidata['config.json'].get('podnet_b_enabled', False)

    # Find the host_status
    instanciated_infra = get_instanciated_infra()
    invert = get_test_bit_map('invert')
    if instanciated_infra['hostname'] == 'podnet-a':
        if cidata_mountable is True:
            if podnet_b_enabled is False:
                host_status = podnet_a_install
                host_status_text = "podnet_a_install"
            else:
                host_status = podnet_a_reinstall
                host_status_text = "podnet_a_reinstall"
        else:
            host_status = podnet_a_validate
            host_status_text = "podnet_a_validate"

    elif instanciated_infra['hostname'] == 'podnet-b':
        if cidata_mountable is True:
            host_status = podnet_b_install
            host_status_text = "podnet_b_install"
        else:
            host_status = podnet_b_validate
            host_status_text = "podnet_b_validate"

    elif instanciated_infra['hostname'] == 'appliance-a':
        if cidata_mountable is True:
            host_status = appliance_a_install
            host_status_text = "appliance_a_install"
        else:
            host_status = appliance_a_validate
            host_status_text = "appliance_a_validate"
    else:
            host_status = 0
            host_status_text = 'Unknown'
            fail_map = invert  # All ones representing all tests have failed
            update_fail_map(fail_map)
    
    insert_host_status(host_status, host_status_text)

    # Determine which maps to use based on host_status
    if host_status == podnet_a_validate:
        warn = get_test_bit_map('podnet_a_validate_warn')
        fail = get_test_bit_map('podnet_a_validate_fail')
    elif host_status == podnet_a_install:
        warn = get_test_bit_map('podnet_a_install_warn')
        fail = get_test_bit_map('podnet_a_install_fail')
    elif host_status == podnet_a_reinstall:
        warn = get_test_bit_map('podnet_a_reinstall_warn')
        fail = get_test_bit_map('podnet_a_reinstall_fail')
    elif host_status == podnet_b_validate:
        warn = get_test_bit_map('podnet_b_validate_warn')
        fail = get_test_bit_map('podnet_b_validate_fail')
    elif host_status == podnet_b_install:
        warn = get_test_bit_map('podnet_b_install_warn')
        fail = get_test_bit_map('podnet_b_install_fail')
    elif host_status == appliance_a_validate:
        warn = get_test_bit_map('appliance_a_validate_warn')
        fail = get_test_bit_map('appliance_a_validate_fail')
    elif host_status == appliance_a_install:
        warn = get_test_bit_map('appliance_a_install_warn')
        fail = get_test_bit_map('appliance_a_install_fail')
    else:
        warn = 0b0
        fail = 0b0
    
    ignore = (warn | fail) ^ invert

    update_test_levels(fail, ignore, warn)

    ##########################################################################
    #      Run the Tests   (test_id, optional test value)                    #
    ##########################################################################

    hard_core_coun(0, 20)
    hard_ram_count(1, 8)
    hard_stor_coun(2, 300)
    hard_pprt_coun(3, 5)
    hard_aprt_coun(4, 1)
    hard_publ_oper(5)
    hard_publ_carr(6)
    hard_publ_ethn(7)
    hard_mgmt_oper(8)
    hard_mgmt_carr(9)
    hard_mgmt_ethn(10)
    hard_oob__oper(11)
    hard_oob__carr(12)
    hard_oob__ethn(13)
    hard_priv_oper(14)
    hard_priv_carr(15)
    hard_priv_ethn(16)
    hard_intr_oper(17)
    hard_intr_carr(18)
    hard_intr_ethn(19)
    config_matches(20)
    inst_conf_pnum(21)
    inst_conf_pnam(22)
    inst_conf_blen(23)
    inst_conf_aena(24)
    inst_conf_aenb(25)
    inst_conf_bena(26)
    inst_conf_benb(27)
    inst_conf_aben(28)
    inst_conf_ip4l(29)
    inst_conf_ip6l(30)
    inst_conf_ip4s(31)
    inst_conf_ip6s(32)
    inst_conf_dnss(33)
    inst_conf_cmon(34)

    pass_map, warn_map, fail_map, test_result = get_test_results()
    host_status, host_status_text = get_host_details()

    return host_status, host_status_text, pass_map, warn_map, fail_map, test_result
