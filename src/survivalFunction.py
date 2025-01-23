import numpy as np
import matplotlib.pyplot as plt
import os


# (資産の)リストから変動が0の要素を除外するための関数
def removeDuplicates(agents, trader_i):
    assets = agents[trader_i].cash
    deduplicated_assets = [assets[0]]
    # 前の期間の資産から変化しているものだけ保存
    for period_i in range(len(assets) - 1):
        if assets[period_i] != assets[period_i + 1]:
            deduplicated_assets.append(assets[period_i + 1])
    return deduplicated_assets


# 前の要素からの変動の割合を求める関数
def calculateChangeRatio(base_list):
    change_ratios = []
    for i in range(len(base_list) - 1):
        change_ratio = base_list[i + 1] - base_list[i]/ base_list[i]
        change_ratios.append(change_ratio)
    return change_ratios


# 標準化された正のデータを生存関数に依存するデータにする関数
def changeSurvival(standardized_list):
    length = len(standardized_list)
    standardized_list.sort()
    survival = []
    # グラフの点の刻み幅を設定
    x = [0.0001]
    count = 1
    while count != 0:
        count = sum(1 for data in standardized_list if data >= x[-1])
        x.append(x[-1] + x[0])
        survival.append(count/length)
    x = x[:-1]
    return x, survival


def makeSurvival(base_list):
    base_list.sort()
    base_mean = np.mean(base_list)
    base_variance = np.std(base_list)
    standardized_list = []
    for data in range(len(base_list)):
        standardization = (base_list[data] - base_mean) / base_variance
        standardized_list.append(abs(standardization))
    # 標準化されたデータを生存関数に
    x, survival = changeSurvival(standardized_list)
    return x, survival


# 作成された生存関数と同じ平均と標準偏差と大きさのガウス分布の生存関数のデータを作成
def gaussianSurvival(base_list):
    normal_mean = 0
    normal_variance = 1
    # 平均0,分散1のガウス分布に従う乱数を絶対値をとったものを作成
    gaussian = abs(
        np.random.normal(loc=normal_mean, scale=normal_variance, size=len(base_list))
    )
    gaussian_list = gaussian.tolist()
    # ガウス分布の生存関数を作成するためのデータを求める
    gaussian_x, gaussian_survival = changeSurvival(gaussian_list)
    return gaussian_x, gaussian_survival


# 生存関数をグラフにする関数
def plotSurvival(x, survival, gaussian_x, gaussian_survival, plot_name, file_name, number):
    plt.clf()

    plt.scatter(x, survival, color="blue", label=f"{plot_name}", s=10)
    plt.scatter(gaussian_x, gaussian_survival, color="red", label="N(0,1)", s=10)
    plt.ylim(1/number, 2)
    plt.xscale("log")
    plt.yscale("log")
    plt.legend()

    output_png_path = os.path.join("output_png", f"{plot_name}_{file_name}sur.png")
    plt.savefig(output_png_path,)
    output_pdf_path = os.path.join("output_pdf", f"{plot_name}_{file_name}sur.pdf")
    plt.savefig(output_pdf_path, format="pdf")
    


# 作成されたデータをdatファイルに
def datSurvival(x, survival, gaussian_x, gaussian_survival, plot_name, file_name):
    # xとgaussian_xのうち、長い方に合わせるために短いデータにNaNを追加
    max_len = max(len(x), len(gaussian_x))
    arr_x = np.array(x)
    arr_survival = np.array(survival)
    arr_gaussian_x = np.array(gaussian_x)
    arr_gaussian_survival = np.array(gaussian_survival)
    float_x = arr_x.astype(float)
    float_survival = arr_survival.astype(float)
    float_gaussian_x = arr_gaussian_x.astype(float)
    float_gaussian_survival = arr_gaussian_survival.astype(float)

    # max_lenとの差だけNaNを追加していく
    padded_x = np.pad(float_x, (0, max_len - len(float_x)), constant_values=np.nan)
    padded_survival = np.pad(
        float_survival, (0, max_len - len(float_survival)), constant_values=np.nan
    )
    padded_gaussian_x = np.pad(
        float_gaussian_x, (0, max_len - len(float_gaussian_x)), constant_values=np.nan
    )
    padded_gaussian_survival = np.pad(
        float_gaussian_survival,
        (0, max_len - len(float_gaussian_survival)),
        constant_values=np.nan,
    )

    # ファイルにしていく
    # 出力ファイルのパスを指定
    output_file_path = os.path.join("output_dat", f"{plot_name}_{file_name}.dat")
    with open(output_file_path, "w") as file:
        for data_i in range(max_len):
            file.write(
                f"{padded_x[data_i]} {padded_survival[data_i]} {padded_gaussian_x[data_i]} {padded_gaussian_survival[data_i]}\n"
            )


# Binder cumulantを求める関数
def Binder_cumulant(base_list, file_name):
    list_mean = np.mean(base_list)
    v_2 = 0
    v_4 = 0
    for i in range(len(base_list)):
        v_2 += (base_list[i]-list_mean)**2 / len(base_list)
        v_4 += (base_list[i]-list_mean)**4 / len(base_list)
    BinderCumulant = 1.0 - v_4/(3*(v_2**2))

    # Binder_cumulant.datに書き込む
    with open("Binder_cumulant.dat", "a") as f:
        f.write(f"{file_name}, {BinderCumulant}\n")
