from flask import Flask, render_template, request
from flask import Flask, render_template, request
import os
import numpy as np

from pyit2fls import IT2FS, trapezoid_mf, tri_mf,gaussian_mf, IT2FS_Gaussian_UncertMean, \
    IT2FS_plot, IT2FLS, min_t_norm, max_s_norm, TR_plot, crisp
from numpy import linspace


def calculate_FLS(heart_disease,Age,bmi,avg_glucose_level):

    # For IT2FS_Gaussian_UncertMean, the parameters define:
    # 1 - The tip of the center point of the curve
    # 2 - The width of the lower curve (higher value = lower width)
    # 3 - The height of the lower curve (higher value = higher tip)
    # 4 - The height of the center point of the outer curve.
    # for TRIMF The left end, the center, the right end, and the height of the triangular membership function
    # The left end, the left center, the right center, the right end, and the height of the trapezoidal membership function
    range1=linspace(0,2,100)
    heart_disease_No= IT2FS(range1,tri_mf,[-0.75,0,0.75,1])
    heart_disease_Yes = IT2FS(range1,tri_mf,[0.25,1,1.75,1])
    
    range2=linspace(0,100,1000)
    age_young=IT2FS(range2,tri_mf,[-35,0,35,1])
    age_middle=IT2FS(range2,tri_mf,[20,45,70,1])
    age_old=IT2FS(range2,tri_mf,[50,75,100,1])
    
    range3=linspace(0,50,100)
    bmi_normalweight=IT2FS(range3,tri_mf,[0,12,25,1])
    bmi_overweight=IT2FS(range3,tri_mf,[20,27,35,1])
    bmi_obese=IT2FS(range3,tri_mf,[30,50,75,1])
    
    range4=linspace(0,300,1000)
    glucose_normal=IT2FS(range4,tri_mf,[0,60,125,1])
    glucose_prediabetic=IT2FS(range4,tri_mf,[115,130,145,1])
    glucose_diabetic=IT2FS(range4,tri_mf,[135,210,285,1])
    
    range5=linspace(0,15,100)
    risk_low=IT2FS(range5,tri_mf,[-3.5,0,3.5,1])
    risk_belownormal=IT2FS(range5,tri_mf,[2.5,5.0,7.5,1])
    risk_normal=IT2FS(range5,tri_mf,[5.0,7.5,10,1])
    risk_abovenormal=IT2FS(range5,tri_mf,[7.5,10,12.5,1])
    risk_high=IT2FS(range5,tri_mf,[10,12.5,15.0,1])
    severity = linspace(0.0, 10.0, 100)
    #risk_low = IT2FS_Gaussian_UncertMean(severity, [0, 3, 1, 1.0])
    #risk_normal = IT2FS_Gaussian_UncertMean(severity, [6.5, 2, 1, 1.0])
    #risk_high = IT2FS_Gaussian_UncertMean(severity, [10.7, 1, 1, 1.0])
    def plot_hd_mf():
         IT2FS_plot(heart_disease_No, heart_disease_Yes,
                   title="Heart disease",
                   legends=["low", "high"],
                   )
    def plot_age_mf():
         IT2FS_plot(age_young,age_middle,age_old,
                   title="age",
                   legends=["young aged", "middle aged","old aged"],
                   )
    def plot_bmi_mf():
         IT2FS_plot(bmi_normalweight,bmi_overweight,bmi_obese,
                   title="bmi",
                   legends=["normal weight", "overweight","obese"],
                   )
    def plot_glucose_mf():
         IT2FS_plot(glucose_normal,glucose_prediabetic,glucose_diabetic,
                   title="Average glucose level",
                   legends=["normal", "prediabetic","diabetic"],
                   )
    def plot_risk_mf():
         IT2FS_plot(risk_low,risk_normal,risk_high,
                   title="Risklevel",
                   legends=["lowrisk","Normal","highrisk"],
                   )
    #plot_hd_mf()
    #plot_age_mf()
    #plot_bmi_mf()
    #plot_glucose_mf()
    #plot_risk_mf()
    myIT2FLS = IT2FLS()

    myIT2FLS.add_input_variable("HeartDisease")
    myIT2FLS.add_input_variable("age")
    myIT2FLS.add_input_variable("bmi")
    myIT2FLS.add_input_variable("GlucoseLevel")
    myIT2FLS.add_output_variable("risk")

    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_young ), ("bmi", bmi_normalweight ), ("GlucoseLevel",glucose_normal )], [("risk",risk_low )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_young ), ("bmi", bmi_normalweight ), ("GlucoseLevel",glucose_prediabetic )], [("risk",risk_low )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_young ), ("bmi", bmi_normalweight ), ("GlucoseLevel",glucose_diabetic )], [("risk",risk_low )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_young ), ("bmi", bmi_overweight ), ("GlucoseLevel",glucose_normal )], [("risk",risk_low )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_young ), ("bmi", bmi_overweight ), ("GlucoseLevel",glucose_prediabetic )], [("risk",risk_low )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_young ), ("bmi", bmi_overweight ), ("GlucoseLevel",glucose_diabetic )], [("risk",risk_normal )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_young ), ("bmi", bmi_obese ), ("GlucoseLevel",glucose_normal )], [("risk",risk_normal )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_young ), ("bmi", bmi_obese ), ("GlucoseLevel",glucose_prediabetic )], [("risk", risk_normal)])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_young ), ("bmi", bmi_obese ), ("GlucoseLevel",glucose_diabetic )], [("risk",risk_normal )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_middle ), ("bmi", bmi_normalweight ), ("GlucoseLevel",glucose_normal )], [("risk",risk_low )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_middle ), ("bmi", bmi_normalweight ), ("GlucoseLevel",glucose_prediabetic )], [("risk",risk_low)])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_middle), ("bmi", bmi_normalweight ), ("GlucoseLevel",glucose_diabetic )], [("risk",risk_normal )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_middle), ("bmi", bmi_overweight ), ("GlucoseLevel",glucose_normal )], [("risk",risk_normal )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_middle), ("bmi", bmi_overweight ), ("GlucoseLevel",glucose_prediabetic )], [("risk",risk_normal )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_middle), ("bmi", bmi_overweight ), ("GlucoseLevel",glucose_diabetic )], [("risk",risk_normal)])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_middle), ("bmi", bmi_obese ), ("GlucoseLevel",glucose_normal )], [("risk", risk_normal)])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_middle), ("bmi", bmi_obese ), ("GlucoseLevel",glucose_prediabetic )], [("risk",risk_normal)])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_middle), ("bmi", bmi_obese ), ("GlucoseLevel",glucose_diabetic )], [("risk",risk_high)])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_old ), ("bmi", bmi_normalweight ), ("GlucoseLevel",glucose_normal )], [("risk",risk_low )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_old ), ("bmi", bmi_normalweight ), ("GlucoseLevel",glucose_prediabetic )], [("risk",risk_low )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_old ), ("bmi", bmi_normalweight ), ("GlucoseLevel",glucose_diabetic )], [("risk",risk_normal )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_old ), ("bmi", bmi_overweight ), ("GlucoseLevel",glucose_normal )], [("risk",risk_normal )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_old ), ("bmi", bmi_overweight ), ("GlucoseLevel",glucose_prediabetic )], [("risk",risk_normal )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_old ), ("bmi", bmi_overweight ), ("GlucoseLevel",glucose_diabetic )], [("risk",risk_high )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_old ), ("bmi", bmi_obese ), ("GlucoseLevel",glucose_normal )], [("risk",risk_normal )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_old ), ("bmi", bmi_obese ), ("GlucoseLevel",glucose_prediabetic )], [("risk",risk_abovenormal )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_No), ("age",age_old ), ("bmi", bmi_obese ), ("GlucoseLevel",glucose_diabetic )], [("risk",risk_high)])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_young ), ("bmi", bmi_normalweight ), ("GlucoseLevel",glucose_normal )], [("risk", risk_low )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_young ), ("bmi", bmi_normalweight ), ("GlucoseLevel",glucose_prediabetic )], [("risk", risk_low )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_young ), ("bmi", bmi_normalweight ), ("GlucoseLevel",glucose_diabetic )], [("risk", risk_belownormal )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_young ), ("bmi", bmi_overweight ), ("GlucoseLevel",glucose_normal )], [("risk", risk_belownormal )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_young ), ("bmi", bmi_overweight ), ("GlucoseLevel",glucose_prediabetic )], [("risk", risk_belownormal)])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_young ), ("bmi", bmi_overweight ), ("GlucoseLevel",glucose_diabetic )], [("risk",risk_abovenormal)])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_young ), ("bmi", bmi_obese ), ("GlucoseLevel",glucose_normal )], [("risk",risk_abovenormal )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_young ), ("bmi", bmi_obese ), ("GlucoseLevel",glucose_prediabetic )], [("risk",risk_abovenormal)])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_young ), ("bmi", bmi_obese ), ("GlucoseLevel",glucose_diabetic )], [("risk",risk_abovenormal )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_middle ), ("bmi", bmi_normalweight ), ("GlucoseLevel",glucose_normal )], [("risk",risk_abovenormal )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_middle ), ("bmi", bmi_normalweight ), ("GlucoseLevel",glucose_prediabetic )], [("risk",risk_abovenormal )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_middle), ("bmi", bmi_normalweight ), ("GlucoseLevel",glucose_diabetic )], [("risk",risk_high )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_middle), ("bmi", bmi_overweight ), ("GlucoseLevel",glucose_normal )], [("risk",risk_abovenormal )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_middle), ("bmi", bmi_overweight ), ("GlucoseLevel",glucose_prediabetic )], [("risk",risk_high )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_middle), ("bmi", bmi_overweight ), ("GlucoseLevel",glucose_diabetic )], [("risk",risk_high )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_middle), ("bmi", bmi_obese ), ("GlucoseLevel",glucose_normal )], [("risk",risk_high)])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_middle), ("bmi", bmi_obese ), ("GlucoseLevel",glucose_prediabetic )], [("risk",risk_high)])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_middle), ("bmi", bmi_obese ), ("GlucoseLevel",glucose_diabetic )], [("risk",risk_high )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_old ), ("bmi", bmi_normalweight ), ("GlucoseLevel",glucose_normal )], [("risk",risk_abovenormal )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_old ), ("bmi", bmi_normalweight ), ("GlucoseLevel",glucose_prediabetic )], [("risk",risk_abovenormal )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_old ), ("bmi", bmi_normalweight ), ("GlucoseLevel",glucose_diabetic )], [("risk",risk_high )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_old ), ("bmi", bmi_overweight ), ("GlucoseLevel",glucose_normal )], [("risk",risk_abovenormal )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_old ), ("bmi", bmi_overweight ), ("GlucoseLevel",glucose_prediabetic )], [("risk",risk_high)])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_old ), ("bmi", bmi_overweight ), ("GlucoseLevel",glucose_diabetic )], [("risk",risk_high )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_old ), ("bmi", bmi_obese ), ("GlucoseLevel",glucose_normal )], [("risk",risk_high )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_old ), ("bmi", bmi_obese ), ("GlucoseLevel",glucose_prediabetic )], [("risk",risk_high )])
    myIT2FLS.add_rule([("HeartDisease",heart_disease_Yes), ("age",age_old ), ("bmi", bmi_obese ), ("GlucoseLevel",glucose_diabetic )], [("risk",risk_high)])
   
    
    it2out, tr = myIT2FLS.evaluate({"HeartDisease": heart_disease, "age": Age, "bmi": bmi, "GlucoseLevel": avg_glucose_level},
                                   min_t_norm, max_s_norm, severity,
                                   method="Centroid", algorithm="EKM")
    #print(tr)
    #print(it2out)

    #it2out["risk"].plot(title="Type-2 output MF converted to Type-1")
    #TR_plot(severity, tr["risk"])
    #print("Chance of stroke: ", int((crisp(tr["risk"]))*10 ), "%")

    return  int((crisp(tr["risk"]))*7) 
    

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/result", methods=['POST'])
def result():
    heart_disease = float(request.form['heart_disease'])
    age = float(request.form['age'])
    bmi = float(request.form['bmi'])
    avg_glucose_level= float(request.form['avg_glucose_level'])
    if bmi>72:
         bmi=72
    res=calculate_FLS(heart_disease,age,bmi,avg_glucose_level)
    if res<35:
          return render_template('prediction.html', prediction_text=f'Congratulations, you are safe.\n Probability of you being having stroke is {res} %')
    elif res>=35 and res<60:
          return render_template('prediction.html', prediction_text=f'you are safe for now,Take good care of your health.\n Probability of you being having Stroke is {res} %')
    else: 
        return render_template('prediction.html', prediction_text=f'Risk!,Immedietly Consult the doctor.\n Probability of you being having Stroke is {res} %')
if __name__ == "__main__":
    app.run(debug=True, port=7385)
