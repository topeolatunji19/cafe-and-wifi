from flask import Flask, render_template, request, jsonify, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, URL
from flask_bootstrap import Bootstrap


Base = declarative_base()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some_random_key'

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField(label="City Name", validators=[DataRequired()])
    map_url = StringField(label="Cafe Location on Google Maps (URL)", validators=[DataRequired(), URL()])
    img_url = StringField(label="Image URL of the Cafe", validators=[DataRequired(), URL()])
    has_sockets = BooleanField(label="Does the Cafe have Sockets?", validators=[DataRequired()])
    has_toilet = BooleanField(label="Does the Cafe have Toilets?", validators=[DataRequired()])
    has_wifi = BooleanField(label="Does the Cafe have Wi-Fi?", validators=[DataRequired()])
    can_take_calls = BooleanField(label="Can You take Calls here?", validators=[DataRequired()])
    seats = StringField('How many seats are available', validators=[DataRequired()])
    coffee_price = StringField('What is the Price of the Coffee here?', validators=[DataRequired()])
    submit = SubmitField('Add Cafe')


class Cafes(Base):

    __tablename__ = "cafe"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True, nullable=False)
    map_url = Column(String(500), nullable=False)
    img_url = Column(String(500), nullable=False)
    location = Column(String(250), nullable=False)
    has_sockets = Column(Boolean, nullable=False)
    has_toilet = Column(Boolean, nullable=False)
    has_wifi = Column(Boolean, nullable=False)
    can_take_calls = Column(Boolean, nullable=False)
    seats = Column(String(250), nullable=False)
    coffee_price = Column(String(250), nullable=False)


engine = create_engine("sqlite:///cafes.db")

# Base.metadata.create_all(engine)


@app.route("/")
def home():
    with Session(engine) as session:
        available_cafes = session.query(Cafes).all()
    return render_template("index.html", cafes=available_cafes)


@app.route("/add-cafe", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with Session(engine) as session:
            new_cafe = Cafes(
                name=form.cafe.data,
                location=form.location.data,
                img_url=form.img_url.data,
                map_url=form.map_url.data,
                coffee_price=form.coffee_price.data,
                has_sockets=form.has_sockets.data,
                has_wifi=form.has_wifi.data,
                has_toilet=form.has_toilet.data,
                can_take_calls=form.can_take_calls.data,
                seats=form.seats.data
            )
            session.add(new_cafe)
            session.commit()
        return redirect(url_for('home'))
    return render_template("add-cafe.html", form=form)


# HTTP GET - Read Record
@app.route("/all", methods=["GET"])
def all_cafes():
    with Session(engine) as session:
        cafes = session.query(Cafes).all()
        list_of_cafes = []
        for each_cafe in cafes:
            cafe = {
                "id": each_cafe.id,
                "name": each_cafe.name,
                "map_url": each_cafe.map_url,
                "img_url": each_cafe.img_url,
                "location": each_cafe.location,
                "seats": each_cafe.seats,
                "has_toilet": each_cafe.has_toilet,
                "has_wifi": each_cafe.has_wifi,
                "has_sockets": each_cafe.has_sockets,
                "can_take_calls": each_cafe.can_take_calls,
                "coffee_price": each_cafe.coffee_price
            }
            list_of_cafes.append(cafe)
        return jsonify(cafes=list_of_cafes)


if __name__ == "__main__":
    app.run(debug=True)
