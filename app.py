from flask import Flask, render_template, request
import pickle


vector=pickle.load(open("vectorizer.pkl","rb"))
model=pickle.load(open("finalized_model.pkl","rb"))

app = Flask(__name__)

@app.route("/")
def Home():
    return render_template("index.html")
@app.route('/Prediction',methods=['GET','POST'])
def prediction():
  if request.method=="POST":
        news=str(request.form['news'])
        print(news)
        predict=model.predict(vector.transform([news]))[0]
        print(predict)
        return render_template("prdiction.html",prediction_text="News Headline is->{}".format(predict))
  else:
     return render_template("prdiction.html")


if __name__== '__main__':
    app.run()