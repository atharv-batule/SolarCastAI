from flask import Flask, jsonify
from predict import predict_today

app = Flask(__name__)

@app.route("/solar-forecast", methods=["GET"])
def solar_forecast():

    df = predict_today(15.2833, 73.9833)

    result = df.to_dict(orient="records")

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)