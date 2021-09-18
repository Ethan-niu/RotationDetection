# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import
import os
import tensorflow as tf
import math

from dataloader.pretrained_weights.pretrain_zoo import PretrainModelZoo

"""
r3det + kl + sqrt tau=2
FLOPs: 1262712277;    Trainable params: 37769656

13epoch
{'0.75': {'swimming-pool': 0.09891712452748125, 'helicopter': 0.12032085561497327, 'large-vehicle': 0.6015218571335811, 'storage-tank': 0.6378551748268436, 'soccer-ball-field': 0.5299921199177453, 'roundabout': 0.3634852645547833, 'harbor': 0.22719794640998095, 'baseball-diamond': 0.21252524694273342, 'bridge': 0.09144526399331833, 'basketball-court': 0.5619399009115349, 'tennis-court': 0.8987241044310863, 'mAP': 0.43441594159054214, 'plane': 0.7666838903747283, 'ship': 0.6857873630276102, 'ground-track-field': 0.3581753527349263, 'small-vehicle': 0.36166765845680615},
'0.8': {'swimming-pool': 0.04667528364210828, 'helicopter': 0.05509641873278237, 'large-vehicle': 0.3973752808648695, 'storage-tank': 0.46404754065544784, 'soccer-ball-field': 0.4875522795212273, 'roundabout': 0.23537126715092818, 'harbor': 0.12350998132988655, 'baseball-diamond': 0.10769068392907402, 'bridge': 0.04138496882179193, 'basketball-court': 0.5384188706438824, 'tennis-court': 0.876004203471962, 'mAP': 0.3282276601014777, 'plane': 0.6334729949014898, 'ship': 0.4605706851078813, 'ground-track-field': 0.24817865061767505, 'small-vehicle': 0.2080657921311591},
'mmAP': 0.4161059001310853,
'0.95': {'swimming-pool': 0.0, 'helicopter': 0.0, 'large-vehicle': 0.0016604400166044002, 'storage-tank': 0.00219941348973607, 'soccer-ball-field': 0.008264462809917356, 'roundabout': 0.0007639419404125286, 'harbor': 0.0001362954886193267, 'baseball-diamond': 0.0, 'bridge': 0.0, 'basketball-court': 0.0021141649048625794, 'tennis-court': 0.04587710867331721, 'mAP': 0.0046749516409746086, 'plane': 0.007206208425720621, 'ship': 0.0002788622420524261, 'ground-track-field': 0.0, 'small-vehicle': 0.0016233766233766233},
'0.55': {'swimming-pool': 0.5139335447262788, 'helicopter': 0.5626537907742718, 'large-vehicle': 0.8092916935300205, 'storage-tank': 0.8580134302377008, 'soccer-ball-field': 0.6856752856363537, 'roundabout': 0.6073362513669001, 'harbor': 0.5454372214089946, 'baseball-diamond': 0.6804894176071942, 'bridge': 0.3679176998657419, 'basketball-court': 0.6342561331942549, 'tennis-court': 0.9025829004708436, 'mAP': 0.6718581853020654, 'plane': 0.8964344709804708, 'ship': 0.8596490860143631, 'ground-track-field': 0.5042265118194478, 'small-vehicle': 0.649975341898146},
'0.7': {'swimming-pool': 0.24083824023613937, 'helicopter': 0.30823620823620823, 'large-vehicle': 0.7282665307986915, 'storage-tank': 0.7537890472562147, 'soccer-ball-field': 0.5921382895260648, 'roundabout': 0.4727626565401645, 'harbor': 0.3173829055666567, 'baseball-diamond': 0.48751635496750184, 'bridge': 0.2093195784744906, 'basketball-court': 0.6142511390728035, 'tennis-court': 0.9023067636727994, 'mAP': 0.5368373360020182, 'plane': 0.7997907237125352, 'ship': 0.7551689532748252, 'ground-track-field': 0.384207788121679, 'small-vehicle': 0.4865848605734989},
'0.9': {'swimming-pool': 0.0002070822116380203, 'helicopter': 0.007575757575757575, 'large-vehicle': 0.01652892561983471, 'storage-tank': 0.0684800763540921, 'soccer-ball-field': 0.12473572938689217, 'roundabout': 0.015584415584415584, 'harbor': 0.00808080808080808, 'baseball-diamond': 0.007575757575757575, 'bridge': 0.012987012987012986, 'basketball-court': 0.058512396694214874, 'tennis-court': 0.48376995513219534, 'mAP': 0.0700337540867533, 'plane': 0.17039183907475702, 'ship': 0.045454545454545456, 'ground-track-field': 0.023923444976076555, 'small-vehicle': 0.006698564593301435}, '
0.65': {'swimming-pool': 0.39551978397823184, 'helicopter': 0.423591948230682, 'large-vehicle': 0.7563383592094458, 'storage-tank': 0.7771164309807067, 'soccer-ball-field': 0.618458387898894, 'roundabout': 0.5345024644436781, 'harbor': 0.40851117733013564, 'baseball-diamond': 0.5982573737022315, 'bridge': 0.2362489827098382, 'basketball-court': 0.6196894977610174, 'tennis-court': 0.9025829004708436, 'mAP': 0.6012448924023374, 'plane': 0.8896234607912762, 'ship': 0.846382493508526, 'ground-track-field': 0.4356910733340961, 'small-vehicle': 0.576159051685458},
'0.5': {'swimming-pool': 0.5414980691939376, 'helicopter': 0.6128720296184411, 'large-vehicle': 0.816558205343505, 'storage-tank': 0.8622105375879134, 'soccer-ball-field': 0.6945128619476624, 'roundabout': 0.6182074382008003, 'harbor': 0.6425302188899505, 'baseball-diamond': 0.6916726607838906, 'bridge': 0.4118354327940224, 'basketball-court': 0.6342561331942549, 'tennis-court': 0.9025829004708436, 'mAP': 0.6909463698745434, 'plane': 0.8966432300842945, 'ship': 0.8607844372153713, 'ground-track-field': 0.5191338303752648, 'small-vehicle': 0.658897562417998},
'0.85': {'swimming-pool': 0.011363636363636364, 'helicopter': 0.01515151515151515, 'large-vehicle': 0.13488081194580614, 'storage-tank': 0.22431618723760724, 'soccer-ball-field': 0.31235979062066016, 'roundabout': 0.11583577712609971, 'harbor': 0.022727272727272728, 'baseball-diamond': 0.05069169960474308, 'bridge': 0.025974025974025972, 'basketball-court': 0.27073779177422425, 'tennis-court': 0.7631717744106066, 'mAP': 0.1796305358365672, 'plane': 0.4167760164646072, 'ship': 0.14983017832534987, 'ground-track-field': 0.14532424368319674, 'small-vehicle': 0.03531731613915684},
'0.6': {'swimming-pool': 0.4732325349031143, 'helicopter': 0.48775745708534846, 'large-vehicle': 0.783493112947132, 'storage-tank': 0.8446821520715765, 'soccer-ball-field': 0.6333891200462218, 'roundabout': 0.5541033387823082, 'harbor': 0.5014655823023442, 'baseball-diamond': 0.6677393217419294, 'bridge': 0.31667691590880964, 'basketball-court': 0.6342561331942549, 'tennis-court': 0.9025829004708436, 'mAP': 0.6431893744735732, 'plane': 0.8935214859617987, 'ship': 0.8561306896972893, 'ground-track-field': 0.4724313115640485, 'small-vehicle': 0.6263785604265774}}

17epoch
{'0.85': {'harbor': 0.0303030303030303, 'large-vehicle': 0.20457375711250994, 'storage-tank': 0.23851921498099515, 'bridge': 0.022727272727272728, 'roundabout': 0.09935139961136495, 'tennis-court': 0.7740395582450829, 'ship': 0.2091185895365388, 'ground-track-field': 0.15608288770053474, 'baseball-diamond': 0.10363636363636364, 'small-vehicle': 0.039872264271758585, 'plane': 0.42065430032873075, 'mAP': 0.195712452245265, 'basketball-court': 0.29107811767658315, 'soccer-ball-field': 0.31239669421487604, 'helicopter': 0.01515151515151515, 'swimming-pool': 0.018181818181818184},
'0.65': {'harbor': 0.40859694988590056, 'large-vehicle': 0.7569511355396031, 'storage-tank': 0.7763785057190755, 'bridge': 0.2484686541915298, 'roundabout': 0.5353985091313098, 'tennis-court': 0.9019933644990007, 'ship': 0.8473562056286674, 'ground-track-field': 0.4254970884879057, 'baseball-diamond': 0.5777382202207458, 'small-vehicle': 0.582327196689123, 'plane': 0.8911505214153135, 'mAP': 0.6007305438502534, 'basketball-court': 0.6123771114924711, 'soccer-ball-field': 0.6226186879843851, 'helicopter': 0.4302492969336915, 'swimming-pool': 0.3938567099350776},
'0.95': {'harbor': 0.00014149274849663957, 'large-vehicle': 0.0024644030668127055, 'storage-tank': 0.003398470688190314, 'bridge': 0.0, 'roundabout': 0.0007272727272727273, 'tennis-court': 0.05947251953213205, 'ship': 0.00045759609517998775, 'ground-track-field': 0.0, 'baseball-diamond': 0.0, 'small-vehicle': 0.0017482517482517483, 'plane': 0.03636363636363637, 'mAP': 0.008068825615247585, 'basketball-court': 0.002272727272727273, 'soccer-ball-field': 0.013986013986013986, 'helicopter': 0.0, 'swimming-pool': 0.0},
'0.5': {'harbor': 0.6439753225391185, 'large-vehicle': 0.8149934498886875, 'storage-tank': 0.8627897858609628, 'bridge': 0.4059467692235915, 'roundabout': 0.6183959295560748, 'tennis-court': 0.9019933644990007, 'ship': 0.8602303622851744, 'ground-track-field': 0.510090969882596, 'baseball-diamond': 0.698028206179207, 'small-vehicle': 0.6562147813098156, 'plane': 0.8967267532979831, 'mAP': 0.6868746447602, 'basketball-court': 0.6331485241454013, 'soccer-ball-field': 0.697221527429899, 'helicopter': 0.555721641719391, 'swimming-pool': 0.5476422835860963},
'0.6': {'harbor': 0.5105934798145298, 'large-vehicle': 0.7826372317655539, 'storage-tank': 0.8398606801183912, 'bridge': 0.31193141196328267, 'roundabout': 0.5586186366958545, 'tennis-court': 0.9019933644990007, 'ship': 0.8564215706485413, 'ground-track-field': 0.4439330816673156, 'baseball-diamond': 0.6601619816692428, 'small-vehicle': 0.6284180676701098, 'plane': 0.8941540659217737, 'mAP': 0.639951364332094, 'basketball-court': 0.6331485241454013, 'soccer-ball-field': 0.6367307480975793, 'helicopter': 0.48089474649128916, 'swimming-pool': 0.4597728738135453},
'0.9': {'harbor': 0.00946969696969697, 'large-vehicle': 0.025974025974025972, 'storage-tank': 0.0588765766099643, 'bridge': 0.01515151515151515, 'roundabout': 0.022727272727272728, 'tennis-court': 0.5146697472150332, 'ship': 0.09090909090909091, 'ground-track-field': 0.022727272727272728, 'baseball-diamond': 0.0101010101010101, 'small-vehicle': 0.008849557522123894, 'plane': 0.17106694699524405, 'mAP': 0.08511543338451097, 'basketball-court': 0.1306204906204906, 'soccer-ball-field': 0.1875, 'helicopter': 0.006993006993006993, 'swimming-pool': 0.001095290251916758},
'mmAP': 0.42059425588228166,
'0.8': {'harbor': 0.1097146691619162, 'large-vehicle': 0.41312776919614896, 'storage-tank': 0.4968280019124732, 'bridge': 0.05057064147973239, 'roundabout': 0.2287878787878788, 'tennis-court': 0.8898031481893893, 'ship': 0.48327942279990377, 'ground-track-field': 0.2450640424867229, 'baseball-diamond': 0.15257637099742363, 'small-vehicle': 0.22193076015153473, 'plane': 0.6367943544824874, 'mAP': 0.33594577135959797, 'basketball-court': 0.5228214436086706, 'soccer-ball-field': 0.4783506634977224, 'helicopter': 0.05436498984886082, 'swimming-pool': 0.055172413793103454},
'0.75': {'harbor': 0.2084397435958704, 'large-vehicle': 0.6210868060656154, 'storage-tank': 0.6490907747424259, 'bridge': 0.13571678888535899, 'roundabout': 0.3721035514226594, 'tennis-court': 0.8993748958919842, 'ship': 0.7142487266642491, 'ground-track-field': 0.34713400511719844, 'baseball-diamond': 0.23069828722002636, 'small-vehicle': 0.37632321945062513, 'plane': 0.7668494483090519, 'mAP': 0.4426777710824595, 'basketball-court': 0.5599133418684313, 'soccer-ball-field': 0.5306108935886007, 'helicopter': 0.12251547735418702, 'swimming-pool': 0.10606060606060605},
'0.7': {'harbor': 0.31168679724577025, 'large-vehicle': 0.7281041596487654, 'storage-tank': 0.7558610579086219, 'bridge': 0.20165519141410043, 'roundabout': 0.47083232688380966, 'tennis-court': 0.901636948367715, 'ship': 0.7856370034957771, 'ground-track-field': 0.37968549199840973, 'baseball-diamond': 0.48333315703107993, 'small-vehicle': 0.4969184872755785, 'plane': 0.799159798568518, 'mAP': 0.5405236613797736, 'basketball-court': 0.6123771114924711, 'soccer-ball-field': 0.5863464456774315, 'helicopter': 0.33383677204372636, 'swimming-pool': 0.26078417164482737},
'0.55': {'harbor': 0.5467921841439292, 'large-vehicle': 0.8044135648981297, 'storage-tank': 0.8571919986878196, 'bridge': 0.3832299441901049, 'roundabout': 0.606481577645191, 'tennis-court': 0.9019933644990007, 'ship': 0.8593010464446709, 'ground-track-field': 0.49360757458204774, 'baseball-diamond': 0.6844056475659118, 'small-vehicle': 0.649193216538884, 'plane': 0.895819314924704, 'mAP': 0.6703420908134152, 'basketball-court': 0.6331485241454013, 'soccer-ball-field': 0.6806052640518444, 'helicopter': 0.5553654786188741, 'swimming-pool': 0.5035826612647156}}

20epoch
{'0.95': {'mAP': 0.007583964453051848, 'basketball-court': 0.0022172949002217295, 'small-vehicle': 0.001594896331738437, 'soccer-ball-field': 0.0202020202020202, 'helicopter': 0.0, 'large-vehicle': 0.002932551319648094, 'ground-track-field': 0.0, 'baseball-diamond': 0.0, 'ship': 0.0004737933076695292, 'swimming-pool': 0.0, 'storage-tank': 0.004070556309362279, 'roundabout': 0.0007215007215007215, 'harbor': 0.0002608582235554976, 'plane': 0.009404388714733543, 'tennis-court': 0.0718816067653277, 'bridge': 0.0},
'0.7': {'mAP': 0.5428876293708036, 'basketball-court': 0.6126957845842131, 'small-vehicle': 0.49696768305194816, 'soccer-ball-field': 0.5908672362642071, 'helicopter': 0.346471961218505, 'large-vehicle': 0.7269659903307181, 'ground-track-field': 0.3979847433897339, 'baseball-diamond': 0.4722839487852875, 'ship': 0.7942998949105702, 'swimming-pool': 0.24310660697687284, 'storage-tank': 0.7542883260058181, 'roundabout': 0.4692051901181773, 'harbor': 0.3300425209565573, 'plane': 0.800191255198228, 'tennis-court': 0.8989236585217396, 'bridge': 0.20901964024947586},
'0.75': {'mAP': 0.4448118983411511, 'basketball-court': 0.5682037417551529, 'small-vehicle': 0.37657552341445355, 'soccer-ball-field': 0.5304365182461158, 'helicopter': 0.14768270944741535, 'large-vehicle': 0.619916243718708, 'ground-track-field': 0.3312877567267383, 'baseball-diamond': 0.20222779764764498, 'ship': 0.7155837568606931, 'swimming-pool': 0.10667506596619679, 'storage-tank': 0.6482076786738242, 'roundabout': 0.38224660567000357, 'harbor': 0.23449807818010668, 'plane': 0.7683928498356186, 'tennis-court': 0.898094586580467, 'bridge': 0.14214956239412763},
'0.65': {'mAP': 0.6016755207174157, 'basketball-court': 0.6126957845842131, 'small-vehicle': 0.5820792159089286, 'soccer-ball-field': 0.6185860182072304, 'helicopter': 0.43894716351885665, 'large-vehicle': 0.7554866628395395, 'ground-track-field': 0.42564278127635524, 'baseball-diamond': 0.5870287952261386, 'ship': 0.8477775912012528, 'swimming-pool': 0.3930787679744914, 'storage-tank': 0.7767612605814211, 'roundabout': 0.5349342125443448, 'harbor': 0.41738775331119093, 'plane': 0.8927572857176885, 'tennis-court': 0.90069149541957, 'bridge': 0.24127802245001315},
'0.85': {'mAP': 0.19507737081658616, 'basketball-court': 0.31392799998219695, 'small-vehicle': 0.04913604913604913, 'soccer-ball-field': 0.3272953897953898, 'helicopter': 0.013986013986013986, 'large-vehicle': 0.1964178769830598, 'ground-track-field': 0.15352828989192624, 'baseball-diamond': 0.049090909090909095, 'ship': 0.16708367270959934, 'swimming-pool': 0.01515151515151515, 'storage-tank': 0.24178371493315817, 'roundabout': 0.09968152258901157, 'harbor': 0.09090909090909091, 'plane': 0.4194708961736817, 'tennis-court': 0.7716521663717358, 'bridge': 0.017045454545454544},
'0.9': {'mAP': 0.07938951399218218, 'basketball-court': 0.1129380764163373, 'small-vehicle': 0.009134406263592866, 'soccer-ball-field': 0.18414918414918416, 'helicopter': 0.006993006993006993, 'large-vehicle': 0.0303030303030303, 'ground-track-field': 0.018181818181818184, 'baseball-diamond': 0.0101010101010101, 'ship': 0.045454545454545456, 'swimming-pool': 0.0015810276679841897, 'storage-tank': 0.05939733800272628, 'roundabout': 0.0303030303030303, 'harbor': 0.008741258741258742, 'plane': 0.15027973340015208, 'tennis-court': 0.5102982309180428, 'bridge': 0.012987012987012986},
'0.5': {'mAP': 0.6887448008027849, 'basketball-court': 0.6326106376680607, 'small-vehicle': 0.6560670765674932, 'soccer-ball-field': 0.6936861011744623, 'helicopter': 0.5739232643918715, 'large-vehicle': 0.8138035118767092, 'ground-track-field': 0.5087500337744116, 'baseball-diamond': 0.6953210207273014, 'ship': 0.8609741822956081, 'swimming-pool': 0.5547366160202774, 'storage-tank': 0.8621856458759649, 'roundabout': 0.6216088360470955, 'harbor': 0.6460245004405539, 'plane': 0.8980315695768792, 'tennis-court': 0.90069149541957, 'bridge': 0.4127575201855172},
'0.8': {'mAP': 0.3364711120461215, 'basketball-court': 0.5245542574749525, 'small-vehicle': 0.2219205030039983, 'soccer-ball-field': 0.4910086258770469, 'helicopter': 0.0606060606060606, 'large-vehicle': 0.41517590510469315, 'ground-track-field': 0.2441879549022406, 'baseball-diamond': 0.12303650068305115, 'ship': 0.4844049372054363, 'swimming-pool': 0.049371766444937175, 'storage-tank': 0.4912021376936267, 'roundabout': 0.2274528521111353, 'harbor': 0.15134115430558118, 'plane': 0.6396673866925017, 'tennis-court': 0.8858939160514234, 'bridge': 0.03724272253513712},
'0.55': {'mAP': 0.6718958319999611, 'basketball-court': 0.6326106376680607, 'small-vehicle': 0.648979438638037, 'soccer-ball-field': 0.6790570520626545, 'helicopter': 0.5702160548013672, 'large-vehicle': 0.8028054943369699, 'ground-track-field': 0.49941305764384436, 'baseball-diamond': 0.6819428290940807, 'ship': 0.8598818829417697, 'swimming-pool': 0.5102565823150921, 'storage-tank': 0.8561741569527139, 'roundabout': 0.6092485854830295, 'harbor': 0.5494860585652571, 'plane': 0.8977904637066929, 'tennis-court': 0.90069149541957, 'bridge': 0.3798836903702743},
'0.6': {'mAP': 0.642434349911939, 'basketball-court': 0.6326106376680607, 'small-vehicle': 0.6282725977919469, 'soccer-ball-field': 0.6356530918174754, 'helicopter': 0.5136580228761356, 'large-vehicle': 0.7819203748811538, 'ground-track-field': 0.4451550544531957, 'baseball-diamond': 0.6549500939074957, 'ship': 0.8564847588436661, 'swimming-pool': 0.45898885052497534, 'storage-tank': 0.838934225140391, 'roundabout': 0.5660122493554345, 'harbor': 0.5163352422332927, 'plane': 0.8956585262925287, 'tennis-court': 0.90069149541957, 'bridge': 0.31119002747376434},
'mmAP': 0.4210971992451998}
"""

# ------------------------------------------------
VERSION = 'RetinaNet_DOTA_R3Det_KL_2x_20210225'
NET_NAME = 'resnet50_v1d'  # 'MobilenetV2'

# ---------------------------------------- System
ROOT_PATH = os.path.abspath('../../')
print(20*"++--")
print(ROOT_PATH)
GPU_GROUP = "0,1,2,3"
NUM_GPU = len(GPU_GROUP.strip().split(','))
SHOW_TRAIN_INFO_INTE = 20
SMRY_ITER = 200
SAVE_WEIGHTS_INTE = 20673 * 2

SUMMARY_PATH = os.path.join(ROOT_PATH, 'output/summary')
TEST_SAVE_PATH = os.path.join(ROOT_PATH, 'tools/test_result')

pretrain_zoo = PretrainModelZoo()
PRETRAINED_CKPT = pretrain_zoo.pretrain_weight_path(NET_NAME, ROOT_PATH)
TRAINED_CKPT = os.path.join(ROOT_PATH, 'output/trained_weights')
EVALUATE_R_DIR = os.path.join(ROOT_PATH, 'output/evaluate_result_pickle/')

# ------------------------------------------ Train and test
RESTORE_FROM_RPN = False
FIXED_BLOCKS = 1  # allow 0~3
FREEZE_BLOCKS = [True, False, False, False, False]  # for gluoncv backbone
USE_07_METRIC = True
ADD_BOX_IN_TENSORBOARD = True

MUTILPY_BIAS_GRADIENT = 2.0  # if None, will not multipy
GRADIENT_CLIPPING_BY_NORM = 10.0  # if None, will not clip

CLS_WEIGHT = 1.0
REG_WEIGHT = 2.0

BATCH_SIZE = 1
EPSILON = 1e-5
MOMENTUM = 0.9
LR = 1e-3
DECAY_STEP = [SAVE_WEIGHTS_INTE*12, SAVE_WEIGHTS_INTE*16, SAVE_WEIGHTS_INTE*20]
MAX_ITERATION = SAVE_WEIGHTS_INTE*20
WARM_SETP = int(1.0 / 4.0 * SAVE_WEIGHTS_INTE)

# -------------------------------------------- Dataset
DATASET_NAME = 'DOTATrain'  # 'pascal', 'coco'
PIXEL_MEAN = [123.68, 116.779, 103.939]  # R, G, B. In tf, channel is RGB. In openCV, channel is BGR
PIXEL_MEAN_ = [0.485, 0.456, 0.406]
PIXEL_STD = [0.229, 0.224, 0.225]  # R, G, B. In tf, channel is RGB. In openCV, channel is BGR
IMG_SHORT_SIDE_LEN = 800
IMG_MAX_LENGTH = 800
CLASS_NUM = 15

IMG_ROTATE = False
RGB2GRAY = False
VERTICAL_FLIP = False
HORIZONTAL_FLIP = True
IMAGE_PYRAMID = False

# --------------------------------------------- Network
SUBNETS_WEIGHTS_INITIALIZER = tf.random_normal_initializer(mean=0.0, stddev=0.01, seed=None)
SUBNETS_BIAS_INITIALIZER = tf.constant_initializer(value=0.0)
PROBABILITY = 0.01
FINAL_CONV_BIAS_INITIALIZER = tf.constant_initializer(value=-math.log((1.0 - PROBABILITY) / PROBABILITY))
WEIGHT_DECAY = 1e-4
USE_GN = False
NUM_SUBNET_CONV = 4
NUM_REFINE_STAGE = 1
USE_RELU = False
FPN_CHANNEL = 256
FPN_MODE = 'fpn'

# --------------------------------------------- Anchor
LEVEL = ['P3', 'P4', 'P5', 'P6', 'P7']
BASE_ANCHOR_SIZE_LIST = [32, 64, 128, 256, 512]
ANCHOR_STRIDE = [8, 16, 32, 64, 128]
ANCHOR_SCALES = [2 ** 0, 2 ** (1.0 / 3.0), 2 ** (2.0 / 3.0)]
ANCHOR_RATIOS = [1, 1 / 2, 2., 1 / 3., 3., 5., 1 / 5.]
ANCHOR_ANGLES = [-90, -75, -60, -45, -30, -15]
ANCHOR_SCALE_FACTORS = None
USE_CENTER_OFFSET = True
METHOD = 'H'
ANGLE_RANGE = 90

# -------------------------------------------- Head
SHARE_NET = True
USE_P5 = True
IOU_POSITIVE_THRESHOLD = 0.5
IOU_NEGATIVE_THRESHOLD = 0.4
REFINE_IOU_POSITIVE_THRESHOLD = [0.6, 0.7]
REFINE_IOU_NEGATIVE_THRESHOLD = [0.5, 0.6]

NMS = True
NMS_IOU_THRESHOLD = 0.1
MAXIMUM_DETECTIONS = 100
FILTERED_SCORE = 0.05
VIS_SCORE = 0.4

# -------------------------------------------- KLD
KL_TAU = 2.0
KL_FUNC = 0
