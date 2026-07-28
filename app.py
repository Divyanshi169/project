from flask import Flask, render_template, request
from hide import predict_stock

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None

    if request.method == "POST":
        symbol = request.form.get("symbol", "").upper()
        if symbol:
            result = predict_stock(symbol)
            if result is None:
                error = "Invalid Stock Symbol"

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=False)