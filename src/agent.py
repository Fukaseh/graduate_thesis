import numpy as np

class Agent:
    def __init__(self):
        self.Value = 0
        self.Cost = 0
        self.seller = False
        self.buyer = False
        self.Traded = False
        self.order = 0
        self.numOrder = 0
        self.transaction = []  # 取引価格(売りなら＋に買いなら－に)
        self.stock = [50]
        self.cash = [5000]  # 所持金を0円からスタート

    # Generate a bid offer
    def formBidPrice(self, constrained, maxValue, geoBrown):
        # 制限ありなら1～self.Valueのbid（買い）
        if (constrained == 1) or geoBrown:
            potentialBid = self.Value - (np.random.rand() * (self.Value - 1))
            bid = int(potentialBid)

        # 制限なしなら1～maxValueのbid（買い）
        else:
            potentialBid = np.random.rand() * maxValue + 1
            # 小数点を切り捨てる
            bid = int(potentialBid)
        return bid

    # Generate ask offer
    def formAskPrice(self, constrained, maxValue, maxCost, geoBrown):
        # 制限ありならself.Cost～max.Valueのask(売り)
        if (constrained == 1) or geoBrown:
            potentialAsk = self.Cost + (
                (np.random.rand() * np.absolute(maxValue - self.Cost))
            )
            ask = int(np.ceil(potentialAsk))
        # 制限なしなら0～max.Cost-1のask(売り)
        else:
            potentialAsk = np.random.rand() * (maxCost - 1)
            # 小数点を切り上げる
            ask = int(np.ceil(potentialAsk))
        return ask

    # 買い注文数を計算
    def numberBuyOrders(self, transactionPrices, geoBrown, maxBid):
        if geoBrown:
            # 自身の現金のk倍を買い注文の限界に
            buy_max = maxBid * self.cash[-1]
            number_buy_orders = int(buy_max * np.random.rand() / transactionPrices[-1])
            return number_buy_orders
        else:
            number_buy_orders = 1
            return number_buy_orders

    # 売り注文数を計算
    def nuberSellOrders(self, transactionPrices, geoBrown, maxAsk):
        if geoBrown:
            # 総資産を計算
            all_asset = self.cash[-1] + (self.stock[-1] * transactionPrices[-1])
            # max.Valueの何倍が売り注文の限界の値段か決める
            max_sell = maxAsk * all_asset
            # self.Cost～max.Valueのmax_sell倍のask(売り)として注文数を計算
            number_sell_orders = int(
                np.ceil(max_sell * np.random.rand() / transactionPrices[-1])
            )
            if number_sell_orders > self.stock[-1]:
                number_sell_orders = self.stock[-1]
            return number_sell_orders
        else:
            number_sell_orders = 1
            return number_sell_orders
