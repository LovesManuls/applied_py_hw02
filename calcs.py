

def calc_calorie_norm(weight, height):
    return 10 * weight + 6.25 * height

def calc_base_water_norm(weight, activity):
    return weight * 30 + int(activity) * 300

def calc_today_water_norm(base_norm, temp):
    if temp > 25:
        return base_norm + 500
    else:
        return base_norm