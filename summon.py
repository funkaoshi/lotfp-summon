import random
from flask import flash, request, render_template, Flask

from dice import d
from monster import Monster
import tables


app = Flask(__name__)
app.config.from_prefixed_env()


def get_save_vs_magic(level):
    """
    Return the saving throw value of a magic user depending on his level.
    """
    if 1 <= level <= 5:
        return 14
    elif 6 <= level <= 10:
        return 12
    elif 11 <= level <= 15:
        return 8
    elif 16 <= level <= 18:
        return 6
    else:
        return 4

def get_domination_result(level, bonuses, monster):
    while True:
        caster_roll = level + bonuses + d(20)
        monster_roll = monster.domination_roll()
        result = caster_roll - monster_roll
        if result != 0:
            break
    rounds = 0
    if result >= 19 or result >= 2 * monster.domination_margin:
        margin = 'massive'
        domination = "<b>Holy shit!</b> You now own a pet demon. Use it for good."
    elif result >= monster.domination_margin:
        margin = 'great'
        domination = "You may demand a term of service from the creature without needing to consciously direct it. The details of this service must be communicated in a clear and succinct manner. This is your chance! <b>Don't fuck it up.</b>"
    elif result >= 1:
        margin = 'normal'
        rounds = d(10)
        domination = "If you concentrate you can control the monster for %d rounds." % rounds
    elif result > -monster.domination_margin:
        margin = 'normal'
        rounds = max(d(10) * -result, monster.hd)
        domination = "This thing is here and it's angry. You're going to have to deal with it trying to kill you for %d rounds." % rounds
    elif result > -19 or result > 2 * monster.domination_margin:
        margin = 'great'
        domination = "I can tell you, it's not going to be good. <blockquote><p>%s</p></blockquote>" % random.choice(tables.DOMINATION_FAILURES)
    else:
        margin = 'massive'
        if d(20) == 20:
            domination = "<b>You son of a bitch.</b> It's basically raining demons right now. There are hundreds of them. You're fucked."
        else:
            monster.hd = monster.hd * (d(4) + 1)
            domination = "This thing is here and it's not going anywhere. It's going to try and kill your ass right now."
    return {
        'caster': caster_roll,
        'monster': monster_roll,
        'margin': margin,
        'won': caster_roll > monster_roll,
        'domination': domination,
        'rounds': rounds,
    }

def cast_summon(level, monster_hd, bonuses):
    result = {}
    # Can you even summon this thing?
    if monster_hd > level * 2:
        result['ignored'] = True
        return result
    # Make initial saving throw
    result['save'] = get_save_vs_magic(level)
    result['save_roll'] = d(20)
    result['saved'] = result['save_roll'] >= result['save']
    # Create monster
    result['monster'] = Monster(monster_hd, result['saved'])
    if not result['monster'].is_abstract_form:
        # Domination rolls
        result['domination'] = get_domination_result(level, bonuses, result['monster'])
    return result

def get_params(request):
    default = (True, 1, 2, 0)
    try:
        level = int(request.form.get('level', 1))
        monster_hd = int(request.form.get('monster-hd', 2))
        bonuses = int(request.form.get('bonuses', 0))
    except (ValueError, TypeError):
        flash("Try entering some valid numbers", "error")
        return default
    if level < 1 or bonuses < 0 or monster_hd < 0:
        flash("These numbers should be positive", "error")
        return default
    return False, level, monster_hd, bonuses

@app.route('/', methods=['GET', 'POST'])
def summon():
    errors, level, monster_hd, bonuses = get_params(request)
    if not errors and request.method == 'POST':
        result = cast_summon(level, monster_hd, bonuses)
    else:
        result = None

    return render_template("index.html", result=result,
            level=level, monster_hd=monster_hd, bonuses=bonuses)

if __name__ == '__main__':
    app.run("0.0.0.0")
