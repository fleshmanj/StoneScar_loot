from flask_wtf import FlaskForm, Form
from wtforms import SelectField
from constants import BOSS_DROPS


class ReserveLootForm(FlaskForm):
    boss = SelectField(u'Boss', choices=[("", "Select a boss")] + [(key, key) for key in BOSS_DROPS.keys()])
    item = SelectField(u'Item', choices=[])
    difficulty = SelectField(u'Difficulty', choices=[('normal', 'Normal'), ('heroic', 'Heroic'), ('mythic', 'Mythic')])
