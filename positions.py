import pandas as pd

def getAllPositions(cashFlows):
    rows=[]
    for asset in cashFlows[cashFlows.type=='buy'].asset.unique():
        assetFrame=cashFlows[cashFlows.asset==asset]
        buys=assetFrame[assetFrame.type=='buy']
        sells=assetFrame[assetFrame.type=='sell']
        buys['paid']=buys.amount*buys.price+buys.addons
        sells['received']=sells.amount*sells.price-sells.addons
        buyAmountTotal=buys.amount.sum()
        buyPaidTotal=buys.paid.sum()
        sellAmountTotal=sells.amount.sum()
        sellReceivedTotal=sells.received.sum()
        amount=buyAmountTotal-sellAmountTotal
        margin=sellReceivedTotal-buyPaidTotal
        rows.append([asset,amount,margin])
    positions=pd.DataFrame(rows)
    positions.columns=['asset','amount','margin']
    return positions

def getOpenPositions(cashFlows):
    positions=getAllPositions(cashFlows)
    currentPositions=positions[positions.amount>0]
    rows=[]
    for asset in currentPositions.asset:
        assetBuys=cashFlows[(cashFlows.type=='buy') & (cashFlows.asset==asset)].sort_values(by='date',ascending=False)
        currentAmount=positions[positions.asset==asset].iloc[0].amount
        priceTotal=0
        addonTotal=0
        for rowTupple in assetBuys.iterrows():
            row=rowTupple[1]
            if currentAmount<=row.amount:
                priceTotal=priceTotal+row.price*currentAmount
                addonTotal=addonTotal+currentAmount/row.amount*row.addons
                break
            priceTotal=priceTotal+row.price*row.amount
            addonTotal=addonTotal+row.addons
            currentAmount=currentAmount-row.amount
        currentAmount=positions[positions.asset==asset].iloc[0].amount
        category=assetBuys.iloc[0].category
        rows.append([asset,category,currentAmount,priceTotal/currentAmount,addonTotal/currentAmount])
    openPositions=pd.DataFrame(rows)
    openPositions.columns=['asset','category','amount','ppc','addons_per_share']
    openPositions['invested_capital']=(openPositions.ppc+openPositions.addons_per_share)*openPositions.amount
    return openPositions