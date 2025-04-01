from sqlalchemy.exc import IntegrityError
from flask import Flask, request, jsonify

from flask_migrate import Migrate
from models import db, Hero, HeroPower, Power

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db.init_app(app)
migrate = Migrate(app, db)




@app.route('/add_hero', methods=['POST'])      
def add_hero():
    data = request.get_json()
    name = data.get('name')
    super_name = data.get('super_name')

    existing_hero = Hero.query.filter_by(name=name).first()
    if existing_hero:
        return jsonify({'error': 'Hero already exists'}), 400

    new_hero = Hero(name=name, super_name=super_name)
    db.session.add(new_hero)
    
    try:
        db.session.commit()
        return jsonify(new_hero.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Super name already exists'}), 400
    

@app.route('/add_power', methods=['POST'])
def add_power():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if len(description) <20:
        return jsonify({'error': 'Description must be at least 20 characters'}), 400
    
    existing_power = Power.query.filter_by(name=name).first()
    if existing_power:
        return jsonify({'error': 'Power already exists'}), 400
    
    new_power = Power(name=name, description=description)
    db.session.add(new_power)

    try:
        db.session.commit()
        return jsonify(new_power.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Power already exists'}), 400
    

@app.route('/remove_power', methods=['POST'])
def remove_power():
    data = request.get_json()
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')

    hero_power = HeroPower.query.filter_by(hero_id=hero_id, power_id=power_id).first()
    if not hero_power:
        return jsonify({'error': 'Power not assigned to hero'}), 404

    db.session.delete(hero_power)
    db.session.commit()
    return jsonify({"message": f"Power removed from hero."}), 200

@app.route('/hero_powers', methods=['POST'])
def assign_power():
    data = request.get_json()
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')
    strength = data.get('strength')

    if strength not in ['strong', 'weak', 'average']:
        return jsonify({'error': 'Invalid strength'}), 400
    
    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if not hero:
        return jsonify({'error': 'Hero not found'}), 404
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    
    hero_power = HeroPower(hero_id=hero_id, power_id=power_id, strength=strength)
    db.session.add(hero_power)

    try:
        db.session.commit()
        return jsonify(hero_power.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'errors': ['Validation errors']}), 400



@app.route('/heroes', methods = ['GET'])  
def get_heroes():
    heroes = Hero.query.all()
    heroes_list = [hero.to_dict() for hero in heroes]
    return jsonify(heroes_list), 200

@app.route('/powers', methods = ['GET'])
def get_powers():
    powers = Power.query.all()
    powers_list = [power.to_dict() for power in powers]
    return jsonify(powers_list), 200

@app.route('/hero/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        return jsonify(hero.to_dict()), 200
    else:
        return jsonify({'error': 'Hero not found'}), 404
    

@app.route('/power/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power:
        return jsonify(power.to_dict()), 200
    else:
        return jsonify({'error': 'Power not found'}), 404
    
@app.route('/power/<int:id>', methods=['PATCH'])
def update_power(id):
    data = request.get_json()
    description = data.get('description')

    if len (description) < 20:
        return jsonify({'error': 'Description must be at least 20 characters long'}), 400
    power = Power.query.get(id)
    if power:
        power.description = description
        db.session.commit()
        return jsonify(power.to_dict()), 200
    else:
        return jsonify({'error': 'Power not found'}), 404
    
if __name__ == '__main__':
    app.run(debug=True)