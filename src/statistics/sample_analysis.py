import os
import numpy
import lib_data
import json

'''   以下程序实现了计算所有样本用户的六维数据的方差，并输出，其结果为

{'Acc': 328416.95536684606, 'Precision': 69100.17995745681, 'Flow': 176140.7529856739, 'Jump': 977312.5566506414, 
'Speed': 274150.8838509888, 'Stamina': 209264.9192446591}

user_list = os.listdir(lib_data.user_info_dir)
user_acc = []
user_precision = []
user_flow = []
user_jump = []
user_speed = []
user_stamina = []

for user in user_list:
    try:
        f = open(lib_data.user_info_dir + user)
        user_info = json.load(f)
        user_acc.append(user_info["user_stats"]["Acc_total"])
        user_precision.append(user_info["user_stats"]["Precision_total"])
        user_flow.append(user_info["user_stats"]["Flow_total"])
        user_jump.append(user_info["user_stats"]["Jump_total"])
        user_speed.append(user_info["user_stats"]["Speed_total"])
        user_stamina.append(user_info["user_stats"]["Stamina_total"])
        f.close()
    except Exception as e:
        print(e)
        print(user_info["user_stats"]["username"])

user_var = {"Acc":numpy.var(user_acc), "Precision":numpy.var(user_precision), "Flow":numpy.var(user_flow),
            "Jump":numpy.var(user_jump), "Speed":numpy.var(user_speed), "Stamina":numpy.var(user_stamina)}

print(user_var)'''

''' 以下数据计算了方差占比 结果为

{'Acc': 0.1614329411047822, 'Precision': 0.033966106496973174, 'Flow': 0.08658176546069647,
 'Jump': 0.4803967572944444, 'Speed': 0.13475852194386564, 'Stamina': 0.102863907699238133}

user_var = {'Acc': 328416.95536684606, 'Precision': 69100.17995745681, 'Flow': 176140.7529856739,
            'Jump': 977312.5566506414, 'Speed': 274150.8838509888, 'Stamina': 209264.9192446591}

total = 0

user_percentage = user_var

for key in user_var:
    total += user_var[key]

print(total)

for key in user_percentage:
    t = user_percentage[key]
    user_percentage[key] = t/total

print(user_percentage)'''

''' 以下计算了方差总占比及其倒数，再计算所得结果的占比，其结果为

{'Acc': 6.19452258725141, 'Precision': 29.44111360214669, 'Flow': 11.549776037472313, '
Jump': 2.0816127186867766, 'Speed': 7.420680974940903, 'Stamina': 9.721582840541908}

66.40928876104

{'Acc': 0.09327795407568827, 'Precision': 0.44332824746978405, 'Flow': 0.17391808063224073, 
'Jump': 0.03134520422552674, 'Speed': 0.11174161195495827, 'Stamina': 0.14638890164180193｝

user_percenatge = {'Acc': 0.1614329411047822, 'Precision': 0.033966106496973174, 'Flow': 0.08658176546069647,
                   'Jump': 0.4803967572944444, 'Speed': 0.13475852194386564, 'Stamina': 0.102863907699238133}

user_weight = user_percenatge

for key in user_percenatge:
    user_weight[key] = 1 / user_percenatge[key]

print(user_weight)

weight_percentage = user_weight

total_weight = 0

for  key in user_weight:
    total_weight += user_weight[key]

print(total_weight)

for key in weight_percentage:
    weight_percentage[key] = weight_percentage[key]/total_weight

print(weight_percentage)'''

coefficient = {'Acc': 0.09327795407568827, 'Precision': 0.44332824746978405, 'Flow': 0.17391808063224073,
               'Jump': 0.03134520422552674, 'Speed': 0.11174161195495827, 'Stamina': 0.14638890164180193}