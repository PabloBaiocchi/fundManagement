class BinaryPosition:

  def __init__(self,put,call,commission):
    put={
        'invested_capital':put.invested_capital,
        'current_margin':put.current_margin,
        'ppc':put.ppc,
        'amount':put.amount
    }
    call={
        'invested_capital':call.invested_capital,
        'current_margin':call.current_margin,
        'ppc':call.ppc,
        'amount':call.amount
    }
    self.assets={
        'put':put,
        'call':call
    }
    self.commission=commission

  def putTargetPrice(self,callPrice):
    put=self.assets['put']
    call=self.assets['call']
    return (put['invested_capital']+call['invested_capital']-call['current_margin']-put['current_margin']-call['amount']*callPrice*(1-self.commission))/put['amount']/(1-self.commission)

  def callTargetPrice(self,putPrice):
    put=self.assets['put']
    call=self.assets['call']
    return (put['invested_capital']+call['invested_capital']-call['current_margin']-put['current_margin']-put['amount']*putPrice*(1-self.commission))/call['amount']/(1-self.commission)

  def buy(self,type,amount,price):
    pricePaid=price*(1+self.commission)
    asset=self.assets[type]
    asset['ppc']=(pricePaid*amount+asset['invested_capital'])/(asset['amount']+amount)
    asset['amount']=asset['amount']+amount
    asset['invested_capital']=asset['ppc']*asset['amount']

  def sell(self,type,amount,price):
    priceReceived=price*(1-self.commission)
    asset=self.assets[type]
    asset['invested_capital']=asset['invested_capital']-asset['ppc']*amount
    asset['amount']=asset['amount']-amount
    asset['current_margin']=asset['current_margin']+(priceReceived-asset['ppc'])*amount

def ratio(self):
    totalCapital=self.assets['put']['invested_capital']+self.assets['call']['invested_capital']
    callPercent=self.assets['call']['invested_capital']/totalCapital
    return {
        'call': callPercent,
        'put': 1-callPercent
    }