"""Calculators blueprint."""
from flask import Blueprint, render_template, request

calculators_bp = Blueprint('calculators', __name__)


@calculators_bp.route('/', methods=['GET', 'POST'])
def index():
    """Fitness calculators."""
    bmi_result = None
    tdee_result = None

    if request.method == 'POST':
        calc_type = request.form.get('calc_type')

        if calc_type == 'bmi':
            try:
                weight = float(request.form.get('weight', 0))
                height = float(request.form.get('height', 0))

                if weight > 0 and height > 0:
                    height_m = height / 100
                    bmi = weight / (height_m ** 2)
                    bmi_result = {'bmi': round(bmi, 2)}

                    if bmi < 18.5:
                        bmi_result['category'] = 'Insuffisance pondérale'
                    elif bmi < 25:
                        bmi_result['category'] = 'Poids normal'
                    elif bmi < 30:
                        bmi_result['category'] = 'Surpoids'
                    else:
                        bmi_result['category'] = 'Obésité'
            except (ValueError, TypeError):
                pass

        elif calc_type == 'tdee':
            try:
                weight = float(request.form.get('weight', 0))
                height = float(request.form.get('height', 0))
                age = int(request.form.get('age', 0))
                gender = request.form.get('gender', 'male')
                activity = request.form.get('activity', 'sedentary')

                if weight > 0 and height > 0 and age > 0:
                    # Calculate BMR using Mifflin-St Jeor equation
                    if gender == 'male':
                        bmr = 10 * weight + 6.25 * height - 5 * age + 5
                    else:
                        bmr = 10 * weight + 6.25 * height - 5 * age - 161

                    # Activity multipliers
                    activity_multipliers = {
                        'sedentary': 1.2,
                        'light': 1.375,
                        'moderate': 1.55,
                        'active': 1.725,
                        'extra': 1.9
                    }

                    tdee = bmr * activity_multipliers.get(activity, 1.2)
                    tdee_result = {
                        'bmr': round(bmr),
                        'tdee': round(tdee),
                        'cutting': round(tdee - 500),
                        'bulking': round(tdee + 500)
                    }
            except (ValueError, TypeError):
                pass

    return render_template(
        'calculators/index.html',
        bmi_result=bmi_result,
        tdee_result=tdee_result
    )
