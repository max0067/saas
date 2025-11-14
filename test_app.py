#!/usr/bin/env python3
"""Test if the Flask app loads correctly."""
import sys
sys.path.insert(0, '/home/user/saas')

try:
    from fitgang_app import create_app
    app = create_app('production')

    print("✓ Application créée avec succès")
    print(f"✓ Nom: {app.name}")
    print(f"✓ Config: {app.config['SITE_NAME']}")

    # List all routes
    print("\nRoutes enregistrées:")
    for rule in app.url_map.iter_rules():
        if 'test' in str(rule):
            print(f"  ✓ {rule}")

    # Test the route
    with app.test_client() as client:
        response = client.get('/test-update')
        print(f"\n✓ Test /test-update: {response.status_code}")
        if response.status_code == 200:
            print("  ✓ La route fonctionne!")
        else:
            print(f"  ✗ Erreur: {response.status_code}")

except Exception as e:
    print(f"✗ Erreur: {e}")
    import traceback
    traceback.print_exc()
