from flask import render_template, url_for, flash, redirect, request, g
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from datetime import datetime
import secrets
from sqlalchemy.sql import func
from app.users import bp
from app.models import (User, Post, Follow, Role, Permission, Address, Occupation, Links, Intrest, Donation, SponsorshipRequest, Sponsorship, Events, EventsIntrest, Achievement, Campaign, DonationReason,  Travel, Special_event, Media, Rewards,
                        PostLike, CommentLike, BlogLike, DonationReason, Blog, Bio, BlogCommentLike, Sports, BrandBrief, Campaign, SocialDash, Update, UpdateComment,  UpdateLike, UpdateCommentLike, EventsFAQ)
from app.users.forms import (UpdateAccountForm, AchievementForm, EventsForm, TravelForm, Special_eventForm, FAQForm, SocialDashForm,
                             AddressForm, OccupationForm, BioForm, BrandBriefForm, LinksForm, IntrestForm, MediaForm, UpdateBrandRoleForm, UpdateAccountRoleForm,  UpdateBrandAccountForm, SportsForm, UpdateForm, UpdateCommentForm)
from app.users.utils import save_picture
from app.users.utils1 import save_pic
from app.users.utils2 import save_pics
from app.main.forms import SearchForm
from .email import send_verify_email
from .phone import send_verify_msg


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        g.search_form = SearchForm()
        db.session.commit()


@bp.route("/roleupdatebrands/<int:id>", methods=['GET', 'POST'])
@login_required
def roleupdatebrands(id):
    flash('please fill in all this details to get eligible for Brands Role','warning')
    user = User.query.get_or_404(id)
    form = UpdateBrandAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user.image_file = picture_file
        user.username = form.username.data
        user.email = form.email.data
        user.brand_name = form.brand_name.data
        user.company_name = form.company_name.data
        user.about_me = form.about_me.data
        user.web_url = form.web_url.data
        user.available_for_sponsorship = form.available_for_sponsorship.data
        user.contact_number = form.contact_number.data

        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main.role2'))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.brand_name.data = user.brand_name
        form.company_name.data = user.company_name
        form.about_me.data = user.about_me
        form.web_url.data = user.web_url
        form.available_for_sponsorship.data = user.available_for_sponsorship
        form.contact_number.data = user.contact_number
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    return render_template('users/account1.html', title='Account', image_file=image_file, form=form, user=user)


@bp.route("/bio/<int:id>", methods=['GET', 'POST'])
@login_required
def bio(id):
    form = BioForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        bio = Bio( goal = form.goal.data,
        hurdles = form.hurdles.data,
        rank = form.rank.data,
        accomplished = form.accomplished.data,
        fear = form.fear.data,
        finance = form.finance.data,
        market = form.market.data,
        other = form.other.data,
        motivate = form.motivate.data,
                                Protagonist=user)
        db.session.add(bio)
        db.session.commit()
        flash('Your bio has been updated sucessfully!', 'success')
        return redirect(url_for('main.role1'))
    return render_template('users/bioform.html', title='Bio', user=user,
                           form=form,)
        


@bp.route("/roleupdatecreators/<int:id>", methods=['GET', 'POST'])
@login_required
def roleupdatecreators(id):
    flash('please fill in all this details to get eligible for Creators Role', "warning")
    user = User.query.get_or_404(id)
    form = UpdateAccountRoleForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user.image_file = picture_file
        user.last_name = form.last_name.data
        user.first_name = form.first_name.data
        user.username = form.username.data
        user.language = form.language.data
        user.category = form.category.data
        user.date_of_birth = form.date_of_birth.data
        user.email = form.email.data
        user.about_me = form.about_me.data
        user.education_level = form.education_level.data
        user.gender = form.gender.data
        user.web_url = form.web_url.data
        user.contact_number = form.contact_number.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.bio', id=user.id))
    elif request.method == 'GET':
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.username.data = user.username
        form.email.data = user.email
        form.language.data = user.language
        form.category.data = user.category
        form.date_of_birth.data = user.date_of_birth
        form.about_me.data = user.about_me
        form.education_level.data = user.education_level
        form.gender.data = user.gender
        form.web_url.data = user.web_url
        form.contact_number.data = user.contact_number

    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    return render_template('users/account2.html', title='Account', image_file=image_file, form=form, user=user)





@bp.route("/account/<int:id>", methods=['GET', 'POST'])
@login_required
def account(id):

    user = User.query.get_or_404(id)
    if current_user.is_role == 'Brand':
        form = UpdateBrandAccountForm()
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                user.image_file = picture_file
            user.username = form.username.data
            user.is_role = form.is_role.data
            user.email = form.email.data
            user.brand_name = form.brand_name.data
            user.company_name = form.company_name.data
            user.about_me= form.about_me.data
            user.web_url = form.web_url.data
            user.available_for_sponsorship = form.available_for_sponsorship.data
            user.contact_number = form.contact_number.data
        
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('users.user', id=user.id))
        elif request.method == 'GET':
            form.username.data = user.username
            form.email.data = user.email
            form.brand_name.data = user.brand_name
            form.company_name.data = user.company_name
            form.is_role.data = user.is_role
            form.about_me.data = user.about_me
            form.web_url.data = user.web_url
            form.available_for_sponsorship.data = user.available_for_sponsorship
            form.contact_number.data = user.contact_number
    else:
        form = UpdateAccountForm()
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                user.image_file = picture_file
            user.last_name = form.last_name.data
            user.first_name = form.first_name.data
            user.username = form.username.data
            user.is_role = form.is_role.data
            user.language = form.language.data
            user.category = form.category.data
            user.date_of_birth = form.date_of_birth.data
            user.email = form.email.data
            user.about_me= form.about_me.data
            user.education_level = form.education_level.data
            user.gender = form.gender.data
            user.web_url = form.web_url.data
            user.contact_number = form.contact_number.data
        
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('users.user', id=user.id))
        elif request.method == 'GET':
            form.first_name.data = user.first_name
            form.last_name.data = user.last_name
            form.username.data = user.username
            form.email.data = user.email
            form.language.data = user.language
            form.category.data = user.category
            form.date_of_birth.data = user.date_of_birth
            form.is_role.data = user.is_role
            form.about_me.data = user.about_me
            form.education_level.data = user.education_level
            form.gender.data = user.gender
            form.web_url.data = user.web_url
            form.contact_number.data = user.contact_number

    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    return render_template('users/account.html', title='Account',image_file=image_file, form=form, user=user)


@bp.route("/address/<int:id>", methods=['GET', 'POST'])
@login_required
def address(id):
    form = AddressForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        address = Address(street=form.street.data,
                    city=form.city.data,
                    zip_code=form.zip_code.data,
                    country=form.country.data,
                    Protagonist= user)
        db.session.add(address)
        db.session.commit()
        flash('Your address has been updated sucessfully!', 'success')
        return redirect(url_for('users.user', id=user.id))
    return render_template('users/address.html', title='Address', user=user,
                           form=form, legend='Address'  )

@bp.route("/brandbrief/<int:id>", methods=['GET', 'POST'])
@login_required
def brandbrief(id):
    form = BrandBriefForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        brandbrief = BrandBrief(business_description=form.business_description.data,
                    brand_psychology=form.brand_psychology.data,
                    current_market_perception=form.current_market_perception.data,
                    brand_goals=form.brand_goals.data,
                    Protagonist= user)
        db.session.add(brandbrief)
        db.session.commit()
        flash('Your brand brief details has been updated successfully!', 'success')
        return redirect(url_for('users.user', id=user.id))
    return render_template('users/brand_brief.html', title='Brand Details',
                           form=form, legend='Brand Details', user=user)

@bp.route("/sports/<int:id>", methods=['GET', 'POST'])
@login_required
def sports(id):
    form = SportsForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        sports = Sports(street=form.street.data,
                    level_of_playing=form.level_of_playing.data,
                    current_team=form.current_team.data,
                    tournament=form.tournament.data,
                    Protagonist= user)
        db.session.add(Sports)
        db.session.commit()
        flash('Your Sports carrier details has been updated successfully!', 'success')
        return redirect(url_for('users.user', id=user.id))
    return render_template('users/sports.html', title='Address', user=user,
                           form=form, legend='Sports carrier' )

@bp.route("/Occupation/<int:id>", methods=['GET', 'POST'])
@login_required
def occupation(id):
    form = OccupationForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        occupation = Occupation(occupation_name=form.occupation_name.data,
                    occupation_company=form.occupation_company.data,
                    occupation_start_date=form.occupation_start_date.data,
                    occupation_end_date=form.occupation_end_date.data,
                    Protagonist= user)
        db.session.add(occupation)
        db.session.commit()
        flash('Your occupation has been updated successfully!', 'success')
        return redirect(url_for('users.user', id=user.id))
    return render_template('users/occupation.html', title='occupation', user=user,
                           form=form, legend='occupation')


@bp.route("/SocialDashboard/<int:id>", methods=['GET', 'POST'])
@login_required
def socialdashboard(id):
    form = SocialDashForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        socialdash = SocialDash(likes=form.likes.data,
                                views=form.views.data,
                                share=form.share.data,
                                comment=form.comment.data,
                                category=form.category.data,
                                engagments=form.engagments.data,
                                Protagonist=user)
        db.session.add(socialdash)
        db.session.commit()
        flash('Your social dash has been updated successfully!', 'success')
        return redirect(url_for('users.user', id=user.id))
    return render_template('users/userdash.html', title='Social Dash', user=user,
                           form=form, legend='Dashboard')

@bp.route("/links/<int:id>", methods=['GET', 'POST'])
@login_required
def links(id):
    form = LinksForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        links = Links(facebook_id=form.facebook_id.data,
                    twitter_id=form.twitter_id.data,
                    instagram_id=form.instagram_id.data,
                    snapchat_id=form.snapchat_id.data,
                    Protagonist= user)
        db.session.add(links)
        db.session.commit()
        flash('Your social links has been updated successfully!', 'success')
        return redirect(url_for('users.user', id=user.id))
    return render_template('users/links.html', title='social links', user=user,
                           form=form, legend='links'  )


@bp.route("/eventsview", methods=['GET', 'POST'])
def view_events():
    page = request.args.get('page', 1, type=int)
    events = Events.query.order_by(Events.event_start_date.desc())
    campaign = Campaign.query.order_by(Campaign.campaign_start_date.desc()).paginate(page=page, per_page=10)

    return render_template('users/events.html', events=events, campaign=campaign,  current_time=datetime.utcnow(), title='Events')


@bp.route("/eventsn/<int:events_id>", methods=['GET', 'POST'])
@login_required
def eventsn(events_id):
    events = Events.query.get_or_404(events_id)
    intrested = EventsIntrest.query.filter_by(
        events_id=events_id).order_by(EventsIntrest.timestamp)
    form = FAQForm()
    if form.validate_on_submit():
        faq = EventsFAQ(que=form.que.data,
                          ans=form.ans.data,
                          events=events,
                          Protagonist=current_user._get_current_object())
        db.session.add(faq)
        db.session.commit()
        flash('Your FAQ has been published.', 'success')
        return redirect(request.referrer)
    bbq = EventsFAQ.query.filter_by(
        events_id=events_id).order_by(EventsFAQ.timestamp.asc())
    return render_template('users/eventsn.html', events=events, form=form, bbq=bbq, intrested=intrested)

@bp.route("/intrest/<int:id>", methods=['GET', 'POST'])
@login_required
def intrest(id):
    form = IntrestForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        intrest = Intrest(intrest_type=form.intrest_type.data,
                    Protagonist= user)
        db.session.add(intrest)
        db.session.commit()
        flash('Your intrest has been updated successfully!', 'success')
        return redirect(url_for('users.user', id=user.id))
    return render_template('users/intrest.html', title='Interest', user=user,
                           form=form, legend='Interest'  )

@bp.route("/achievement/<int:id>", methods=['GET', 'POST'])
@login_required
def achievement(id):
    form = AchievementForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        achievement = Achievement(
                    medal_count=form.medal_count.data,
                    timestamp=form.timestamp.data,
                    Protagonist= user)
        db.session.add(achievement)
        db.session.commit()
        flash('Your Achievement has been updated successfully!', 'success')
        return redirect(url_for('users.user', id=user.id))
    return render_template('users/achievement.html', title='Achievement', user=user,
                           form=form, legend='Achievement'  )

@bp.route("/events/<int:id>", methods=['GET', 'POST'])
@login_required
def events(id):
    form = EventsForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        picture_file = save_pics(form.picture.data)
        events = Events(event_name=form.event_name.data,
                    event_description=form.event_description.data,
                    event_location=form.event_location.data,
                    event_type=form.event_type.data,
                    image_file=picture_file,
                    event_category=form.event_category.data,
                    event_links=form.event_links.data,
                    event_frequency=form.event_frequency.data,
                    event_start_date=form.event_start_date.data,
                    event_end_date=form.event_end_date.data,
                    Protagonist= user)
        db.session.add(events)
        db.session.commit()
        flash('Your Event has been updated successfully!', 'success')
        return redirect(url_for('users.user', id=user.id))
    return render_template('users/event.html', title='Events',
                           form=form, legend='Event'  )
                           

@bp.route("/travel/<int:id>", methods=['GET', 'POST'])
@login_required
def travel(id):
    form =TravelForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        travel = Travel(place=form.place.data,
                    start_date=form.start_date.data,
                    end_date=form.end_date.data,
                    Protagonist= user)
        db.session.add(travel)
        db.session.commit()
        flash('Your Travel designation has been updated successfully!', 'success')
        return redirect(url_for('users.user', id=user.id))
    return render_template('users/travel.html', title='Travel',
                           form=form, legend='Travel'  )

@bp.route("/special_event/<int:id>", methods=['GET', 'POST'])
@login_required
def special_event(id):
    form =Special_eventForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        special_event = Special_event(life_event=form.life_event.data,
                    life_event_start_date=form.life_event_start_date.data,
                    life_event_end_date=form.life_event_end_date.data,
                    Protagonist= user)
        db.session.add(special_event)
        db.session.commit()
        flash('Your Special event n has been updated successfully!', 'success')
        return redirect(url_for('users.user', id=user.id))
    return render_template('users/special_event.html', title='Special event', user=user,
                           form=form, legend='Special event'  )

@bp.route("/media/<int:id>", methods=['GET', 'POST'])
@login_required
def media(id):
    form =MediaForm()
    if form.validate_on_submit():
        user = User.query.get_or_404(id)
        picture_file = save_picture(form.image.data)
        media = media(

                     media_name = picture_file,
                    media_format=form.media_format.data,
                    Protagonist= user)
        db.session.add(media)
        db.session.commit()
        media_name = url_for('static', filename='pictures/' + user.media_name)
        flash('Your  image  has been updated successfully!', 'success')
        return redirect(url_for('users.user', id=user.id))
    return render_template('users/media.html', title='upload',
                            form=form, legend='Add image '  )






@bp.route("/user/<int:id>", methods=['GET', 'POST'])
def user(id):
    page = request.args.get('page', 1, type=int)
    user = User.query.get_or_404(id)
    updatecomment=UpdateComment
    form = UpdateCommentForm()
    if form.validate_on_submit():
        updatecomment = UpdateComment(body=form.body.data,
                          update=update,
                          update_author=current_user._get_current_object() )
        db.session.add(updatecomment)
        db.session.commit()
        flash('Your comment has been published.', 'success')
        return redirect(url_for('users.user', id=updatecomment.update_author.id))
    updatecomments=UpdateComment.query.order_by(UpdateComment.timestamp.desc())
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(id=id).first_or_404()
    datetimecurr = datetime.utcnow()
    user_id = user.id
    reward = Rewards.query.filter_by(user_id=id).order_by(Rewards.timestamp.desc())
    tota = db.session.query(func.sum(Rewards.points)).filter(
        Rewards.user_id == id).scalar()
    sponsorshiprequest = SponsorshipRequest.query.filter_by(user_id=id).order_by(SponsorshipRequest.start_date.desc())
    update = Update.query.filter_by(user_id=id).order_by(Update.update_date_posted.desc()).paginate(page=page, per_page=6)
    sponsorships = Sponsorship.query.filter_by(user_id=id).order_by(Sponsorship.start_date.desc())
    posts = Post.query.filter_by(user_id=id).order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)
    campaign = Campaign.query.filter_by(user_id=id).order_by(Campaign.campaign_start_date.desc())
    brandbrief =  BrandBrief.query.filter_by(user_id=id).first()
    donationreason = DonationReason.query.filter_by(
        author_id=id).order_by(DonationReason.end_date.desc())
    donation = db.session.query(func.sum(Donation.amount)).filter(
        Donation.donation_id == DonationReason.id).scalar()
    blogs = Blog.query.filter_by(user_id=id).order_by(Blog.blog_date_posted.desc())
    events = Events.query.filter_by(user_id=id).order_by(Events.event_start_date.desc())
    socialdash = SocialDash.query.filter_by(user_id=id).first()
    special_event = Special_event.query.filter_by(user_id=id).first()
    achievement = Achievement.query.filter_by(user_id=id).first()
    follows = Follow.query.filter_by(follower_id=id).order_by(Follow.timestamp.desc())
    following = Follow.query.filter_by(followed_id=id).order_by(Follow.timestamp.desc())
    intrest = Intrest.query.filter_by(user_id=id).first()
    sports = Sports.query.filter_by(user_id=id).first()
    links = Links.query.filter_by(user_id=id).first()
    address = Address.query.filter_by(user_id=id).first()
    occupation = Occupation.query.filter_by(user_id=id).first()
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    posts = Post.query.filter_by(Protagonist=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('users/user.html', datetimecurr=datetimecurr, image_file=image_file, posts=posts, user=user, achievement=achievement, address=address, links=links, occupation=occupation,
                           sports=sports, intrest=intrest, special_event=special_event, updates=[
                               update], update=update, form=form, sponsorships=sponsorships, campaign=campaign, blogs=blogs, tota=tota, donationreason=donationreason, donation=donation,
                           updatecomments=updatecomments, follows=follows,  following=following, brandbrief=brandbrief, events=events, socialdash=socialdash,  updatecomment=updatecomment, reward=reward, title=user.username, sponsorshiprequest=sponsorshiprequest,
                         legend='New update')

@bp.route("/muser/<int:id>", methods=['GET', 'POST'])
def muser(id):
    page = request.args.get('page', 1, type=int)
    user = User.query.get_or_404(id)
    updatecomment=UpdateComment
    form = UpdateCommentForm()
    if form.validate_on_submit():
        updatecomment = UpdateComment(body=form.body.data,
                          update=update,
                          update_author=current_user._get_current_object() )
        db.session.add(updatecomment)
        db.session.commit()
        flash('Your comment has been published.', 'success')
        return redirect(url_for('users.muser', id=updatecomment.update_author.id))
    updatecomments=UpdateComment.query.order_by(UpdateComment.timestamp.desc())
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(id=id).first_or_404()
    datetimecurr = datetime.utcnow()
    user_id = user.id
    reward = Rewards.query.filter_by(user_id=id).order_by(Rewards.timestamp.desc())
    tota = db.session.query(func.sum(Rewards.points)).filter(
        Rewards.user_id == id).scalar()
    sponsorshiprequest = SponsorshipRequest.query.filter_by(user_id=id).order_by(SponsorshipRequest.start_date.desc())
    update = Update.query.filter_by(user_id=id).order_by(Update.update_date_posted.desc()).paginate(page=page, per_page=6)
    sponsorships = Sponsorship.query.filter_by(user_id=id).order_by(Sponsorship.start_date.desc())
    posts = Post.query.filter_by(user_id=id).order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)
    campaign = Campaign.query.filter_by(user_id=id).order_by(Campaign.campaign_start_date.desc())
    brandbrief =  BrandBrief.query.filter_by(user_id=id).first()
    donationreason = DonationReason.query.filter_by(
        author_id=id).order_by(DonationReason.end_date.desc())
    donation = db.session.query(func.sum(Donation.amount)).filter(
        Donation.donation_id == DonationReason.id).scalar()
    blogs = Blog.query.filter_by(user_id=id).order_by(Blog.blog_date_posted.desc())
    events = Events.query.filter_by(user_id=id).order_by(Events.event_start_date.desc())
    socialdash = SocialDash.query.filter_by(user_id=id).first()
    special_event = Special_event.query.filter_by(user_id=id).first()
    achievement = Achievement.query.filter_by(user_id=id).first()
    intrest = Intrest.query.filter_by(user_id=id).first()
    sports = Sports.query.filter_by(user_id=id).first()
    links = Links.query.filter_by(user_id=id).first()
    address = Address.query.filter_by(user_id=id).first()
    occupation = Occupation.query.filter_by(user_id=id).first()
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    posts = Post.query.filter_by(Protagonist=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('users/muser.html', datetimecurr=datetimecurr, image_file=image_file, posts=posts, user=user, achievement=achievement, address=address, links=links, occupation=occupation,
                           sports=sports, intrest=intrest, special_event=special_event, updates=[
                               update], update=update, form=form, sponsorships=sponsorships, campaign=campaign, blogs=blogs, tota=tota, donationreason=donationreason, donation=donation,
                           updatecomments=updatecomments,  brandbrief=brandbrief, events=events, socialdash=socialdash,  updatecomment=updatecomment, reward=reward, title=user.username, sponsorshiprequest=sponsorshiprequest,
                         legend='New update')



@bp.route("/update/<int:update_id>/update", methods=['GET', 'POST'])
@login_required
def update_update(update_id):
    update = Update.query.get_or_404(update_id)
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
                picture_file = save_pic(form.picture.data)
                update.image_file = picture_file
        update.update_text = form.update_text.data
        db.session.commit()
        flash(' post has been updated!', 'success')
        return redirect(url_for('users.user', id=update.update_author.id))
    elif request.method == 'GET':
        form.update_text.data = update.update_text
        form.update_location.data = update.update_location
    return render_template('users/update.html', title='Update update',
                           form=form, legend='update')


@bp.route("/events/<int:events_id>/update", methods=['GET', 'POST'])
@login_required
def update_events(events_id):
    events = Events.query.get_or_404(events_id)
    form = EventsForm()
    if form.validate_on_submit():
        if form.picture.data:
                picture_file = save_pics(form.picture.data)
                events.image_file = picture_file
        events.event_name = form.event_name.data
        events.event_description = form.event_description.data
        events.event_location = form.event_location.data
        events.event_type = form.event_type.data
        events.event_category = form.event_category.data
        events.event_links = form.event_links.data
        events.event_frequency = form.event_frequency.data
        events.event_start_date = form.event_start_date.data
        events.event_end_date = form.event_end_date.data
        db.session.commit()
        flash(' post has been updated!', 'success')
        return redirect(url_for('users.user', id=events.Protagonist.id))
    elif request.method == 'GET':
        form.event_name.data = events.event_name
        form.event_description.data = events.event_description
        form.event_location.data = events.event_location
        form.event_type.data = events.event_type
        form.event_category.data = events.event_category
        form.event_links.data = events.event_links
        form.event_frequency.data = events.event_frequency
        form.event_start_date.data = events.event_start_date
        form.event_end_date.data = events.event_end_date
    return render_template('users/event.html', title='Update Event',
                           form=form, legend='update')


@bp.route('/follow/<int:id>')
@login_required
def follow(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        flash(('User not found','warning'))
        return redirect(url_for('main.home'))
    if current_user.is_following(user):
        flash('You are already following this user', 'warning')
        return redirect(url_for('main.home', id=id))
    if user == current_user:
        flash(('You cannot follow yourself!', 'warning'))
        return redirect(url_for('main.home', id=id))
    current_user.follow(user)
    db.session.commit()
    random_hex = secrets.token_hex(8)
    rewards = Rewards(points=3, action="follow", address=random_hex, Protagonist=current_user)
    db.session.add(rewards)
    db.session.commit()
    flash('You are now following this user' , 'success' )
    return redirect(request.referrer)


@bp.route('/role/<int:id>/<action>')
@login_required
def role(id, action):
    user = User.query.get_or_404(id)
    if action == 'brand':
        current_user.role_is_brand(user)
        db.session.commit()
        flash("Congratulations ! Now you'll continue your journey as a Brand  ", 'success')
    if action == 'creators':
        current_user.role_is_creators(user)
        db.session.commit()
        flash("Congratulations ! Now you'll continue your journey as a Creator  ", 'success')
    if action == 'mentor':
        current_user.role_is_mentor(user)
        db.session.commit()
        flash("Congratulations ! Now you'll continue your journey as a mentor  ", 'success')
    return redirect(url_for('main.home'))


@bp.route("/verification/<int:id>/<action>", methods=['GET', 'POST'])
@login_required
def verification(id, action):
    user = User.query.get_or_404(id)
    if action == 'email':
        send_verify_email(user)
        flash('An email has been sent with instructions to verify your account.', 'info')
    if action == 'phone':
        send_verify_msg(user)
        flash('An message has been sent with instructions to verify your account.', 'info')
    return redirect(url_for('users.user', id=user.id))



@bp.route("/auth2verify/<token>", methods=['GET', 'POST'])
def auth2verify(token):
    if current_user.is_authenticated:
        user = User.verify_reset_token(token)
        if user is None:
            flash('That is an invalid or expired token', 'warning')
            return redirect(url_for('auth.login'))
        user.purpuse = "ok"
        db.session.commit()
        flash('Your profile has been sucessfully verified now you can apply for your desired role', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_token.html', title='Reset Password', form=form)





@bp.route('/unfollow/<int:id>')
@login_required
def unfollow(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        flash(('User  not found.', 'warning'))
        return redirect(url_for('main.home'))
    if user == current_user:
        flash(('You cannot unfollow yourself!', 'warning'))
        return redirect(url_for('users.user', id=id))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following this user anymore', 'danger'  )
    return redirect(request.referrer)

@bp.route('/followers/<int:id>')
def followers(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        flash('Invalid user', 'warning')
        return redirect(url_for('users.user'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('users/followers.html', user=user, title="Followers of",
                           endpoint='followers', pagination=pagination,
                           follows=follows)


@bp.route('/followed_by/<int:id>')
def followed_by(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('users.user'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='followed_by', pagination=pagination,
                           follows=follows)


@bp.route("/profile", methods=['GET', 'POST'])
def profile():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_pic(form.picture.data)
            update = Update(update_text=form.update_text.data,image_file=picture_file,update_author=current_user)
            db.session.add(update)
            db.session.commit()
        else:
            update = Update(update_text=form.update_text.data,update_author=current_user)
            db.session.add(update)
            db.session.commit()
        flash('Your update has been created!', 'success')
        return redirect(url_for('users.profile'))
    page = request.args.get('page', 1, type=int)
    ak = request.args.get('page', 1, type=int)
    update = Update.query.order_by(Update.update_date_posted.desc())
    events = Events.query.order_by(Events.event_start_date.desc())
    tota = db.session.query(func.sum(Rewards.points)).filter(
        Rewards.user_id == current_user.id).scalar()
    donationreason = DonationReason.query.order_by(DonationReason.end_date.desc())
    donation = db.session.query(func.sum(Donation.amount)).filter( Donation.donation_id == DonationReason.id).scalar()
    campaign = Campaign.query.order_by(Campaign.campaign_start_date.desc()).paginate(page=page, per_page=5)
    brand = User.query.filter_by(is_role="Brand").order_by(User.member_since.desc()).paginate(page=page, per_page=7)
    creators = User.query.filter_by(is_role="Creators").order_by(User.member_since.desc()).paginate(page=page, per_page=7)
    return render_template('users/profile.html', brand=brand, creators=creators, donationreason=donationreason, donation=donation, tota=tota,  events=events, campaign=campaign, current_time=datetime.utcnow(), update=update, form=form, title="Timeline")

@bp.route("/mprofile", methods=['GET', 'POST'])
def mprofile():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_pic(form.picture.data)
            update = Update(update_text=form.update_text.data,image_file=picture_file,update_author=current_user)
            db.session.add(update)
            db.session.commit()
        else:
            update = Update(update_text=form.update_text.data,update_author=current_user)
            db.session.add(update)
            db.session.commit()
        flash('Your update has been created!', 'success')
        return redirect(url_for('users.mprofile'))
    page = request.args.get('page', 1, type=int)
    ak = request.args.get('page', 1, type=int)
    update = Update.query.order_by(Update.update_date_posted.desc())
    events = Events.query.order_by(Events.event_start_date.desc())
    tota = db.session.query(func.sum(Rewards.points)).filter(
        Rewards.user_id == current_user.id).scalar()
    donationreason = DonationReason.query.order_by(DonationReason.end_date.desc())
    donation = db.session.query(func.sum(Donation.amount)).filter( Donation.donation_id == DonationReason.id).scalar()
    campaign = Campaign.query.order_by(Campaign.campaign_start_date.desc()).paginate(page=page, per_page=5)
    brand = User.query.filter_by(is_role="Brand").order_by(User.member_since.desc()).paginate(page=page, per_page=7)
    creators = User.query.filter_by(is_role="Creators").order_by(User.member_since.desc()).paginate(page=page, per_page=7)
    return render_template('users/mprofile.html', brand=brand, creators=creators, donationreason=donationreason, donation=donation, tota=tota,  events=events, campaign=campaign, current_time=datetime.utcnow(), update=update, form=form, title="Timeline")


@bp.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_popup.html', user=user)


@bp.route("/update/<int:update_id>/delete", methods=['POST'])
@login_required
def delete_update(update_id):
    update = Update.query.get_or_404(update_id)
    db.session.delete(update)
    db.session.commit()
    flash('  update has been deleted!', 'success')
    return redirect(request.referrer)


@bp.route("/events/<int:events_id>/delete", methods=['POST'])
@login_required
def delete_events(events_id):
    events = Events.query.get_or_404(events_id)
    db.session.delete(events)
    db.session.commit()
    flash('  event has been deleted!', 'success')
    return redirect(request.referrer)

@bp.route('/updatelike/<int:update_id>/<action>')
@login_required
def updatelike_action(update_id, action):
    update = Update.query.filter_by(id=update_id).first_or_404()
    if action == 'like':
        current_user.like_update(update)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_update(update)
        db.session.commit()
    return redirect(request.referrer)

@bp.route('/eventintrest/<int:events_id>/<action>')
@login_required
def eventin_action(events_id, action):
    events = Events.query.filter_by(id=events_id).first_or_404()
    if action == 'in':
        current_user.in_events(events)
        db.session.commit()
    if action == 'out':
        current_user.out_events(events)
        db.session.commit()
    return redirect(request.referrer)

@bp.route('/updatecommentlike/<int:update_comment_id>/<action>')
@login_required
def updatecommentlike_action(update_comment_id, action):
    updatecomment = Update.query.filter_by(id=update_comment_id).first_or_404()
    if action == 'like':
        current_user.like_updatecomment(updatecomment)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_updatecomment(updatecomment)
        db.session.commit()
    return redirect(request.referrer)


@bp.route("/rewards", methods=['GET', 'POST'])
def rewards():

    reward = Rewards.query.filter_by(user_id=current_user.id).order_by(Rewards.timestamp.desc())
    tota = db.session.query(func.sum(Rewards.points)).filter(
        Rewards.user_id == current_user.id).scalar()
    return render_template('users/rewards.html', reward=reward, tota=tota,  current_time=datetime.utcnow(), title='Rewards')
