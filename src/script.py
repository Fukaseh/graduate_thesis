import numpy as np
import yaml
import sys
import os

import matplotlib

matplotlib.use("Agg")  # 画面に描画せずにファイルとして直接画像を生成できる
import survivalFunction as sur
from agent import Agent
from openPrice import trade

# set seed
np.random.seed(0)
# トレーダーの人数
numberTraders = 2000

# 幾何ブラウン運動に従うようにするならTrue、標準ブラウン運動ならFalseに
geoBrown = True

# 標準ブラウン運動で毎期間、価格設定を変更するならChangeをTrueに、しないならFalseに
change_price = True

# 制限あり(constrained = 1)で実行
# 制限なしにしたい場合は0にすること
constrained = 1

# 償却価値maxValueとコストmaxCost
if geoBrown:
    maxValue = 500

    maxCost = 500
else:
    maxValue = 100
    maxCost = 100

# 資産の変動を調べたいトレーダーの番号
checkTrader = 1

# 取引価格の初期値を設定
transactionPrices = [175]

# 取引を行う回数を設定
periods = 5000

inputfile = sys.argv[1]
# inputfileの拡張子以外をfile_nameに保存
file_name, _ = os.path.splitext(os.path.basename(inputfile))
# 幾何ブラウン運動の場合、資産の何倍の注文を出すかを決める
# 売り注文の場合、総資産の何倍を仮の注文の上限にするか決める
with open(inputfile) as f:
    params = yaml.safe_load(f)

maxAsk = float(params["maxAsk"])
# 買い注文の場合、キャッシュの何倍を仮の注文の上限にするか決める
maxBid = float(params["maxBid"])

# Create vector holding all agents
agents = []
for i in range(numberTraders):
    agents.append(Agent())


for i in range(periods):
    loop = True
    if loop:
        # Valueを0～maxValueに
        valueVec = maxValue * np.random.rand(numberTraders)
        for i in range(numberTraders):
            agents[i].Value = valueVec[i]
        # Costを0～maxCostに
        costVec = maxCost * np.random.rand(numberTraders)
        for i in range(numberTraders):
            agents[i].Cost = costVec[i]
        # 価格戦略を変更しないならroopをFalseにして固定する
        if (change_price == False) and (geoBrown == False):
            loop = False

    # agentsをリセット
    for i in range(numberTraders):
        agents[i].Traded = False
        agents[i].seller = False
        agents[i].buyer = False
        agents[i].order = 0
        agents[i].numOrder = 0
    # 取引価格の記録をリセット
    transactionprice = 0

    agents, transactionprice = trade(
        agents,
        numberTraders,
        constrained,
        maxValue,
        maxCost,
        geoBrown,
        transactionPrices,
        maxBid,
        maxAsk,
    )
    # 取引価格を記録
    transactionPrices.append(transactionprice)


# トレーダーの最終的な保有資産を保存
cash_list = []
for i in range(len(agents)):
    cash_list.append(agents[i].cash[-1])

# 資産変動の生存関数を作成
# (資産の)リストから変動が0の要素を除外する
deduplicated_assets = sur.removeDuplicates(agents, checkTrader)
# 生存関数のためのデータを作成
asset_change_ratio = sur.calculateChangeRatio(deduplicated_assets)
asset_x, asset_survival = sur.makeSurvival(asset_change_ratio)
# datファイルに
plot_name1 = "asset_growth"
gaussian_x1, gaussian_survival1 = sur.gaussianSurvival(asset_change_ratio)
sur.datSurvival(
    asset_x, asset_survival, gaussian_x1, gaussian_survival1, plot_name1, file_name
)

# 価格変動の生存関数を作成
price_change_ratio = sur.calculateChangeRatio(transactionPrices)
price_x, price_survival = sur.makeSurvival(price_change_ratio)
plot_name2 = "price"
gaussian_x2, gaussian_survival2 = sur.gaussianSurvival(price_change_ratio)

# 資産分布の生存関数を作成
asset_distribution_x, asset_distribution_survival = sur.makeSurvival(cash_list)
plot_name3 = "asset"
gaussian_x3, gaussian_survival3 = sur.gaussianSurvival(cash_list)

"""
sur.plotSurvival(
    asset_x, asset_survival, gaussian_x1, gaussian_survival1, plot_name1, file_name, numberTraders
)

sur.plotSurvival(
    price_x, price_survival, gaussian_x2, gaussian_survival2, plot_name2, file_name, periods


sur.plotSurvival(
    asset_distribution_x,
    asset_distribution_survival,
    gaussian_x3,
    gaussian_survival3,
    plot_name3,
    file_name,
    periods
)
"""

sur.datSurvival(
    price_x, price_survival, gaussian_x2, gaussian_survival2, plot_name2, file_name
)


sur.datSurvival(
    asset_distribution_x,
    asset_distribution_survival,
    gaussian_x3,
    gaussian_survival3,
    plot_name3,
    file_name,
)

# Binder cumulantを保存
sur.Binder_cumulant(cash_list, file_name)
sur.Binder_cumulant(asset_change_ratio, file_name)


