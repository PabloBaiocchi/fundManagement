def getBreakEven(positions,commissions,broker,asset,multiday=True):
  x=positions[positions.asset==asset].iloc[0]
  pricePaid=x.ppc+x.addons_per_share
  comm=getCommission(commissions,broker,x.category,multiday)
  return pricePaid/(1-comm)

def getCommission(commissionsDf,broker,category,multiday=True):
  filtered=commissionsDf[commissionsDf.entity.isin(['market',broker]) & (commissionsDf.category==category)]
  if multiday:
    return filtered.multiday.sum()
  return filtered.intraday.sum()
