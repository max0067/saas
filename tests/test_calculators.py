"""Test fitness calculators."""
import pytest


def test_calculators_page(client):
    """Test calculators page loads."""
    response = client.get('/calculators/')

    assert response.status_code == 200
    assert b'IMC' in response.data or b'BMI' in response.data


def test_bmi_calculator(client):
    """Test BMI calculator."""
    response = client.post('/calculators/', data={
        'weight': 75,
        'height': 180,
        'submit': 'Calculer l\'IMC'
    })

    assert response.status_code == 200
    # BMI should be around 23.1
    assert b'23' in response.data


def test_tdee_calculator(client):
    """Test TDEE calculator."""
    response = client.post('/calculators/', data={
        'weight': 75,
        'height': 180,
        'age': 30,
        'gender': 'male',
        'activity_level': 'moderate',
        'submit-tdee': 'Calculer la TDEE'
    })

    assert response.status_code == 200
    # Should return a TDEE value


def test_onerm_calculator(client):
    """Test 1RM calculator."""
    response = client.post('/calculators/', data={
        'weight': 100,
        'reps': 5,
        'submit-onerm': 'Calculer le 1RM'
    })

    assert response.status_code == 200
    # 1RM should be around 116kg
