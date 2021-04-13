from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
import datetime

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://yourate:Weetikniet2000!@134.122.57.236:3306/yourate'
db = SQLAlchemy(app)

#personeel = db.Table('personeel', db.metadata, autoload=True, autoload_with=db.engine)
#posts = db.Table('vlucht', db.metadata, autoload=True, autoload_with=db.engine)
#vluchtroutes = db.Table('vluchtroute', db.metadata, autoload=True, autoload_with=db.engine)


base = automap_base()
base.prepare(db.engine, reflect=True)

# user = base.classes.users
# post = base.classes.posts


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_id = request.form['id']
        new_name = request.form['name']
        new_username = request.form['username']
        new_email = request.form['email']
        new_password = request.form['password']

        new_users = user(id=new_id, name=new_name, username=new_username,
                         email=new_email, password=new_password)

        try:
            db.session.add(new_users)
            db.session.commit()
            return redirect('/index')

        except:
            return 'Er is iets fout gegaan tijdens het toevoegen van een user'

    else:
        results = db.session.query(user).all()
        totaal = db.session.query(user).count()
        return render_template('index.html', results=results, totaal=totaal)


@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = db.session.query(
        user).filter_by(id=id).first()

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect('/index')
    except:
        return'Het verwijderen van een user is mislukt'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    users = db.session.query(user).filter_by(
        id=id).first()

    if request.method == 'POST':
        users.id = request.form['id']
        users.name = request.form['name']
        users.email = request.form['email']
        users.username = request.form['username']

        try:
            db.session.commit()
            return redirect('/index')
        except:
            'Er is iets fout gegaan tijdens het bewerken van de user'

    else:
        return render_template('update.html', users=users)


# Vluchten & Routes  ---------------------------------------------------------------------------------------------------------


@app.route('/posts.html', methods=['GET', 'POST'])
def posts():
    posts = db.session.query(post).all()
    totaal = db.session.query(post).count()
    return render_template('posts.html', posts=posts, totaal=totaal)


@app.route('/posts/delete/<int:id>')
def deleteposts(id):
    posts_to_delete = db.session.query(
        post).filter_by(id=id).first()

    try:
        db.session.delete(posts_to_delete)
        db.session.commit()
        return redirect('/posts.html')
    except:
        return'Het verwijderen van een post is mislukt'


@app.route('/routes.html', methods=['GET', 'POST'])
def routes():

    if request.method == 'POST':
        new_routenr = request.form['RouteNr']
        new_vertrekplaats = request.form['Vertrek_plaats']
        new_aankomstplaats = request.form['Aankomst_plaats']

        new_route = route(RouteNr=new_routenr, Vertrek_Plaats=new_vertrekplaats,
                          Aankomst_Plaats=new_aankomstplaats)

        try:
            db.session.add(new_route)
            db.session.commit()
            return redirect('/routes.html')

        except:
            return 'Er is iets fout gegaan tijdens het toevoegen van een route'

    else:
        routes = db.session.query(route).all()
        return render_template('routes.html', routes=routes)

# Passagiers --------------------------------------------------------------------------------------------


@app.route('/passagier.html', methods=['GET', 'POST'])
def passagier():
    if request.method == 'POST':
        new_Passagiersnr = request.form['passagierNummer']
        new_voornaam = request.form['voornaam']
        new_achternaam = request.form['achternaam']
        new_email = request.form['email']
        new_ticket = request.form['ticket']

        new_Passagier = z(PassagierNr=new_Passagiersnr, TicketNr=new_ticket, Voornaam=new_voornaam,
                          Achternaam=new_achternaam, Email=new_email)

        try:
            db.session.add(new_Passagier)
            db.session.commit()
            return redirect('/passagier.html')

        except:
            return 'Er is iets fout gegaan tijdens het toevoegen van Passagier'

    else:
        passagiers = db.session.query(
            z, ticket).filter(z.TicketNr == ticket.TicketNr).all()
    return render_template('passagier.html', passagiers=passagiers)

# Vliegtuig---------------------------------------------------------------------------------------------


@app.route('/vliegtuigen.html', methods=['GET', 'POST'])
def vliegtuigen():

    if request.method == 'POST':
        new_TimeStamp = datetime.datetime.now()
        new_VliegtuigNr = request.form['vliegtuignr']
        new_VliegtuigNaam = request.form['vliegtuignaam']
        new_Longitude = request.form['longitude']
        new_Latitude = request.form['latitude']

        new_vliegtuig = vliegtuig(TimeStamp=new_TimeStamp, VliegtuigNr=new_VliegtuigNr, VliegtuigNaam=new_VliegtuigNaam,
                                  Latitude=new_Latitude, Longitude=new_Longitude)

        try:
            db.session.add(new_vliegtuig)
            db.session.commit()
            return redirect('vliegtuigen.html')

        except:
            return 'Er is iets fout gegaan tijdens het toevoegen van vliegtuig'

    else:
        results = db.session.query(vliegtuig).all()
        return render_template('vliegtuigen.html', results=results)


if __name__ == "__main__":
    app.run(debug=True)
