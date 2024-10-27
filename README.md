## Risk Metric Systems Objectives Project Overview

# Overview

This project aims to develop a financial risk analysis system to assess risk metrics of a portfolio. It incorporates several parts to conduct risk metric analysis and reporting.
Table of Contents

-	Process Flowchart

-	Assumptions 

-	Configuration File

-	Proof of Concept

-	Risk Calculation Objects 

-   Historical Risk Metrics Reporting and Storing

## Process Flow Chart

Visual representation of the workflow within the Risk Metric Systems, aiding in understanding the overall process and interactions between various components. 


## Assumptions 

- It's assumed that the historical market data fetched via yfinance is accurate and complete.

- When parametric methods are used to calculate Value at Risk (VaR) it's often assumed that portfolio returns are normally distributed. This assumption allows for the use of z-scores and the normal distribution's properties.

- The risk metrics are calculated with the assumption that the portfolio composition (weights of different assets) remains constant over the calculation horizon. 

- The calculations may assume that assets are independent. 


## Configuration File

The configuration file outlines various components for the portfolio configuration. This YAML file includes information on different holdings in the portfolio, along with attributes like risk tolerance, capital, and rebalancing strategy.

## Proof of Concept

This section would demonstrate the viability of the system with a simplified, working version of your project. It includes basic implementations of the risk calculation and reporting features.

## Risk Calculation Objects 

The Risk Model file is the analytical core of the risk metric project, responsible for assessing the financial risks of an investment portfolio. It processes portfolio details, fetches historical data, and calculates key risk metrics like VaR and TVaR, alongside summary statistics. 

## Historical Risk Metrics Reporting and Storing 

The main file loads portfolio configurations, leveraging the Risk Model to calculate risk metrics and summary statistics, and then saving and displaying the results. It acts as the interface between the user's input and the analytical capabilities of the Risk Model.


