# Failures and bounded retry

- Call 01: rejected mechanically because `str.isdigit()` accepts Unicode
  decimal characters and the contract requires ASCII digits only.
- Call 02: passed extraction, compilation, and the full parser contract.
- Calls used: 2 of maximum 2. No third call was made.
- vLLM was not stopped or started; it was already intentionally stopped.
