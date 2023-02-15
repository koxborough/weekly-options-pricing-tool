from yahoo_fin import options as op
from yahoo_fin import stock_info as si
from tqdm import tqdm
import datetime

def save_contract():
    type = ("S" if tickers[i][3] == "short" else "L") + ("C" if contract_type == "calls" else "P")
    contracts_list.append([ticker, type, contracts.loc[j]["Bid"], contracts.loc[j]["Ask"], contracts.loc[j]["Strike"], price, get_price_change(False)])

def save_bid_ask_strike():
    return contracts.loc[j]["Bid"], contracts.loc[j]["Ask"], contracts.loc[j]["Strike"]

def get_price_change(above_threshold):
    return ((strike - price) / price) * 100 if (above_threshold) else ((contracts.loc[j]["Strike"] - price) / price) * 100

# Read in list of tickers (symbol, desired change/price, call/put)
tickers = []
with open("ticker_information.txt") as f:
    for line in f:
        temp1, temp2, temp3 = [str(s) for s in line.split()]
        tickers.append([temp1, float(temp2), "calls" if temp3[1] == "C" else "puts", "long" if temp3[0] == "L" else "short"])

# Get Friday to access weekly options
today = datetime.date.today()
friday = today + datetime.timedelta( (4-today.weekday()) % 7 )

if (today == friday and datetime.datetime.now().hour >= 4):
    friday = today + datetime.timedelta(days=7)
    
formatted_friday = f"{str(friday.month).zfill(2)}/{str(friday.day).zfill(2)}/{friday.year}"

# Iterate over the list of desired tickers
contracts_list = []
for i in tqdm(range(len(tickers)), position=0, leave=False):
    ticker = tickers[i][0]
    max_change = tickers[i][1]
    contract_type = tickers[i][2]
    price = si.get_live_price(ticker)
    desired_price = (max_change * 2) if (max_change >= 1.0) else round(price * (1 + max_change if contract_type == "calls" else 1 - max_change), 2)

    # Get entire list of contracts for specific ticker
    chain = op.get_options_chain(ticker, formatted_friday)
    contracts = chain[contract_type]

    bid = ask = strike = 0.
    next = False if ((tickers[i][3] == "long" and contract_type == "calls") or (tickers[i][3] == "short" and contract_type == "puts")) else True

    # Iterate over each option until the right one is found
    for j in range(len(contracts)):
        
        # Found the call when a strike price is entered
        if (contract_type == "calls" and max_change >= 1.0 and max_change == contracts.loc[j]["Strike"]):
            save_contract()
            break

        # Found the put when a strike price is entered
        elif (contract_type == "puts" and max_change >= 1.0 and max_change == contracts.loc[j]["Strike"]):
            save_contract()
            break

        # Continue looking at calls while we are under threshold
        elif (contract_type == "calls" and (contracts.loc[j]["Strike"] <= desired_price or next)):
            if (contracts.loc[j]["Strike"] > desired_price):
                next = False
            bid, ask, strike = save_bid_ask_strike()

        # Continue looking at puts while we are under threshold
        elif (contract_type == "puts" and (contracts.loc[j]["Strike"] <= desired_price or next)):
            if (contracts.loc[j]["Strike"] > desired_price):
                next = False
            bid, ask, strike = save_bid_ask_strike()

        # Above the threshold, return with contract data
        else:
            type = ("S" if tickers[i][3] == "short" else "L") + ("C" if contract_type == "calls" else "P")
            contracts_list.append([ticker, type, bid, ask, strike, price, get_price_change(True)])
            break
    pass

# Sort contracts by ticker then strike price
contracts_list.sort(key = lambda contract: (contract[0], contract[4]))

# Print list of contracts
print("/-------------------------------------------------------------\\")
print("| Symbol | Type |  Bid  |  Ask  |  Strike |  Price  |  Diff.  |")
print("|-------------------------------------------------------------|")
for contract in contracts_list:
    print(f"|  {contract[0].ljust(4)}  |  {contract[1]}  | {float(contract[2]):5.2f} | {float(contract[3]):5.2f} | {float(contract[4]):7.2f} | {float(contract[5]): 7.2f} | {float(contract[6]):6.2f}% |")
print("\\-------------------------------------------------------------/")