"""SEO utilities."""
from flask import Response, url_for
from datetime import datetime
from fitgang_app.models import BlogPost, Product


def generate_sitemap(app):
    """Generate XML sitemap."""
    with app.app_context():
        pages = []

        # Static pages
        static_pages = [
            ('main.index', 'daily', '1.0'),
            ('blog.list', 'daily', '0.9'),
            ('shop.programs', 'daily', '0.9'),
            ('shop.ebooks', 'daily', '0.9'),
            ('calculators.index', 'weekly', '0.7'),
        ]

        for route, changefreq, priority in static_pages:
            try:
                pages.append({
                    'loc': url_for(route, _external=True),
                    'changefreq': changefreq,
                    'priority': priority,
                    'lastmod': datetime.utcnow().strftime('%Y-%m-%d')
                })
            except Exception:
                pass

        # Blog posts
        blog_posts = BlogPost.query.filter_by(is_published=True).all()
        for post in blog_posts:
            pages.append({
                'loc': url_for('blog.post_detail', slug=post.slug, _external=True),
                'changefreq': 'weekly',
                'priority': '0.8',
                'lastmod': post.updated_at.strftime('%Y-%m-%d') if post.updated_at else datetime.utcnow().strftime('%Y-%m-%d')
            })

        # Products
        products = Product.query.filter_by(is_published=True).all()
        for product in products:
            pages.append({
                'loc': url_for('shop.product_detail', slug=product.slug, _external=True),
                'changefreq': 'weekly',
                'priority': '0.9',
                'lastmod': product.updated_at.strftime('%Y-%m-%d') if product.updated_at else datetime.utcnow().strftime('%Y-%m-%d')
            })

        # Generate XML
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

        for page in pages:
            xml += '  <url>\n'
            xml += f'    <loc>{page["loc"]}</loc>\n'
            xml += f'    <changefreq>{page["changefreq"]}</changefreq>\n'
            xml += f'    <priority>{page["priority"]}</priority>\n'
            xml += f'    <lastmod>{page["lastmod"]}</lastmod>\n'
            xml += '  </url>\n'

        xml += '</urlset>'

        return Response(xml, mimetype='application/xml')
