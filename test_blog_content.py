#!/usr/bin/env python3
"""
Test pour voir le contenu d'un article de blog et tester le filtre smart_content.
Usage: python3 test_blog_content.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from fitgang_app import db
from fitgang_app.models.blog import BlogPost
from fitgang_app.utils.text_filters import smart_content

app = create_app('production')

with app.app_context():
    # Chercher l'article "programme-seche-les-secrets-pour-reussir"
    post = BlogPost.query.filter_by(slug='programme-seche-les-secrets-pour-reussir').first()

    if not post:
        print("❌ Article 'programme-seche-les-secrets-pour-reussir' introuvable!")
        print("\n📋 Articles disponibles:")
        posts = BlogPost.query.all()
        for p in posts:
            print(f"   - {p.slug}")
        sys.exit(1)

    print("=" * 70)
    print("ARTICLE TROUVÉ")
    print("=" * 70)
    print(f"\nTitre: {post.title}")
    print(f"Slug: {post.slug}")
    print(f"Published: {post.is_published}")
    print(f"Featured Image: {post.featured_image}")

    print("\n" + "=" * 70)
    print("CONTENU BRUT (premiers 500 caractères)")
    print("=" * 70)
    print(post.content[:500] if post.content else "VIDE")

    print("\n" + "=" * 70)
    print("CONTENU APRÈS FILTRE smart_content (premiers 500 caractères)")
    print("=" * 70)
    formatted = smart_content(post.content)
    print(str(formatted)[:500])

    print("\n" + "=" * 70)
    print("DÉTECTION")
    print("=" * 70)

    # Détecter si c'est du HTML ou du texte brut
    import re
    has_html = bool(re.search(r'<(p|div|h[1-6]|ul|ol|li|br|strong|em|a|img)[^>]*>', post.content or '', re.IGNORECASE))

    if has_html:
        print("✅ Le contenu contient déjà du HTML")
        print("   → Le filtre smart_content le retournera tel quel")
    else:
        print("❌ Le contenu est du TEXTE BRUT")
        print("   → Le filtre smart_content va le convertir en HTML")

    print("\n" + "=" * 70)
    print("STRUCTURE DU CONTENU")
    print("=" * 70)

    lines = (post.content or '').split('\n')
    print(f"Nombre de lignes: {len(lines)}")
    print(f"Nombre de doubles sauts de ligne: {post.content.count(chr(10) + chr(10)) if post.content else 0}")

    # Afficher les 10 premières lignes
    print("\n📝 Premières lignes:")
    for i, line in enumerate(lines[:10], 1):
        preview = line[:60] + '...' if len(line) > 60 else line
        print(f"   {i:2d}. {repr(preview)}")
