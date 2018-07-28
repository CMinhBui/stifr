import fastText
from flask import Flask, request

FT_MODEL_INTENT = "intent.bin"
FT_MODEL_YESNO = "yesno.bin"
app = Flask(__name__)

model_intent = None
model_yesno = None

def init():
    global model_intent, model_yesno
    model_intent = fastText.load_model(FT_MODEL_INTENT)
    #model_yesno = fastText.load_model(FT_MODEL_YESNO)

def ft_classifier(model, req):
    text = req.json['text']
    res = model.predict(text)
    return res[0][0]

@app.route("/intention", methods=["POST"])
def intention():
    return ft_classifier(model_intent, request)

@app.route("/yesno", methods=["POST"])
def yesno():
    return ft_classifier(model_yes, request)

if __name__ == "__main__":
    init()
    app.run(host="0.0.0.0", port=1812)
