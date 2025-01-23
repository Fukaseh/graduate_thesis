import numpy as np
import random


# 取引価格を決める関数
def trade(
    agents,
    numberTraders,
    constrained,
    maxValue,
    maxCost,
    geoBrown,
    transactionPrices,
    maxBid,
    maxAsk,
):
    # 取引数が1以上になるまでループ
    while True:
        for trader_i in range(numberTraders):
            # Randomly choose between a buyer and a seller (belor 0.5 we select a
            # buyer, otherwise we select a seller).1/2で売りてか買い手かを決める
            traderDeterminer = np.random.rand()

            # Process as buyer
            if traderDeterminer < 0.5:
                # 自身がbuyerであることを記録
                agents[trader_i].buyer = True
                # 指値注文の価格を決定
                agents[trader_i].order = agents[trader_i].formBidPrice(
                    constrained, maxValue, geoBrown
                )
                # 注文数を決定
                agents[trader_i].numOrder = agents[trader_i].numberBuyOrders(
                    transactionPrices, geoBrown, maxBid
                )
                # 購入額が現金額を超える場合は買えるだけ注文
                cost = agents[trader_i].order * agents[trader_i].numOrder
                if cost > agents[trader_i].cash[-1]:
                    agents[trader_i].numOrder = int(
                        agents[trader_i].cash[-1] / agents[trader_i].order
                    )
            else:
                # 自身がsellerであることを記録
                agents[trader_i].seller = True
                # 指値注文の価格を決定
                agents[trader_i].order = agents[trader_i].formAskPrice(
                    constrained, maxValue, maxCost, geoBrown
                )
                # 注文数を決定
                agents[trader_i].numOrder = agents[trader_i].nuberSellOrders(
                    transactionPrices, geoBrown, maxAsk
                )
                # 売る株数が保有数を超える場合は売れるだけ売却
                if agents[trader_i].numOrder > agents[trader_i].stock[-1]:
                    agents[trader_i].numOrder = agents[trader_i].stock[-1]

        sellOrder = []
        buyOrder = []
        # トレーダーの注文を売り買いに分けて保存
        for trader_i in range(numberTraders):
            # 注文価格を注文数だけ追加
            if agents[trader_i].seller == True:
                sellOrder.extend([agents[trader_i].order] * agents[trader_i].numOrder)
            elif agents[trader_i].buyer == True:
                buyOrder.extend([agents[trader_i].order] * agents[trader_i].numOrder)
            # debug
            else:
                print("seller,buyerの選び方に異常あり")
                exit()
        # ソート(需給曲線の作成)
        sellOrder.sort()
        buyOrder.sort(reverse=True)

        # 約定する数を決める
        maxContracts = min(len(sellOrder), len(buyOrder))
        numberContracts = 0
        while sellOrder[numberContracts] <= buyOrder[numberContracts]:
            numberContracts += 1
            if numberContracts == maxContracts:
                break
        # 実際の人数なのでsellOrder[]に入れるときは-1が必要(多分)
        # 約定する人数が0人なら初めからやり直し
        if numberContracts != 0:
            break

    # 取引価格の決定
    # 取引価格は均衡価格(需給曲線の重なっている部分の中央値)
    if numberContracts == maxContracts:
        equilibrium_price = (
            buyOrder[numberContracts - 1] + sellOrder[numberContracts - 1]
        ) / 2
    else:
        equilibrium_price = (
            min(sellOrder[numberContracts], buyOrder[numberContracts - 1])
            + max(sellOrder[numberContracts - 1], buyOrder[numberContracts])
        ) / 2
    # 取引価格が小数なので1/2の確率で切り上げて1/2の確率で切り捨てる
    if np.random.rand() < 0.5:
        equilibrium_price = int(np.ceil(equilibrium_price))
    else:
        equilibrium_price = int(equilibrium_price)

    # 取引した人を決めていく
    # 約定できた注文のリストを作成
    executedSellOrder = sellOrder[:numberContracts]
    exectedBuyOrder = buyOrder[:numberContracts]
    # 約定できる人の中で最も低い売り注文と、最も高い買い注文の価格を保存
    low_sell_order = executedSellOrder[-1]
    high_buy_order = exectedBuyOrder[-1]
    # 約定できる人の中でその値段で注文を出した人の人数を保存
    count_low_sell = executedSellOrder.count(low_sell_order)
    count_high_buy = exectedBuyOrder.count(high_buy_order)
    # 取引する人が偏らないようにagentsをランダムに並び替える
    random.shuffle(agents)
    # 均衡価格未満の人の.TradedをTrueに、.transactionを取引価格にする
    # ただし、取引価格ちょうどの注文を出した人はcountが0にならない限り取引ができる
    # 売り注文をした人は自身の株を-1、買い注文をした人は自身の株を+1する
    for trader_i in range(numberTraders):
        # seller
        if agents[trader_i].seller:
            # 均衡価格未満の注文はすべて約定
            if agents[trader_i].order < equilibrium_price:
                agents[trader_i].Traded = True
                agents[trader_i].transaction.append(-1 * equilibrium_price)
                agents[trader_i].numOrder *= -1

            # 均衡価格と等しい注文はagentsの早いもの順に約定していく
            elif agents[trader_i] == equilibrium_price:
                # 注文数がcount_low_sellより少ないならすべて取引可能
                if agents[trader_i].numOrder <= count_low_sell:
                    agents[trader_i].Traded = True
                    agents[trader_i].transaction.append(-1 * equilibrium_price)
                    agents[trader_i].numOrder *= -1
                    # 取引できる人数のカウント(count_low_sell)を減らす
                    count_low_sell -= agents[trader_i].numOrder

                # 注文数全部は取引が行えない人の処理
                elif (agents[trader_i].numOrder > count_low_sell) and (
                    count_low_sell != 0
                ):
                    agents[trader_i].Traded = True
                    agents[trader_i].transaction.append(-1 * equilibrium_price)
                    agents[trader_i].numOrder = -1 * count_low_sell
                    count_low_sell = 0
                else:
                    agents[trader_i].numOrder = 0
                    agents[trader_i].transaction.append(0)

            else:
                agents[trader_i].numOrder = 0
                agents[trader_i].transaction.append(0)

        # buyer
        else:
            # 均衡価格より高い価格の注文はすべて約定
            if agents[trader_i].order > equilibrium_price:
                agents[trader_i].Traded = True
                agents[trader_i].transaction.append(-1 * equilibrium_price)

            # 均衡価格と等しい注文はagentsの早いもの順に約定していく
            elif (agents[trader_i] == equilibrium_price) and (count_high_buy > 0):
                # 注文数がcount_high_buyより少ないならすべて取引可能
                if agents[trader_i].numOrder <= count_high_buy:
                    agents[trader_i].Traded = True
                    agents[trader_i].transaction.append(-1 * equilibrium_price)
                    # 取引できる人数のカウント(count_high_buy)を減らす
                    count_high_buy -= agents[trader_i].numOrder
                # 均衡価格だが注文数全部は取引が行えない人の処理
                elif (agents[trader_i].numOrder > count_high_buy) and (
                    count_high_buy != 0
                ):
                    agents[trader_i].Traded = True
                    agents[trader_i].numOrder = count_high_buy
                    agents[trader_i].transaction.append(-1 * equilibrium_price)
                    count_high_buy = 0
                # 均衡価格だが取引が行えない人の処理
                else:
                    agents[trader_i].numOrder = 0
                    agents[trader_i].transaction.append(0)

            else:
                agents[trader_i].numOrder = 0
                agents[trader_i].transaction.append(0)

    # 資産に変更を加える。
    for trader_i in range(numberTraders):
        # buyerなら現金を減らし、株数を増やす
        # sellerなら現金を増やし、株数を減らす。
        # 取引を行っていなくても資産は更新する
        agents[trader_i].cash.append(
            agents[trader_i].cash[-1]
            + (agents[trader_i].transaction[-1] * agents[trader_i].numOrder)
        )
        agents[trader_i].stock.append(
            agents[trader_i].stock[-1] + agents[trader_i].numOrder
        )

    return agents, equilibrium_price
