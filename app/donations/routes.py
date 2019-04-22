from flask import render_template, request, current_app, request, g, url_for, flash, redirect
from .. import db
from app.models import User, Donation, DonationReason, DonationComments, DonationUpdates, Rewards
from sqlalchemy.sql import func
from flask_bootstrap import Bootstrap
import secrets
from sqlalchemy.sql import func
from flask_login import login_user, current_user, logout_user, login_required
from app.donations.forms import AmountForm, DonationReasonForm, DonationCommentForm, DonationUpdateForm
from app.main.forms import SearchForm
from app.donations.utils import save_picture
import stripe
from datetime import datetime
from app.donations import bp

@bp.route("/Donations/<int:id>",  methods=['GET', 'POST'])
@login_required
def create_donation(id):
    user = User.query.get_or_404(id)
    form = DonationReasonForm()
    if form.validate_on_submit():
      picture_file = save_picture(form.picture.data)
      donationreason = DonationReason(image_file=picture_file,
                          category=form.category.data,
                          title=form.title.data,
                          description=form.description.data,
                          short=form.short.data,
                          goal=form.goal.data,
                          amount_prefilled=form.amount_prefilled.data,
                          target_amount=form.target_amount.data,
                          end_method=form.end_method.data,
                          link=form.link.data,
                          country=form.country.data,
                          address=form.address.data,
                          start_date=form.start_date.data,
                          end_date=form.end_date.data,
                          Protagonist=user)
      db.session.add(donationreason)
      db.session.commit()
      random_hex = secrets.token_hex(8)
      rewards = Rewards(points=6, action="Donation Post Created",
                        address=random_hex, Protagonist=current_user)
      db.session.add(rewards)
      db.session.commit()
      flash('Your Donation  has been published.', 'success')
      return redirect(url_for('donation.donation_view'))
    return render_template('donations/create_donation.html', title='New Donation',
                           form=form, legend='Ask For Donation')

pub_key = 'pk_test_fd7KSTfZFHdU4HkhmuD7NGPh'
pub_secret_key = 'sk_test_uJGFiTYHJCvBSbXPftuCd30H'


stripe.api_key = pub_secret_key


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        g.search_form = SearchForm()
        db.session.commit()

@bp.route("/donation/<int:donationreason_id>",  methods=['GET', 'POST'])
def donation(donationreason_id):
    donationreason = DonationReason.query.get_or_404(donationreason_id)
    form = AmountForm()
    if form.validate_on_submit():
    	donation = Donation(amount=form.amount.data,
                          donationreason=donationreason,
                          Protagonist=current_user._get_current_object() )
    	db.session.add(donation)
    	db.session.commit()
    	return redirect(url_for('donation.pay',  donationreason_id=donationreason.id))
    return render_template('donations/donation.html',  donationreasons=[donationreason], donationreason=donationreason, form=form,
                            	 legend= donationreason.Protagonist.username, current_time=datetime.utcnow() )


@bp.route("/donationn/<int:donationreason_id>",  methods=['GET', 'POST'])
def donationn(donationreason_id):
    donationreason = DonationReason.query.get_or_404(donationreason_id)
    donation = db.session.query(func.sum(Donation.amount)).filter(
        Donation.donation_id == donationreason_id).scalar()
    donations = Donation.query.filter_by(donation_id=donationreason_id).order_by(Donation.time_created.desc())
    donationcomments = DonationComments
    form = DonationCommentForm()
    if form.validate_on_submit():
        donationcomments = DonationComments(body=form.body.data,
                          donationreason=donationreason,
                          Protagonist=current_user._get_current_object())
        db.session.add(donationcomments)
        db.session.commit()
        return redirect(request.referrer)
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (donationreason.donationcomments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = donationreason.donationcomments.order_by(DonationComments.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    donationcomment = pagination.items

    donationupdates = DonationUpdates
    form2 = DonationUpdateForm()
    if form2.validate_on_submit():
        donationupdates = DonationUpdates(body=form2.body.data,
                                            donationreason=donationreason,
                                            Protagonist=current_user._get_current_object())
        db.session.add(donationupdates)
        db.session.commit()
        return redirect(request.referrer)
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (donationreason.updates.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = donationreason.updates.order_by(DonationUpdates.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    donationupdate = pagination.items

    return render_template('donations/donationn.html', donationreason=donationreason, current_time=datetime.utcnow(), donation=donation, donationcomment=donationcomment, donations=donations, form=form, form2=form2, donationupdate=donationupdate)

@bp.route("/donation_view", methods=['GET', 'POST'])
def donation_view():
        donationreason = DonationReason.query.order_by(DonationReason.end_date.desc())
        donation = db.session.query(func.sum(Donation.amount)).filter(
            Donation.donation_id == DonationReason.id).scalar()
        tota = db.session.query(func.sum(Donation.amount)).scalar()
        donations = Donation.query.order_by(Donation.time_created.desc())
        return render_template('donations/donationview.html', donationreason=donationreason, current_time=datetime.utcnow(), title='Donations', donation=donation, float=float, donations=donations, tota=tota)

@bp.route("/pay/<int:donationreason_id>", methods=['GET', 'POST'])
def pay(donationreason_id):
	donationreason = DonationReason.query.get_or_404(donationreason_id)
	donation = Donation.query.filter_by(donation_id=donationreason_id).first()
	if request.method == 'POST':
		customer = stripe.Customer.create(email= current_user.email, source=request.form['stripeToken'])
		charge = stripe.Charge.create(customer =customer.id, amount = donation.amount, currency = 'usd',description = 'Donation')
		flash('Your donation has been summited, thanks for your contribution ', 'success')
		return redirect(url_for('donation.donation_view'))
	return render_template('donations/pay.html', pub_key=pub_key, donationreason=donationreason, donation=donation)
