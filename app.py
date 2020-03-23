from flask import Flask, render_template, request, jsonify
import model

app = Flask(__name__)


@app.route("/")
def index():    
    return render_template("index.html") 


"""@app.route("/get")
def getBotResponse():
	userText = str(request.args.get('msg'))
	print(userText)
	print(model.chatbot_response(userText))
	return str(model.chatbot_response(userText))"""

@app.route("/get", methods=["GET", "POST"])
def getBotResponse():
	userText = str(request.args.get('name'))
	print(userText)
	print(model.chatbot_response(userText))
	return str(model.chatbot_response(userText))

if __name__ == "__main__":    
    app.run(debug=True)