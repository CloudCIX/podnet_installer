from data_blob import data_blob

#################################################################################
#  Test Print the Data Blob    (Run when you execute this program but not run   #
#            when calling the module data_blob function from external import)   #
#################################################################################
#  i)    host_status and host_status_text                                       #
#  Bit Maps                                                                     #
#  ii)   The 'pass_map' showing the tests with a pass                           #
#  iii)  The 'warn_map' showing the tests with a warn                           #
#  iv)   The 'fail_map' showing the tests with a fail                           #
#  Test Result Dictionary                                                       #
#  v)    A list of test_result with key = test_id                               #
#################################################################################

host_status, host_status_text, pass_map, warn_map, fail_map, test_result = data_blob()

print()
print("i)     Host Status: ", host_status)
print("========================================")
print()
print(" Result Maps")
print("========================================")
print()
print("ii)   The 'pass_map' showing the tests with a pass")
print("pass_map                        ", "{:0b}".format(pass_map))
print()
print("iii)  The 'warn_map' showing the tests with a warn")
print("warn_map                        ", "{:0b}".format(warn_map))
print()
print("iv)   The 'fail_map' showing the tests with a fail")
print("fail_map                        ", "{:0b}".format(fail_map))
print()
print("v     Test Results")
print("========================================")
for i in test_result:
    print(i)
