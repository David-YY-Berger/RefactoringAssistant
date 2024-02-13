import os
import re

from src.gen_files import file_utils as fu, paths as p, gen_scripts as gs, test_class_funcs as tcf, csv_pandas_ops as cpo
from src.gen_files.ConsoleHelpers import input_helper as ih
import xml.etree.ElementTree as ET

testng_server_content = p.testng_header + ',' + p.server_header + """
testng.xml,-
testngAPIData.xml,-
testngAcqAng.xml,-
testngAcqConfig.xml,-
testngAcqConfigNG.xml,-
testngAcqManageSetNG.xml,-
testngAcqNG_Part1.xml,QAC01
testngAcqNG_Part2.xml,QAC01
testngAcqNG_Part3.xml,QAC01
testngAcqNG_Part4.xml,QAC01
testngAcqNG_Part5.xml,QAC01
testngAcqNG_Part6.xml,QAC01
testngAcqNG_Part7.xml,QAC01
testngAcqNetwork.xml,QAC01
testngAcqNetworkNG.xml,QAC01
testngAcqProblematic.xml,-
testngAcq_Part1.xml,-
testngAcq_Part2.xml,-
testngAcq_Part3.xml,-
testngAcq_Part4.xml,-
testngAcq_Part5.xml,-
testngAcq_Part6.xml,-
testngAcq_weekend.xml,-
testngAfterClone_Primo_CrossServers.xml,-
testngAfterClone_QAC01.xml,QAC01
testngAfterClone_QAC01_Base.xml,QAC01
testngAfterClone_QAC01_Digital.xml,QAC01
testngAfterClone_QAC01_Fulf.xml,QAC01
testngAfterClone_QAC01_Letters.xml,QAC01
testngAfterClone_QAC01_MailConf.xml,QAC01
testngAfterClone_QAC01_Primo.xml,QAC01
testngAfterClone_QAC01_Rsh.xml,QAC01
testngAfterClone_QAC01_Users.xml,QAC01
testngAfterClone_SQA_EU01.xml,SQA_EU01
testngAfterClone_SQA_EU02.xml,SQA_EU02
testngAfterClone_SQA_EU04.xml,SQA_EU04
testngAfterClone_SQA_NA01.xml,SQA_NA01
testngAlliance.xml,SQA_NA01
testngAlmaEConfig.xml,-
testngAlmaENetworkConfig.xml,-
testngAlmaE_Part1.xml,QAC01
testngAlmaE_Part2.xml,QAC01
testngAnalysisOfTestResults.xml,-
testngAnalytics.xml,-
testngAnalyticsNewUi.xml,-
testngApiJson.xml,-
testngAuthoritiesDataProjectSingleTest.xml,-
testngAuthorityDataProject.xml,-
testngAuthority_Part1.xml,QAC01
testngAuthority_Part2.xml,QAC01
testngAuthority_Part3.xml,QAC01
testngAuthority_Part4.xml,QAC01
testngAvishai.xml,IGNORE
testngBibSys.xml,-
testngCDI.xml,-
testngCleanupGMail.xml,-
testngCounter.xml,QAC01
testngDBQAQueries.xml,-
testngDBQASingleQuery.xml,-
testngDBvisualizer.xml,-
testngDana.xml,IGNORE
testngDeveloperPortal.xml,-
testngDigital1.xml,QAC01
testngDigital2.xml,QAC01
testngDigital3.xml,-
testngDigital4.xml,QAC01
testngDigital5.xml,QAC01
testngDigitalManageSetsNG.xml,-
testngDownloadResultsFromJenkins.xml,-
testngEBookCentralJob.xml,-
testngEBookCentralJobRes.xml,-
testngERM1.xml,QAC01
testngERM2.xml,QAC01
testngEli.xml,IGNORE
testngElisheva.xml,IGNORE
testngExportPortfolioUrl.xml,-
testngFeatureFlagsRestoration.xml,-
testngFixLogin.xml,-
testngFulf1.xml,QAC01
testngFulf2.xml,QAC01
testngFulf3.xml,QAC01
testngFulf4.xml,QAC01
testngFulf5.xml,QAC01
testngFulf6.xml,QAC01
testngFulfConfig.xml,-
testngFulfConsortia.xml,-
testngFulfNG1.xml,SQA02_NA03
testngFulfNG2.xml,SQA02_NA03
testngFulfNG3.xml,SQA02_NA03
testngFulfNG4.xml,SQA02_NA03
testngFulfNG5.xml,SQA02_NA03
testngFulfNG6.xml,SQA02_NA03
testngFulfNetworkCZ.xml,-
testngFulfRFID.xml,SQA_EU01
testngFulfRshNetwork.xml,-
testngGuy.xml,IGNORE
testngHackathon.xml,-
testngHadarK.xml,IGNORE
testngHaim.xml,IGNORE
testngIdo.xml,IGNORE
testngIndexingJob.xml,-
testngLeganto.xml,-
testngLegantoDevelopers.xml,-
testngMDE_QAC01_SQA03_Part1.xml,QAC01
testngMDE_QAC01_SQA03_Part2.xml,QAC01
testngMDE_SQA_EU04.xml,SQA_EU04
testngMayM.xml,-
testngMigration_CheckResults.xml,-
testngMigration_DbTablesAndColumns.xml,-
testngMigration_RunLoaders.xml,-
testngMobile.xml,-
testngNgrs_Multi_ENV.xml,-
testngNgrs_QAC01.xml,QAC01
testngNgrs_SQANA02.xml,-
testngNgrs_SQA_EU01.xml,SQA_EU01
testngNgrs_SQA_EU01_2.xml,SQA_EU01
testngOBI.xml,-
testngOBI_QQ.xml,-
testngOBI_QQ_Base.xml,-
testngPRM_Part1_SQA03_NA03.xml,QAC01
testngPRM_Part2_SQA03_NA03.xml,QAC01
testngPRM_Part3_SQA03_NA03.xml,QAC01
testngPRM_Part4_SQA03_NA03.xml,QAC01
testngPostDeploymentAcq.xml,-
testngPostDeploymentFulf.xml,-
testngPostDeploymentRM.xml,-
testngPrimo.xml,QAC01
testngPrimoNetwork.xml,SQA_NA01
testngPrimoWeekends.xml,QAC01
testngProviderZone.xml,-
testngPublishingNetwork.xml,SQA_NA01
testngPublishingSplit1.xml,QAC01
testngPublishingSplit2.xml,QAC01
testngPublishingSplit3.xml,QAC01
testngPublishingSplit_sqa_eu01_1.xml,SQA_EU01
testngPublishingSplit_sqa_eu01_2.xml,SQA_EU01
testngPublishingSplit_sqa_eu01_3.xml,SQA_EU01
testngPublishingSplit_sqa_na01_1.xml,SQA_NA01
testngPublishingSplit_sqa_na01_2.xml,SQA_NA01
testngPublishingWeekends.xml,QAC01
testngPublishing_QAC01.xml,QAC01
testngRMConfigAfterClone.xml,-
testngRM_EX_SQA03_NA03.xml,QAC01
testngRSh.xml,-
testngRSh1.xml,QAC01
testngRSh1NG.xml,QAC01
testngRSh1NGPart2.xml,QAC01
testngRSh1Part2.xml,QAC01
testngRSh2.xml,-
testngRSh2NGPart2.xml,-
testngRSh2Part2.xml,-
testngRSh3.xml,-
testngRShNetwork.xml,SQA_EU01
testngRShNetworkPart2.xml,SQA_EU01
testngRShNetworkNG.xml,SQA_EU01
testngRShNetworkNGPart2.xml,SQA_EU01
testngRSh_QAC01-NEU.xml,QAC01
testngRSh_QAC01-VCU.xml,QAC01
testngRSh_RAPIDILL_QAC01.xml,QAC01
testngRanR.xml,-
testngRapidoGTI_QAC01.xml,QAC01
testngRapidoGTI_SQA03_NA03.xml,QAC01
testngRapidoGTI_SQA_EU04.xml,SQA_EU04
testngRapidoSA_URM05.xml,-
testngRapido_AfterClone.xml,-
testngRapido_Config_MultiENV_AfterClone.xml,-
testngRapido_Multi_ENV.xml,-
testngRapido_SQA03_NA03.xml,QAC01
testngRapido_SQA_EU01_1.xml,SQA_EU01
testngRapido_SQA_EU01_2.xml,SQA_EU01
testngRapido_SQA_EU02_MultiplePod.xml,SQA_EU02
testngRapido_SQA_EU03_1.xml,SQA_EU03
testngRapido_SQA_NA01_1.xml,SQA_NA01
testngRapido_SQA_NA01_2.xml,SQA_NA01
testngRapido_SQA_NA01_3.xml,SQA_NA01
testngRialto1.xml,-
testngRialto2.xml,-
testngRialto3.xml,-
testngRialto4.xml,-
testngRialto5.xml,-
testngRialto6.xml,-
testngSendRequestsNotificationCheckResults_1.xml,-
testngSendRequestsNotification_1.xml,-
testngShayli.xml,IGNORE
testngSmartRecommendations.xml,-
testngSmartRecommendationsNet.xml,-
testngSmoke.xml,-
testngSyncCZJob.xml,-
testngSyncCZ_All.xml,-
testngSyncTestrailIds.xml,-
testngUResolverLinks.xml,-
testngUsers1.xml,QAC01
testngUsers2.xml,QAC01
testngUsersNetwork.xml,SQA_NA01
testngUsersWeekends.xml,QAC01
testngUsers_FULFNG.xml,-
testngZ3950.xml,-
testngZalman.xml,IGNORE
testng_ACC.xml,SQA_EU02
testng_ConfigAfterClone_AlmaE.xml,-
testng_ConfigAfterClone_AlmaENetwork.xml,-
testng_GTI.xml,-
testng_Jenkins_Uptime.xml,-
testng_Release_MDE_SQA03_EU01.xml,SQA_EU01
testng_Release_MDE_SQA_NA01.xml,SQA_NA01
testng_SQA_EU01_Authority_Part1.xml,SQA_EU01
testng_SQA_EU01_Authority_Part2.xml,SQA_EU01
testng_SQA_EU01_ERM.xml,SQA_EU01
testng_SQA_EU01_MDE.xml,SQA_EU01
testng_SQA_NA01_ERM.xml,SQA_NA01
testng_SQA_NA01_MDE.xml,SQA_NA01
testng_SQA_NA01_PRM.xml,SQA_NA01
testngYaelS.xml,IGNORE
"""


def create_testng_server_csv():
    fu.write_txt_to_file(p.testng_server_csv_path, testng_server_content)


def init_maps():
    gs.clear_create_dir(p.temp_dir)

    if not os.path.exists(p.test_project_base_txt_file_path):
        with open(p.test_project_base_txt_file_path, 'w') as file:
            file.write(r'C:\urm\workspace-1.0.0.2-URM\alma_itest_ux\src\test')

    with open(p.test_project_base_txt_file_path, 'r') as file:
        p.test_project_base_path = file.read().strip()
    if not os.path.isdir(p.test_project_base_path):
        ih.reassign_project_path()
    p.testng_dir_orig = os.path.join(p.test_project_base_path, "resources")
    p.all_tests_dir = os.path.join(p.test_project_base_path, "java", "tests")

    create_testng_server_csv()
    fill_dict_file_name_to_path(p.all_tests_dir)
    fill_dict_testng_to_test_name(p.testng_dir_orig)
    # fill_dict_test_objs_from_testng(p.testng_dir_orig)



# def fill_dict_test_objs_from_testng(testng_dir_orig):
#
#     test_obj_list = []
#     testng_files_paths = gs.get_paths_from_dir(testng_dir_orig)
#     for testng_file_path in testng_files_paths:
#         class_names = get_class_name_from_testng_file(testng_file_path)
#         for class_name in class_names:
#             test_obj = tcf.get_test_obj_from_class_name(class_name)
#             test_obj.testng_file_name = os.path.basename(testng_file_path)
#             test_obj_list.append(test_obj)
#     cpo.create_csv_from_test_obj_list(test_obj_list=test_obj_list, path=p.init_dict_test_obj_from_testng)


def fill_dict_testng_to_test_name(testng_dir):
    testng_files_paths = gs.get_paths_from_dir(testng_dir)

    with open(p.init_dict_testng_to_test_name, 'w') as file:
        file.write(p.test_name_header + "," + p.testng_header + "\n")

    with open(p.init_dict_testng_to_test_name, 'a') as temp_dict:
        for testng_file in testng_files_paths:
            test_names=get_test_names_from_testng_file(testng_file)
            for test_name in test_names:
                temp_dict.write(test_name + ',' + os.path.basename(testng_file) + "\n")
def get_class_name_from_testng_file(testng_file):
    class_names_list = []
    tree = ET.parse(testng_file)
    root = tree.getroot()

    for test_elem in root.findall(".//test"):
        for class_elem in test_elem.findall(".//class"):
            class_name = class_elem.get("name")
            if class_name:
                class_names_list.append(class_name)
    return class_names_list


def fill_dict_file_name_to_path(dir_with_tests):
    with open(p.init_dict_file_name_to_path, 'w') as file:
        file.write(p.file_name_header + "," + p.test_path_header + "\n")
    rec_fill_name_to_path_dict(dir_with_tests)


# def fill_dict_test_name_to_path_from_testng_files():
#     test_names = gs.get_all_test_names_in_testng_files()
#     test_obj_list = tcf.get_test_obj_list_w_path_from_name_list(test_names)
#     cpo.create_csv_from_test_obj_list(test_obj_list, p.init_dict_test_name_to_path)


def rec_fill_name_to_path_dict(src_dir):
    with open(p.init_dict_file_name_to_path, 'a') as temp_dict:
        for f_name in os.listdir(src_dir):
            f_path = os.path.join(src_dir, f_name)
            if os.path.isfile(f_path):
                f_name = gs.trim_suffix(f_name)
                # f_name = f_name.lower()
                temp_dict.write(f_name + "," + f_path + "\n")
            if os.path.isdir(f_path):
                rec_fill_name_to_path_dict(os.path.join(src_dir, f_path))


def get_test_names_from_testng_file(filepath):
    test_names = []

    tree = ET.parse(filepath)
    root = tree.getroot()

    for test_elem in root.findall(".//test"):
        for class_elem in test_elem.findall(".//class"):
            class_name = class_elem.get("name")
            if class_name:
                test_names.append(class_name)

    return [s.split('.')[-1] for s in test_names]
