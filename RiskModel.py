


import pandas as pd
import numpy as np
from datetime import timedelta
import yfinance as yf
import os

class PortfolioRiskMetrics:
    def __init__(self, tickers, alpha, trade_horizon, capital, start_day, historical_horizon):
        # Ensure alpha is interpreted as the lower tail if above 0.5
        self.alpha = max(alpha, 1 - alpha)
        self.tickers = tickers
        self.trade_horizon = trade_horizon
        self.capital = capital
        self.start_day = pd.to_datetime(start_day)
        self.end_day = self.start_day + timedelta(days=self.trade_horizon)
        self.historical_horizon = historical_horizon

        
        # Fetch historical price data within the specified date range
        self.prices = self.fetch_price_data()
        self.returns = self.prices.pct_change().dropna()
        self.log_returns = np.log(self.prices / self.prices.shift(1)).dropna()

        # Calculate portfolio metrics                                                        
        self.portfolio_returns = self.calculate_portfolio_returns()
        self.portfolio_log_returns = self.calculate_portfolio_log_returns()
        self.portfolio_summary = self.generate_summary_statistics()
        self.portfolio_normal_std_dev = self.calculate_portfolio_std_dev(self.returns)
        self.portfolio_lognormal_std_dev = self.calculate_portfolio_std_dev(self.log_returns)
        self.daily_normal_returns = self.calculate_daily_returns(self.returns)
        self.daily_log_returns = self.calculate_daily_returns(self.log_returns)

#
        self.var_normal_historical = None
        self.var_lognormal_historical = None

        self.calculate_var_metrics()
#

    def fetch_price_data(self):
        end_day = self.start_day + pd.DateOffset(days=self.historical_horizon)
        data = yf.download(self.tickers, start=self.start_day, end=end_day)['Adj Close']
        return data

    def calculate_portfolio_returns(self):
        # Aggregate and average the returns across all tickers to get portfolio returns
        return self.returns.mean(axis=1) * self.trade_horizon

    def calculate_portfolio_log_returns(self):
        # Aggregate and average the log returns across all tickers to get portfolio log returns
        return self.log_returns.mean(axis=1) * self.trade_horizon
    
    def calculate_portfolio_std_dev(self, returns):
        # Calculate the standard deviation of the portfolio returns
        return returns.std(axis=1).mean() * np.sqrt(self.trade_horizon)

    def calculate_daily_returns(self, returns):
        # Calculate the average daily returns
        return returns.mean(axis=1)


    def generate_summary_statistics(self):
        summary = {
            'Normal Returns': self.portfolio_returns.describe(),
            'Log Returns': self.portfolio_log_returns.describe()
        }
        return summary
    
    def calculate_var_metrics(self):
        # Ensure the VaR metrics are initialized
        if self.returns.empty or self.log_returns.empty:
            raise ValueError("No return data available to calculate VaR.")

        # Historical VaR for normal returns
        sorted_normal_returns = np.sort(self.returns)
        historical_index_normal = int((1 - self.alpha) * len(sorted_normal_returns))
        self.var_normal_historical = sorted_normal_returns[historical_index_normal]

        # Historical VaR for lognormal returns
        sorted_log_returns = np.sort(self.log_returns)
        historical_index_log = int((1 - self.alpha) * len(sorted_log_returns))
        self.var_lognormal_historical = sorted_log_returns[historical_index_log]

    def calculate_all_var(self):
        if self.var_normal_historical is None or self.var_lognormal_historical is None:
            self.calculate_var_metrics()

        # Scaling VaR from daily to trade_horizon
        var_normal_historical_scaled = self.var_normal_historical * np.sqrt(self.trade_horizon)
        var_lognormal_historical_scaled = self.var_lognormal_historical * np.sqrt(self.trade_horizon)

        return {
            'var_normal_historical_scaled': self.capital * var_normal_historical_scaled,
            'var_lognormal_historical_scaled': self.capital * var_lognormal_historical_scaled
        }
    
    
    def calculate_historical_tvar(self, returns):
        """
        Calculates the historical Tail Value at Risk (TVaR) for the given returns.
        This is the average of the worst losses beyond the VaR threshold.
        """
        # Sort returns from worst to best
        sorted_returns = np.sort(returns)
        
        # Find the threshold return at the alpha level for VaR
        vaR_index = int(np.ceil((1 - self.alpha) * len(sorted_returns))) - 1
        vaR_threshold = sorted_returns[vaR_index]

        # Average the returns worse than the VaR threshold to calculate TVaR
        tvar = sorted_returns[:vaR_index + 1].mean()

        return tvar
    
    def calculate_all_tvar(self):
        # Calculate historical TVaR for normal returns
        tvar_normal = self.calculate_historical_tvar(self.portfolio_returns) * np.sqrt(self.trade_horizon)

        # Calculate historical TVaR for lognormal returns
        tvar_lognormal = self.calculate_historical_tvar(self.portfolio_log_returns) * np.sqrt(self.trade_horizon)

        return {
            'tvar_normal_historical_scaled': self.capital * tvar_normal,
            'tvar_lognormal_historical_scaled': self.capital * tvar_lognormal
        }
    
    def calculate_historical_es(self, returns):
        """
        Calculates the historical Expected Shortfall (ES) for the given returns.
        This is effectively the same calculation as TVaR.
        """
        # Sort returns from worst to best
        sorted_returns = np.sort(returns)
        
        # Find the threshold return at the alpha level for VaR
        vaR_index = int(np.ceil((1 - self.alpha) * len(sorted_returns))) - 1

        # Average the returns worse than the VaR threshold to calculate ES
        es = sorted_returns[:vaR_index + 1].mean()

        return es

    def calculate_all_es(self):
        # Calculate historical ES for normal returns
        es_normal = self.calculate_historical_es(self.portfolio_returns) * np.sqrt(self.trade_horizon)

        # Calculate historical ES for lognormal returns
        es_lognormal = self.calculate_historical_es(self.portfolio_log_returns) * np.sqrt(self.trade_horizon)

        return {
            'es_normal_historical_scaled': self.capital * es_normal,
            'es_lognormal_historical_scaled': self.capital * es_lognormal
        }
    
    def generate_risk_report(self):
        # Calculate all necessary metrics
        var_metrics = self.calculate_all_var()
        tvar_metrics = self.calculate_all_tvar()
        es_metrics = self.calculate_all_es()

        # Define the metrics and their corresponding values in a list of tuples
        risk_metrics_data = [
            ('Capital at Risk', self.capital),
            ('Alpha Level', self.alpha),
            ('Trade Horizon (days)', self.trade_horizon),
            ('Historical VaR (Normal)', var_metrics['var_normal_historical_scaled']),
            ('Historical VaR (Lognormal)', var_metrics['var_lognormal_historical_scaled']),
            ('Tail Value at Risk (Normal)', tvar_metrics['tvar_normal_historical_scaled']),
            ('Tail Value at Risk (Lognormal)', tvar_metrics['tvar_lognormal_historical_scaled']),
            ('Expected Shortfall (Normal)', es_metrics['es_normal_historical_scaled']),
            ('Expected Shortfall (Lognormal)', es_metrics['es_lognormal_historical_scaled'])
        ]

        # Convert the list of tuples into a DataFrame for better visualization
        risk_result_df = pd.DataFrame(risk_metrics_data, columns=['Risk Metric', 'Value'])

        # Ensure the directory exists or create it
        directory = ""
        if not os.path.exists(directory):
           os.makedirs(directory)
    
       # Specify the full path including the filename for the CSV
        file_path = os.path.join(directory, 'risk_metrics_analysis.csv')
    
       # Save the DataFrame to a CSV file
        risk_result_df.to_csv(file_path, index=False)
    
        print(f"Risk report saved to {file_path}")  
       
        return risk_result_df
