from flask import Flask, render_template,request,redirect,session
from flask_socketio import SocketIO,send,emit
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret!"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['transports'] = 'websocket'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')


@socketio.on('join')
def join_chat(data):
    emit('status',{'msg':f"{session.get('username')} joined the chat"},broadcast=True)

@socketio.on('message')
def handle_message(data):
    if data!='a user connected!' and data!="":
        print(f"\n\n\n[-]{session.get('username')}: {data}\n\n\n")
        if '<' and '>' in data:
            print("\n\n\n\nhere\n\n\n\n\n")
            n_data= data.replace('<','&lt').replace('>','&gt')
            send({'msg':f"{n_data}",'user':f"{session.get('username')}",'userid':f"{session.get('userid')}"},broadcast=True)    
        else:
            send({'msg':f"{data}",'user':f"{session.get('username')}",'userid':f"{session.get('userid')}"},broadcast=True)

@socketio.on('leave_room')
def leave_room(data):
    username=session.get('username')
    session.clear()
    emit('status',{'msg':f"{username} leaves the chat"},broadcast=True)
    





@app.route("/",methods=['GET','POST'])
def home_page():
    return render_template("home.html")

@app.route("/chatroom.html",methods=['GET','POST'])
def chat():
    
    if request.method=='POST':
        name=" ".join((request.form['name']).split())
        uid=" ".join((request.form['userid']).split())
        session['username']=name
        session['userid']=uid
        if session.get('username') !="" and session.get('userid')!="":
            print(f"\n\n\n\n{session.get('username')} Joined the chat\n\n\n\n")
            return render_template('chatroom.html',session=session)
        else:
            return redirect('/')
    else:
        return redirect('/')





if __name__ == "__main__":
    app.run(debug=True)
