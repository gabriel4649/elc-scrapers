from flask import Flask, request
app = Flask(__name__)

@app.route("/save_url", methods=['POST'])
def save_url():
    with open('urls', 'a') as urlsFile:
        urlsFile.write(request.form['url'] + "\n")

    return "ok"

if __name__ == "__main__":
    app.run(debug=True)
