import marimo

__generated_with = "0.13.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import altair as alt
    return alt, mo, np


@app.cell
def _(mo):
    mo.md("""
          This is a test
          """)
    return

if __name__ == "__main__":
    app.run()
