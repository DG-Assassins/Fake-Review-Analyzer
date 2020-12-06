from flask import Flask, render_template,request, make_response,redirect,session,url_for,send_file,jsonify
from product_reviews import create_output
from hotel_reviews import create_hotel_output
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/result',methods=['POST'])
def get_result():
    data_url = request.form['url_req']
    optreq = request.form['optradio']
    print("OPTREQ = ",optreq)
    if (optreq == "product"):
        result_out = create_output(data_url)
        
    elif (optreq == "hotel"):
        print(data_url)
        result_out = create_hotel_output(data_url)
    result_out = enumerate(result_out)
    return render_template('index.html',messages=result_out)

if (__name__ == '__main__'):
    app.run(debug=False,threaded=False)

