import pickle
import lib_data
import os
import user_rating
import json

def BuildUserMatrix():
    """
    初始化matrix
    :return: 没有
    """
    maxtrix_row = []
    blank = [""]
    maxtrix_row.append(blank)

    filelist = os.listdir(lib_data.user_info_dir)

    for filename in filelist:
        username = filename.split(".")[0]
        li = [username]
        maxtrix_row.append(li)
        maxtrix_row[0].append(username)

    f = open(lib_data.getBackPath(2) + "/data/UserInfo/matrix/user_matrix.pkl", "wb")
    pickle.dump(maxtrix_row, f, 0)


def CalSimilarity(matrix):
    """
    将用户矩阵填满
    :param matrix: 从pkl中load出来的矩阵
    :return: 修改后的matrix
    """
    for i_r in range(len(matrix)):
        if i_r == 0:
            continue
        for i_c in range(len(matrix[0])):
            if i_c == 0:
                continue
            if matrix[i_r] == matrix[0][i_c]:
                matrix[i_r].append(0)

            try:
                result = user_rating.CalUserSimilarity_Local(matrix[0][i_c], matrix[i_r][0])
                matrix[i_r].append(result)
                print(matrix[0][i_c] + " vs " + matrix[i_r][0] + " : " + str(result))
            except Exception as e:
                print(e)


    return matrix





mf = open(lib_data.getBackPath(2) + "/data/UserInfo/matrix/user_matrix.pkl", "rb+")
m = pickle.load(mf)
nm = CalSimilarity(m)

pickle.dump(nm, mf, 0)




