from flask import Flask,render_template,request
from Heart_Disease_Prediction.pipeline.predict_pipeline import CustomData,PredictPipeline
from Heart_Disease_Prediction.logging.logging import logging

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict",methods=["GET",'POST'])

def predict():
    if request.method=="GET":
        return render_template('home.html')
    else:
        # age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal,target
# 43,1,0,115,303,0,1,181,0,1.2,1,0,2,1
        data=CustomData(
            age=request.form.get("age"),
            sex=request.form.get("sex"),
            cp=request.form.get("cp"),
            trestbps=request.form.get("trestbps"),
            chol=request.form.get("chol"),
            fbs=request.form.get("fbs"),
            restecg=request.form.get("restecg"),
            thalach=request.form.get("thalach"),
            exang=request.form.get("exang"),
            oldpeak=request.form.get("oldpeak"),
            slope=request.form.get("slope"),
            
            ca=request.form.get("ca"),
            
            thal=request.form.get("thal"),
            
            # oldpeak=request.form.get("oldpeak"),
            


        )

        data_frame=data.get_data_as_dataframe()
        logging.info(f"the data frame is {data_frame}")
        predict_pipeline=PredictPipeline()
        results=predict_pipeline.predict(data_frame)
        logging.info(f"the prediction should be:{results}")
        print(results)
        return render_template("home.html",results=results[0])
    




if __name__=="__main__":
    app.run(debug=True)