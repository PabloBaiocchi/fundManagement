import pandas as pd
import numpy as np

def getAllPositions(cashFlows):
  buySells=cashFlows[cashFlows.type.isin(['buy','sell'])].copy()
  buySells['amount_diff']=buySells.apply(lambda x: x.amount if x.type=='buy' else -x.amount,axis=1)
  buySells['total']=buySells.apply(lambda x: x.amount*x.price+x.addons if x.type=='buy' else x.amount*x.price-x.addons,axis=1)
  rows=[]
  for asset in buySells.asset.unique():
    assetFrame=buySells[buySells.asset==asset]
    amount=assetFrame.amount_diff.sum()
    buys=assetFrame[assetFrame.type=='buy']
    sells=assetFrame[assetFrame.type=='sell']
    avgBuy=buys.total.sum()/buys.amount.sum()
    avgSell=sells.total.sum()/sells.amount.sum()
    profit=sells.total.sum()-buys.total.sum()
    rows.append([asset,amount,avgBuy,avgSell,profit])
  frame=pd.DataFrame(rows)
  frame.columns=['asset','amount','avg_buy','avg_sell','profit']
  return frame

def getCurrentPosition(asset,cashFlows):
  assetFlows=cashFlows[cashFlows.asset==asset].copy()
  assetFlows.index=np.arange(len(assetFlows))
  assetFlows['amount_diff']=assetFlows.apply(lambda x: x.amount if x.type=='buy' else -x.amount,axis=1)
  assetFlows['amount_held']=assetFlows.amount_diff.cumsum()
  assetFlows['avg_price']=assetFlows.apply(lambda x: x.price+x.addons/x.amount if x.type=='buy' else x.price-x.addons/x.amount,axis=1)
  assetFlows['total']=assetFlows.avg_price*assetFlows.amount
  zeroIndeces=assetFlows[assetFlows.amount_held==0].index
  if len(zeroIndeces)>0:
    return assetFlows.iloc[zeroIndeces[-1]+1:]
  return assetFlows

def getPpc(currentPosition):
  ppc=0
  for tupple in currentPosition.iterrows():
    index=tupple[0]
    row=tupple[1]
    if row.type=='sell':
      continue
    elif index==0:
      ppc=row.avg_price
    else:
      formerAmountHeld=row.amount_held-row.amount
      ppc=(ppc*formerAmountHeld+row.amount*row.avg_price)/row.amount_held
  return ppc

def getAvgBuy(currentPosition):
  buys=currentPosition[currentPosition.type=='buy']
  return buys.total.sum()/buys.amount.sum()

def getAvgSell(currentPosition):
  sells=currentPosition[currentPosition.type=='sell']
  if len(sells)==0:
      return 0
  return sells.total.sum()/sells.amount.sum()

def getAmountHeld(currentPosition):
  return currentPosition.iloc[-1].amount_held

def marginOnSold(currentPosition):
  amountSold=currentPosition[currentPosition.type=='sell'].amount.sum()
  return (getAvgSell(currentPosition)-getAvgBuy(currentPosition))*amountSold

def getCategory(currentPosition):
  return currentPosition.iloc[0].category

def getOpenPositions(cashFlows):
  assets=cashFlows[cashFlows.type=='buy'].asset.unique()
  rows=[]
  for asset in assets:
    currentPosition=getCurrentPosition(asset,cashFlows)
    if len(currentPosition)<1:
      continue
    ppc=getPpc(currentPosition)
    avgBuy=getAvgBuy(currentPosition)
    avgSell=getAvgSell(currentPosition)
    amountHeld=getAmountHeld(currentPosition)
    currentMargin=marginOnSold(currentPosition)
    category=getCategory(currentPosition)
    rows.append([asset,category,amountHeld,ppc,avgBuy,avgSell,currentMargin])
  frame=pd.DataFrame(rows)
  frame.columns=['asset','category','amount','ppc','avg_buy','avg_sell','current_margin']
  frame['invested_capital']=frame.ppc*frame.amount
  return frame
    