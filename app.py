from flask import Flask, session, redirect, url_for, request, escape
from flask import render_template
from gothonweb import Planisphere

app = Flask(__name__)

count = 0

@app.route("/")
def index():
    session['room_name'] = Planisphere.START
    return redirect(url_for("game"))

@app.route("/game", methods=['POST', 'GET'])
def game():
    room_name = session.get('room_name')
    global count
    val = ""
    if request.method == 'GET':
        if room_name:
            room = Planisphere.load_room(room_name)
            return render_template("show_room.html", room=room, count=10)
        
        else:
            return render_template("you_died.html")
    
    else:
        action = request.form.get('action')

        if room_name and action:
            room = Planisphere.load_room(room_name)
            next_room = room.go(action.lower())
            if room_name == 'laser_weapon_armory':
                try:
                    if action == '013':
                        count = 0
                        session['room_name'] = Planisphere.name_room(next_room)
                    else:
                        while(count < 9):
                            if int(action) > 13:
                                val = 'Input too high'
                            else:
                                val = 'Input too low'
                            session['room_name'] = Planisphere.name_room(room)
                            count = count + 1
                            return render_template("show_room.html", room=room, count=10-count, val=val)
                        count = 0
                        next_room = room.go('*')
                        session['room_name'] = Planisphere.name_room(next_room)
                except ValueError:
                    return render_template("show_room.html", room=room, count=10-count, input_val="Invalid Input")

            if room_name == 'escape_pod':
                if action == '2':
                    session['room_name'] = Planisphere.name_room(next_room)
                else:
                    next_room = room.go('*')
                    session['room_name'] = Planisphere.name_room(next_room)                      
            
            if not next_room:
                session['room_name'] = Planisphere.name_room(room)
                return render_template("show_room.html", room=room, count=10-count, input_val="Invalid Input")



            else:
                session['room_name'] = Planisphere.name_room(next_room)
        
        return redirect(url_for("game"))

app.secret_key = 'A0Zr98j/3yX R~XHH!jN8]LWX/,?RT'

if __name__ == "__main__":
    app.run()