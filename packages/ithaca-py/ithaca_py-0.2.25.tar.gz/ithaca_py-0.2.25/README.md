# Ithaca SDK

## Modules

- Auth

  - login
  - logout
  - get_session_info

- Client

  - fundlock_state
  - curret_positions
  - trade_history
  - historical_positions
  - historical_positions_by_date

- FundLock #TODO

  - deposit
  - withdraw
  - cross_chain_deposit
  - get_cross_chain_tx_status
  - fundlock_history

- Protocol

  - system_info
  - next_auction
  - contract_list
  - contract_list_by_ids
  - historical_contracts

- Testnet

  - matched_orders
  - orderbook

- Orders

  - new
  - status
  - cancel
  - cancel_all
  - open_orders

- Market

  - spot_prices
  - reference_prices

- Calculation
  - calc_portfolio_collateral
  - estimate_order_payoff
  - estimate_order_lock
  - estimate_order_fees
  - black_formula_extended
  - black_vanilla_price
  - black_digital_price
  - implied_volatility

## Prepare

```
pre-commit run --all-files
```

## Docs

```
sphinx-apidoc -o docs ithaca
sphinx-build -M html docs docs/_build
```

## Tests

```python
pytest
```
