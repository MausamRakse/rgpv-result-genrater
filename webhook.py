from flask import Flask,request,abort,send_file
import os
from threading import Thread
import json
# from generate_token import generate_token

app=Flask(__name__)

def start(data):
    os.system('python Automation.py '+data['code']+' '+data['branch']+' '+data['year']+' '+data['sem']+' '+data['start']+' '+data['end']+' '+data['nol']+' '+(str)(data['token']))

@app.route('/webhook',methods=['POST'])
def webhook():
    if request.method=='POST':
        data=request.json
        # token=generate_token()
        print(request.json)
        worker = Thread(target=start,args=(data,))
        # executor = ThreadPoolExecutor(max_workers=5)
        # executor.submit(start(data))
        worker.start()
        total_time=(int)(((int)(data['end'])-(int)(data['start'])+(int)(data['nol']))/8)
        
        # os.system('python Automation.py '+data['code']+' '+data['branch']+' '+data['year']+' '+data['sem']+' '+data['start']+' '+data['end']+ ' '+data['nol']+' '+str(data['token']))
        # print(request.json)
        text='Process Started Your Token Is '+(str)(data['token'])+"\nPlease Keep This Token Safely To Get Your File\nYour Estimated Wait Time Is "+(str)(total_time+2)+" Minutes"
        response = {
            'text':text,
            'total_time':total_time+2
        }
        response=json.dumps(response)
        return response
    else:
        abort(400)

@app.route('/get_file',methods=['GET'])
def get_file():
    if request.method=='GET':
        token=request.args.get('token')
        if os.path.isfile(f'files\{token}.csv'):
            try:
                os.rename(f'files\{token}.csv', f'files\{token}.csv')
                return send_file(f'files\{token}.csv')
            except OSError as e:
                return 'Your File Is Not Completed'
        else:
            return 'File Not Found'
    else:
        abort(400)

if __name__=='__main__':
    app.run(port=80,debug=True)

