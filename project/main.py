import time

from flask import Blueprint
from flask_login import login_required, current_user
from flask import request

import json
import pandas as pd

from project import db
from .models import Normal_Raid, Heroic_Raid, Mythic_Raid
from constants import MAX_RESERVATIONS_HARD, LOCK_TIMES

main = Blueprint('main', __name__)

df = pd.read_csv("database.csv")


@main.route('/')
def index():
    return {"msg": "Index"}, 200


@main.route('/reserve/<difficulty>', methods=["POST"])
@login_required
def reserve_loot(difficulty):
    data = json.loads(request.data)
    try:
        if time.gmtime().tm_hour not in LOCK_TIMES:
            if difficulty == "normal":
                check_reserved = Normal_Raid.query.filter_by(user=current_user.name, boss=data["boss"],
                                                             item=data["item"]).count()
                if check_reserved == 0:
                    reservation = Normal_Raid(user=current_user.name, boss=data["boss"], item=data["item"])
                    records = Normal_Raid.query.filter_by(user=reservation.user).count()
                    if records < MAX_RESERVATIONS_HARD:
                        db.session.add(reservation)
                        db.session.commit()
                        return {"msg": "Reservation for Normal item made"}, 200
                    else:
                        return {"msg": "Reached max reservations"}, 200
                else:
                    return {"msg": "Item is already reserved"}, 200
            elif difficulty == "heroic":
                check_reserved = Heroic_Raid.query.filter_by(user=current_user.name, boss=data["boss"],
                                                             item=data["item"]).count()
                if check_reserved == 0:
                    reservation = Heroic_Raid(user=current_user.name, boss=data["boss"], item=data["item"])
                    records = Heroic_Raid.query.filter_by(user=reservation.user).count()
                    if records < MAX_RESERVATIONS_HARD:
                        db.session.add(reservation)
                        db.session.commit()
                        return {"msg": "Reservation for Heroic item made"}, 200
                    else:
                        return {"msg": "Reached max reservations"}, 200
                else:
                    return {"msg": "Item is already reserved"}, 200
            elif difficulty == "mythic":
                check_reserved = Mythic_Raid.query.filter_by(user=current_user.name, boss=data["boss"],
                                                             item=data["item"]).count()
                if check_reserved == 0:
                    reservation = Mythic_Raid(user=current_user.name, boss=data["boss"], item=data["item"])
                    records = Mythic_Raid.query.filter_by(user=reservation.user).count()
                    if records < MAX_RESERVATIONS_HARD:
                        db.session.add(reservation)
                        db.session.commit()
                        return {"msg": "Reservation for Mythic item made"}, 200
                    else:
                        return {"msg": "Reached max reservations"}, 200
                else:
                    return {"msg": "Item is already reserved"}, 200
        else:
            return {"msg": "Loot reservations are locked until 05:00 UTC"}, 200
    except:
        return {"msg": "Wrong JSON data or endpoint"}, 200


@main.route('/remove/<difficulty>', methods=["POST"])
@login_required
def remove_reservation(difficulty):
    if time.gmtime().tm_hour not in LOCK_TIMES:
        if difficulty == "normal":
            data = json.loads(request.data)
            db.session.query(Normal_Raid).filter(Normal_Raid.item == data["item"],
                                                 Normal_Raid.boss == data["boss"],
                                                 Normal_Raid.user == current_user.name).delete()
            db.session.commit()
            return {"msg": "Item Successfully removed"}, 200
        elif difficulty == "heroic":
            data = json.loads(request.data)
            db.session.query(Heroic_Raid).filter(Heroic_Raid.item == data["item"],
                                                 Heroic_Raid.boss == data["boss"],
                                                 Heroic_Raid.user == current_user.name).delete()
            db.session.commit()
            return {"msg": "Item Successfully removed"}, 200
        elif difficulty == "mythic":
            data = json.loads(request.data)
            db.session.query(Mythic_Raid).filter(Mythic_Raid.item == data["item"],
                                                 Mythic_Raid.boss == data["boss"],
                                                 Mythic_Raid.user == current_user.name).delete()
            db.session.commit()
            return {"msg": "Item Successfully removed"}, 200
        else:
            return {"msg": "Error: did you input the correct difficulty?"}, 200
    else:
        return {"msg": "Loot reservations are locked until 05:00 UTC"}, 200


@main.route('/reserved/<difficulty>/<boss>', methods=["GET"])
@login_required
def show_reserved(difficulty, boss):
    if request.method == "GET":
        if difficulty == "normal":
            reserved = Normal_Raid.query.filter_by(boss=boss)
            payload = {}
            for record in reserved:
                payload[record.id] = {"user": record.user,
                                      "item": record.item}
            return payload, 200
        elif difficulty == "heroic":
            reserved = Heroic_Raid.query.filter_by(boss=boss)
            payload = {}
            for record in reserved:
                payload[record.id] = {"user": record.user,
                                      "item": record.item}
            return payload, 200
        elif difficulty == "mythic":
            reserved = Mythic_Raid.query.filter_by(boss=boss)
            payload = {}
            for record in reserved:
                payload[record.id] = {"user": record.user,
                                      "item": record.item}
            return payload, 200

        else:
            return "failure", 400