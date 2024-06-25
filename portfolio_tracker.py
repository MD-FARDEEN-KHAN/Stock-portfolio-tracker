import yfinance as yf

class Stock:
    def __init__(self, symbol, shares):
        self.symbol = symbol
        self.shares = shares
        self.update_price()

    def update_price(self):
        stock = yf.Ticker(self.symbol)
        self.price = stock.history(period='1d')['Close'].iloc[-1]
        self.value = self.shares * self.price

class Portfolio:
    def __init__(self):
        self.stocks = {}

    def add_stock(self, symbol, shares):
        if symbol in self.stocks:
            self.stocks[symbol].shares += shares
        else:
            self.stocks[symbol] = Stock(symbol, shares)
        self.stocks[symbol].update_price()

    def remove_stock(self, symbol, shares):
        if symbol in self.stocks:
            if self.stocks[symbol].shares >= shares:
                self.stocks[symbol].shares -= shares
                if self.stocks[symbol].shares == 0:
                    del self.stocks[symbol]
            else:
                print(f"Not enough shares to remove. You only have {self.stocks[symbol].shares} shares.")
        else:
            print(f"Stock {symbol} not found in portfolio.")

    def update_portfolio(self):
        for stock in self.stocks.values():
            stock.update_price()

    def get_portfolio_value(self):
        self.update_portfolio()
        total_value = sum(stock.value for stock in self.stocks.values())
        return total_value

    def print_portfolio(self):
        self.update_portfolio()
        print("Portfolio:")
        for symbol, stock in self.stocks.items():
            print(f"{symbol}: {stock.shares} shares @ ${stock.price:.2f} each, Total Value: ${stock.value:.2f}")
        print(f"Total Portfolio Value: ${self.get_portfolio_value():.2f}")

# Example usage
portfolio = Portfolio()
portfolio.add_stock('AAPL', 10)
portfolio.add_stock('GOOGL', 5)
portfolio.print_portfolio()

portfolio.add_stock('AAPL', 5)
portfolio.remove_stock('GOOGL', 2)
portfolio.print_portfolio()

portfolio.remove_stock('AAPL', 20)
portfolio.print_portfolio()
