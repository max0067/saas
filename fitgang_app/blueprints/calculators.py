"""Calculators blueprint."""
from flask import Blueprint, render_template, flash
from fitgang_app.forms.calculators import BMIForm, TDEEForm, MacrosForm, OneRMForm

calculators_bp = Blueprint('calculators', __name__)


@calculators_bp.route('/', methods=['GET', 'POST'])
def index():
    """Fitness calculators."""
    bmi_form = BMIForm()
    tdee_form = TDEEForm()
    macros_form = MacrosForm()
    onerm_form = OneRMForm()

    bmi_result = None
    tdee_result = None
    macros_result = None
    onerm_result = None

    if bmi_form.validate_on_submit() and bmi_form.submit.data:
        height_m = bmi_form.height.data / 100
        bmi = bmi_form.weight.data / (height_m ** 2)
        bmi_result = {'bmi': round(bmi, 2)}

        if bmi < 18.5:
            bmi_result['category'] = 'Insuffisance pondérale'
        elif bmi < 25:
            bmi_result['category'] = 'Poids normal'
        elif bmi < 30:
            bmi_result['category'] = 'Surpoids'
        else:
            bmi_result['category'] = 'Obésité'

    if tdee_form.validate_on_submit() and tdee_form.submit.data:
        # Calculate BMR using Mifflin-St Jeor equation
        if tdee_form.gender.data == 'male':
            bmr = 10 * tdee_form.weight.data + 6.25 * tdee_form.height.data - 5 * tdee_form.age.data + 5
        else:
            bmr = 10 * tdee_form.weight.data + 6.25 * tdee_form.height.data - 5 * tdee_form.age.data - 161

        # Activity multipliers
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }

        tdee = bmr * activity_multipliers[tdee_form.activity_level.data]
        tdee_result = {
            'bmr': round(bmr),
            'tdee': round(tdee),
            'cutting': round(tdee - 500),
            'bulking': round(tdee + 500)
        }

    if macros_form.validate_on_submit() and macros_form.submit.data:
        calories = macros_form.calories.data

        # Macro ratios based on goals
        macro_ratios = {
            'lose': {'protein': 0.35, 'carbs': 0.35, 'fat': 0.30},
            'maintain': {'protein': 0.30, 'carbs': 0.40, 'fat': 0.30},
            'gain': {'protein': 0.30, 'carbs': 0.50, 'fat': 0.20}
        }

        # Adjust for diet type
        if macros_form.diet_type.data == 'low_carb':
            macro_ratios[macros_form.goal.data] = {'protein': 0.40, 'carbs': 0.20, 'fat': 0.40}
        elif macros_form.diet_type.data == 'high_protein':
            macro_ratios[macros_form.goal.data] = {'protein': 0.40, 'carbs': 0.35, 'fat': 0.25}
        elif macros_form.diet_type.data == 'keto':
            macro_ratios[macros_form.goal.data] = {'protein': 0.30, 'carbs': 0.05, 'fat': 0.65}

        ratios = macro_ratios[macros_form.goal.data]

        macros_result = {
            'protein_g': round((calories * ratios['protein']) / 4),
            'carbs_g': round((calories * ratios['carbs']) / 4),
            'fat_g': round((calories * ratios['fat']) / 9)
        }

    if onerm_form.validate_on_submit() and onerm_form.submit.data:
        # Epley formula
        onerm = onerm_form.weight.data * (1 + onerm_form.reps.data / 30)
        onerm_result = {
            'onerm': round(onerm, 1),
            'percentages': {
                '95%': round(onerm * 0.95, 1),
                '90%': round(onerm * 0.90, 1),
                '85%': round(onerm * 0.85, 1),
                '80%': round(onerm * 0.80, 1),
                '75%': round(onerm * 0.75, 1),
                '70%': round(onerm * 0.70, 1)
            }
        }

    return render_template(
        'calculators/index.html',
        bmi_form=bmi_form,
        tdee_form=tdee_form,
        macros_form=macros_form,
        onerm_form=onerm_form,
        bmi_result=bmi_result,
        tdee_result=tdee_result,
        macros_result=macros_result,
        onerm_result=onerm_result
    )
