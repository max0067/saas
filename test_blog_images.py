#!/usr/bin/env python3
"""
Test pour diagnostiquer pourquoi les images du blog ne s'affichent pas.
Usage: python3 test_blog_images.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from fitgang_app import db
from fitgang_app.models.blog import BlogPost

app = create_app('production')

with app.app_context():
    print("=" * 70)
    print("DIAGNOSTIC IMAGES BLOG")
    print("=" * 70)

    posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.published_at.desc()).all()

    if not posts:
        print("\n❌ Aucun article publié trouvé!")
        sys.exit(1)

    print(f"\n📊 {len(posts)} article(s) publié(s) trouvé(s)\n")

    for i, post in enumerate(posts, 1):
        print(f"\n{i}. {post.title}")
        print(f"   Slug: {post.slug}")
        print(f"   Featured Image: {repr(post.featured_image)}")

        if post.featured_image is None:
            print(f"   ❌ PAS D'IMAGE (None)")
            print(f"   → Solution: Édite l'article et uploade une image")

        elif post.featured_image == '':
            print(f"   ❌ PAS D'IMAGE (chaîne vide)")
            print(f"   → Solution: Édite l'article et uploade une image")

        elif post.featured_image.startswith('http'):
            print(f"   🌐 URL EXTERNE")
            print(f"   → L'image sera chargée depuis: {post.featured_image}")
            # Tester si l'URL est accessible
            import urllib.request
            try:
                urllib.request.urlopen(post.featured_image, timeout=5)
                print(f"   ✅ URL accessible")
            except Exception as e:
                print(f"   ❌ URL INACCESSIBLE: {e}")

        else:
            print(f"   📁 FICHIER LOCAL")
            print(f"   → Chemin relatif: {post.featured_image}")
            print(f"   → URL sera: /uploads/{post.featured_image}")

            # Vérifier si le fichier existe
            upload_folder = app.config['UPLOAD_FOLDER']
            file_path = os.path.join(upload_folder, post.featured_image)
            print(f"   → Chemin absolu: {file_path}")

            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"   ✅ Fichier existe ({file_size} bytes)")
            else:
                print(f"   ❌ FICHIER INTROUVABLE!")
                print(f"   → Solution: Réuploader l'image via /admin/blog/{post.id}/edit")

    print("\n" + "=" * 70)
    print("RÉSUMÉ")
    print("=" * 70)

    with_images = [p for p in posts if p.featured_image]
    without_images = [p for p in posts if not p.featured_image]

    print(f"\n✅ Avec image: {len(with_images)}")
    print(f"❌ Sans image: {len(without_images)}")

    if without_images:
        print(f"\n📝 Articles sans image:")
        for p in without_images:
            print(f"   - {p.title} (#{p.id})")
            print(f"     → https://fitgang.fr/admin/blog/{p.id}/edit")
