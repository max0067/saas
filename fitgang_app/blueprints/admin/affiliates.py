"""Admin affiliates blueprint."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from fitgang_app import db
from fitgang_app.models import Affiliate
from fitgang_app.utils.decorators import admin_required

admin_affiliates_bp = Blueprint('admin_affiliates', __name__)


@admin_affiliates_bp.route('/')
@admin_required
def index():
    """List affiliates."""
    affiliates = Affiliate.query.order_by(Affiliate.created_at.desc()).all()
    return render_template('admin/affiliates.html', affiliates=affiliates)


@admin_affiliates_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create():
    """Create affiliate."""
    if request.method == 'POST':
        affiliate = Affiliate(
            code=request.form.get('code').upper(),
            name=request.form.get('name'),
            email=request.form.get('email'),
            commission_rate=float(request.form.get('commission_rate', 10))
        )
        db.session.add(affiliate)
        db.session.commit()

        flash('Affilié créé!', 'success')
        return redirect(url_for('admin_affiliates.index'))

    return render_template('admin/affiliate_form.html', title='Créer un affilié')


@admin_affiliates_bp.route('/<int:affiliate_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(affiliate_id):
    """Edit affiliate."""
    affiliate = Affiliate.query.get_or_404(affiliate_id)

    if request.method == 'POST':
        affiliate.code = request.form.get('code').upper()
        affiliate.name = request.form.get('name')
        affiliate.email = request.form.get('email')
        affiliate.commission_rate = float(request.form.get('commission_rate'))

        db.session.commit()
        flash('Affilié mis à jour!', 'success')
        return redirect(url_for('admin_affiliates.index'))

    return render_template('admin/affiliate_form.html', affiliate=affiliate, title='Modifier l\'affilié')


@admin_affiliates_bp.route('/<int:affiliate_id>/toggle', methods=['POST'])
@admin_required
def toggle_active(affiliate_id):
    """Toggle affiliate status."""
    affiliate = Affiliate.query.get_or_404(affiliate_id)
    affiliate.is_active = not affiliate.is_active
    db.session.commit()

    status = 'activé' if affiliate.is_active else 'désactivé'
    flash(f'Affilié {affiliate.name} {status}.', 'success')
    return redirect(url_for('admin_affiliates.index'))
