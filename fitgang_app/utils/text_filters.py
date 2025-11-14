"""Custom Jinja2 template filters for text formatting."""
import re
from markupsafe import Markup


def nl2br(text):
    """Convert newlines to <br> tags."""
    if not text:
        return ''
    return Markup(text.replace('\n', '<br>\n'))


def auto_paragraphs(text):
    """
    Automatically convert double newlines to paragraphs.
    If the text already contains HTML tags, leave it as is.
    """
    if not text:
        return ''

    # Si le texte contient déjà des balises HTML, on le retourne tel quel
    if bool(re.search(r'<[^>]+>', text)):
        return Markup(text)

    # Sinon, on convertit les doubles sauts de ligne en paragraphes
    # 1. Nettoyer les espaces en début/fin
    text = text.strip()

    # 2. Séparer par doubles sauts de ligne (ou plus)
    paragraphs = re.split(r'\n\s*\n', text)

    # 3. Nettoyer chaque paragraphe et l'entourer de <p></p>
    formatted_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if p:
            # Convertir les sauts de ligne simples en <br>
            p = p.replace('\n', '<br>\n')
            formatted_paragraphs.append(f'<p>{p}</p>')

    return Markup('\n\n'.join(formatted_paragraphs))


def smart_content(text):
    """
    Smart content formatter:
    - If HTML detected: return as-is
    - If plain text: convert to paragraphs with proper formatting
    """
    if not text:
        return ''

    text = text.strip()

    # Détecter si c'est du HTML (présence de balises)
    has_html = bool(re.search(r'<(p|div|h[1-6]|ul|ol|li|br|strong|em|a|img)[^>]*>', text, re.IGNORECASE))

    if has_html:
        # C'est déjà du HTML, on retourne tel quel
        return Markup(text)

    # C'est du texte brut, on le convertit intelligemment
    # 1. Séparer par doubles sauts de ligne
    blocks = re.split(r'\n\s*\n+', text)

    formatted_blocks = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Détecter les titres (lignes courtes qui se terminent par :)
        if len(block) < 100 and (block.endswith(':') or block.isupper()):
            # C'est probablement un titre
            if len(block) < 50:
                formatted_blocks.append(f'<h2>{block}</h2>')
            else:
                formatted_blocks.append(f'<h3>{block}</h3>')
        # Détecter les listes (lignes qui commencent par -, *, •, ou chiffre.)
        elif re.match(r'^[\-\*•]\s', block) or re.match(r'^\d+\.\s', block):
            lines = block.split('\n')
            is_ordered = bool(re.match(r'^\d+\.', lines[0]))
            tag = 'ol' if is_ordered else 'ul'

            items = []
            for line in lines:
                # Enlever le marqueur de liste
                line = re.sub(r'^[\-\*•]\s*', '', line)
                line = re.sub(r'^\d+\.\s*', '', line)
                if line.strip():
                    items.append(f'<li>{line.strip()}</li>')

            formatted_blocks.append(f'<{tag}>\n' + '\n'.join(items) + f'\n</{tag}>')
        else:
            # C'est un paragraphe normal
            # Convertir les sauts de ligne simples en <br>
            block = block.replace('\n', '<br>\n')
            formatted_blocks.append(f'<p>{block}</p>')

    return Markup('\n\n'.join(formatted_blocks))


def register_filters(app):
    """Register custom filters with Flask app."""
    app.jinja_env.filters['nl2br'] = nl2br
    app.jinja_env.filters['auto_paragraphs'] = auto_paragraphs
    app.jinja_env.filters['smart_content'] = smart_content
