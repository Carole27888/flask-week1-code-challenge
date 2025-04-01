from random import choice as rc
from app import app
from models import db, Hero, Power, HeroPower

if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")

        
        HeroPower.query.delete()
        Power.query.delete()
        Hero.query.delete()

        print("Seeding powers...")
        
        powers = [
            Power(name="super strength", description="Gives the wielder super-human strengths, enabling them to lift immense weights and perform feats of incredible power."),
            Power(name="flight", description="Allows the wielder to fly through the skies at supersonic speed, evading attacks and reaching distant locations quickly."),
            Power(name="super human senses", description="Enables the wielder to use senses at a super-human level, detecting danger and locating enemies with ease."),
            Power(name="elasticity", description="Grants the ability to stretch, bend, and reshape the body to extreme lengths and shapes."),
        ]
        db.session.add_all(powers)

        print("Seeding heroes...")
        
        heroes = [
            Hero(name="Kamala Khan", super_name="Ms. Marvel"),
            Hero(name="Doreen Green", super_name="Squirrel Girl"),
            Hero(name="Gwen Stacy", super_name="Spider-Gwen"),
            Hero(name="Janet Van Dyne", super_name="The Wasp"),
            Hero(name="Wanda Maximoff", super_name="Scarlet Witch"),
            Hero(name="Carol Danvers", super_name="Captain Marvel"),
            Hero(name="Jean Grey", super_name="Dark Phoenix"),
            Hero(name="Ororo Munroe", super_name="Storm"),
            Hero(name="Kitty Pryde", super_name="Shadowcat"),
            Hero(name="Elektra Natchios", super_name="Elektra"),
        ]
        db.session.add_all(heroes)

        print("Adding powers to heroes...")
        
        strengths = ["Strong", "Weak", "Average"]
        hero_powers = []

        
        for hero in heroes:
            power = rc(powers)  
            hero_powers.append(
                HeroPower(hero=hero, power=power, strength=rc(strengths))
            )

       
        db.session.add_all(hero_powers)

       
        db.session.commit()

        print("Done seeding!")
