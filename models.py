from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    super_name = db.Column(db.String, nullable=False)

    hero_power_relationship = db.relationship('HeroPower', backref='hero_ref', lazy=True)
    serialize_rules = ('-hero_power_relationship.power.hero_power_relationship', '-hero_power_relationship.hero.hero_power_relationship')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name,
            'hero_power_relationship': [hero_power.to_dict() for hero_power in self.hero_power_relationship]
        }

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)

    hero_powers = db.relationship('HeroPower', backref='power_ref')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'hero_powers': [hero_power.to_dict() for hero_power in self.hero_powers]
        }

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'
    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    strength = db.Column(db.String, nullable=False)

    hero = db.relationship('Hero', backref=db.backref('hero_powers', lazy=True))
    power = db.relationship('Power', backref=db.backref('power_relationship', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'hero_id': self.hero_id,
            'power_id': self.power_id,
            'strength': self.strength,
        }

if __name__ == '__main__':
    app = Flask(__name__)
