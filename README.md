# Weekly Options Pricing Tool

Options in the stock market are contracts that stock traders or investors can use to buy or sell a lot of 100 shares. Each has an expiration date, up to what date a contract is valid for; a strike price, what price the lot of shares will be bought or sold; and a premium, the upfront price the buyer must pay for the contract.

By purchasing options, the trader can either hedge their positions or take on risk to bet on a stock's movement for a large profit. Interestingly, while traders can buy options, another tool is to sell options, in which the seller collects the premium and concedes the right to buy or sell a lot of 100 shares. To learn more, the links below have much more detailed and informative articles than this introduction:
- [What are Options?](https://www.investopedia.com/terms/o/option.asp)
- [The Ins and Outs of Selling Options](https://www.investopedia.com/articles/optioninvestor/09/selling-options.asp)
- [Fidelity's Options Online Educational Course](https://www.fidelity.com/options-trading/education-and-ideas)
- [What are the Benefits & Risks?](https://www.merrilledge.com/investment-products/options/benefits-risks-of-options)

## How to Use
The Weekly Options Pricing Tool uses Python, which can be downloaded [here](https://wiki.python.org/moin/BeginnersGuide/Download).

Once Python is downloaded, make sure that all the files included in the repository, <code>weekly_options_pricing_tool.py</code>, <code>ticker_information.txt</code>, and <code>requirements.txt</code>, are in the same folder. 

To install the outside packages that are used in the project, run the command <code>pip install -r requirements.txt</code> in the terminal.

Finally, the Python script can be ran by writing this command in the terminal: <code>python weekly_options_pricing_tool.py</code>.

## Formatting of <code>ticker_information.txt</code>

The format of <code>ticker_information.txt</code> is extremely important, as it is the way the Python script can access the desired tickers.

Each line in the file needs to have three main components (which are all separated by a space): 
- symbol
- percent change or the desired strike price
- contract type

The first component, the symbol, is the string of letters that represent the stock ("AAPL" is the symbol for Apple, "MSFT" is the symbol for Microsoft).

The second component can be either the percent change of the stock at the time to a strike price, or a desired strike price of a contract. For example, if I would like to see strike prices 15% away from the current price, the second component would be "0.15". However, if I would rather see the contract information with a strike price of $100.00, the second component would be "100.00".

<strong>If a percent chance is the second component, it must be a positive real number between 0 and 1.</strong>

The third component represents the type of the contract and will have two parts to it: position type and contract type. The first character, representing position type, will describe a "long" or "short" position. The second character, representing contract type, will describe a "call" or "put" option. Therefore, there are only four recognizable inputs for this third component:
- "LC" (long call)
- "LP" (long put)
- "SC" (short call)
- "SP" (short put)

For example, if your percent change of the stock ticker "SPY" over the week is 5% and you desire a short put contract, then the line in <code>ticker_information.txt</code> should read "<strong>SPY 0.05 SP</strong>".

## Reading the Output

The Python script will calculate a contract that best suits the position type, contract type, and desired percent change. For short contracts, the script will calculate the closest contract outside of the entered percent change. For long contracts, the script will calculate the closest contract that is in-the-money (ITM) based on the entered percent change.

Using our example from above for our short put, we would get the nearest contract that does not break a 5% change.

## ITM Contract Concerns

An unfortunate aspect of this script is that it cannot calculate the best overall option contract for ITM contracts. Because ITM contracts already have some intrinsic value (otherwise known as "moneyness"), the "optimal contract" for these ITM contracts are subjective. If you would like to see ITM contract information, the strike price must be entered into the second component as discussed above.

Interestingly, if you change the percent change to be negative, you can get ITM contracts; however, this option does not give any unique information compared to entering an ITM strike price.