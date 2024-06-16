# findFit.py

This is just a script, but it works well and has these features:

  - Fails gracefully, not losing the progress (such as when you terminate it early or if you run out of money halfway through).
  - Attempts to resume partially completed executions.
  - Uses newest model, currently 4o, which fortunately is also cheap.
  - Progress bar.
  - Gets project/API key from an environment variable.
  - Takes CSV filename and column name as parameters.
