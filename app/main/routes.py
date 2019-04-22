from flask import render_template, request, current_app, request, g, url_for, redirect
from .. import db
from app.models import Post, Comment, User, Donation, Campaign, Rewards, Follow, RoleRequest
from flask_bootstrap import Bootstrap
from sqlalchemy.sql import func
from flask_login import login_user, current_user, logout_user, login_required
from app.main.forms import InputTextForm, SearchForm
from datetime import datetime
from app.main import bp

import random
import logging

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        g.search_form = SearchForm()
        db.session.commit()



@bp.route("/", methods=['GET', 'POST'])
def landing():
    return redirect(url_for('auth.login'))

@bp.route("/tandc", methods=['GET', 'POST'])
def tandc():
    return render_template('main/t&c.html')


@bp.route("/role", methods=['GET', 'POST'])
def role():
    return render_template('main/role.html')


@bp.route("/brandoffer", methods=['GET', 'POST'])
def brandoffer():
    return render_template('main/brandoffer.html')


@bp.route("/accountverify", methods=['GET', 'POST'])
def accountverify():
    return render_template('main/verification.html')

@bp.route("/roleapply1", methods=['GET', 'POST'])
def role1():
    return render_template('main/role1.html')

@bp.route("/roleapply2", methods=['GET', 'POST'])
def role2():
    return render_template('main/role2.html')


@bp.route("/roleapply3", methods=['GET', 'POST'])
def role3():
    return render_template('main/role3.html')

@bp.route("/aboutus", methods=['GET', 'POST'])
def about():
    return render_template('main/aboutus.html')

@bp.route("/rolerequest", methods=['GET', 'POST'])
def rolerequest():
    role = RoleRequest.query.order_by(RoleRequest.timestamp.desc())
    return render_template('main/rolerequest.html', role=role)


@bp.route("/AdminDashboard", methods=['GET', 'POST'])
def dashboard():
    page = request.args.get('page', 1, type=int)
    follows = Follow.query.order_by(Follow.timestamp.desc()).paginate(page=page, per_page=5)
    donations = Donation.query.order_by(Donation.time_created.desc())
    campaign = Campaign.query.order_by(Campaign.campaign_start_date.desc())
    creators = User.query.order_by(User.member_since.desc())
    tota = db.session.query(func.sum(Donation.amount)).scalar()
    total = db.session.query(func.sum(Rewards.points)).scalar()
    return render_template('main/dashboard.html', creators=creators, total=total, tota=tota, campaign=campaign, current_time=datetime.utcnow(), donations=donations, follows=follows)


@bp.route("/home", methods=['GET', 'POST'])
def home():
    legend = 'Monthly Data'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    page = request.args.get('page', 1, type=int)
    campaign = Campaign.query.order_by(Campaign.campaign_start_date.desc()).paginate(page=page, per_page=10)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=100)

    return render_template('main/home.html', posts=posts, values=values, labels=labels, legend=legend, campaign=campaign, current_time=datetime.utcnow(), title='Home')

@bp.route("/sports", methods=['GET', 'POST'])
def sports():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category="Sports").order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)

    return render_template('main/sports.html', posts=posts, current_time=datetime.utcnow(), title='Sports')

@bp.route("/music", methods=['GET', 'POST'])
def music():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category="Music").order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)

    return render_template('main/music.html', posts=posts, current_time=datetime.utcnow(), title='Music')

@bp.route("/pc", methods=['GET', 'POST'])
def pc():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category="People's Corner").order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)

    return render_template('main/pc.html', posts=posts, current_time=datetime.utcnow(), title="people's Corner")

@bp.route("/design", methods=['GET', 'POST'])
def design():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category="Design").order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)

    return render_template('main/design.html', posts=posts, current_time=datetime.utcnow(), title='Design')

@bp.route("/travel", methods=['GET', 'POST'])
def travel():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category="Travel").order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)

    return render_template('main/travel.html', posts=posts, current_time=datetime.utcnow(), title='Travel')

@bp.route("/others", methods=['GET', 'POST'])
def others():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category="Others").order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)

    return render_template('main/others.html', posts=posts, current_time=datetime.utcnow(), title='Others')




@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('main/home.html', title=_('Explore'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)



@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('main/search.html', title=('Search'), posts=posts,
                           next_url=next_url, prev_url=prev_url)







@bp.route('/')
def track_example():
    track_event(
        category='Example',
        action='test action')
    return 'Event tracked.'


@bp.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500
















def analyse():
    start = time.time()
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        #NLP Stuff
        blob = TextBlob(rawtext)
        received_text2 = blob
        blob_sentiment,blob_subjectivity = blob.sentiment.polarity ,blob.sentiment.subjectivity
        number_of_tokens = len(list(blob.words))
        # Extracting Main Points
        nouns = list()
        for word, tag in blob.tags:
            if tag == 'NN':
                nouns.append(word.lemmatize())
                len_of_words = len(nouns)
                rand_words = random.sample(nouns,len(nouns))
                final_word = list()
                for item in rand_words:
                    word = Word(item).pluralize()
                    final_word.append(word)
                    summary = final_word
                    end = time.time()
                    final_time = end-start
        return render_template('main/analytics.html',received_text = received_text2,number_of_tokens=number_of_tokens,blob_sentiment=blob_sentiment,blob_subjectivity=blob_subjectivity,summary=summary,final_time=final_time)
