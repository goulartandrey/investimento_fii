class FundoImobiliario:
    def __init__(self, code, segment, price, dy, pvp, liquidity):
        self.code = code
        self.segment = segment
        self.price = price
        self.dy = dy
        self.pvp = pvp
        self.liquidity = liquidity

class Strategy:
    def __init__(self, segment='', max_price=0, min_dy=0, max_pvp=0, min_liquidity=0):
        self.segment = segment
        self.max_price = max_price
        self.min_dy = min_dy
        self.max_pvp = max_pvp
        self.min_liquidity = min_liquidity

    def aply_strategy(self, fundo:FundoImobiliario):
        if self.segment != '':
            if fundo.segment != self.segment:
                return False

        if fundo.price > self.max_price \
        or fundo.dy < self.min_dy \
        or fundo.pvp > self.max_pvp \
        or fundo.liquidity < self.min_liquidity:
            return False
        else:
            return True