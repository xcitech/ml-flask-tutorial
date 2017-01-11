from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/getdelay',methods=['POST','GET'])
def get_delay():
    if request.method=='POST':
        result=request.form
        origin = result['origin']
        dest = result['dest']
        unique_carrier = result['unique_carrier']
        day_of_week = result['day_of_week']
        dep_hour = result['dep_hour']

        pkl_file = open('cat', 'rb')
        index_dict = pickle.load(pkl_file)
        cat_vector = np.zeros(len(index_dict))
        
        try:
            cat_vector[index_dict['DAY_OF_WEEK_'+str(day_of_week)]] = 1
        except:
            pass
        try:
            cat_vector[index_dict['UNIQUE_CARRIER_'+str(unique_carrier)]] = 1
        except:
            pass
        try:
            cat_vector[index_dict['ORIGIN_'+str(origin)]] = 1
        except:
            pass
        try:
            cat_vector[index_dict['DEST_'+str(dest)]] = 1
        except:
            pass
        try:
            cat_vector[index_dict['DEP_HOUR_'+str(dep_hour)]] = 1
        except:
            pass
        
        pkl_file = open('logmodel.pkl', 'rb')
        logmodel = pickle.load(pkl_file)
        prediction = logmodel.predict(cat_vector)
        
        return render_template('result.html',prediction=prediction)

    
if __name__ == '__main__':
	app.debug = True
	app.run()