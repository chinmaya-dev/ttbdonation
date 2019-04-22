from datetime import datetime
import os
import json
from time import time
from sqlalchemy_utils import JSONType
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import db, login_manager, bcrypt
from markdown import markdown
from flask import current_app, request, url_for
import bleach
from flask_login import UserMixin, AnonymousUserMixin
from .search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)




class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.ADMIN],
            'Brand': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
            'Mentor': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    username = db.Column(db.String(20), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    about_me = db.Column(db.String(140))
    language = db.Column(db.String(140))
    is_role =  db.Column(db.String(140))
    social_id = db.Column(db.String(140))
    gender = db.Column(db.String(5))
    contact_number = db.Column(db.Integer)
    tandc = db.Column(db.Boolean)
    first_name = db.Column(db.String(60))
    brand_name = db.Column(db.String(60))
    company_name = db.Column(db.String(60))
    role_in_brand = db.Column(db.String(60)) 
    last_name = db.Column(db.String(60))
    category = db.Column(db.String(60))
    issues = db.Column(db.String(60))
    sub_category = db.Column(db.String(60))
    purpuse = db.Column(db.String(60))
    available_for_sponsorship = db.Column(db.String(60))
    web_url = db.Column(db.String(60))
    education_level = db.Column(db.String(60))
    education_institution = db.Column(db.String(60))
    support =  db.Column(db.String(60))
    date_of_birth = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    rewards =  db.relationship('Rewards', backref='Protagonist', lazy='dynamic')
    address = db.relationship('Address', backref='Protagonist', lazy='dynamic')
    occumpation = db.relationship('Occupation', backref='Protagonist', lazy='dynamic')
    donation = db.relationship('Donation', backref='Protagonist', lazy='dynamic')
    donor = db.relationship('DonationReason', backref='Protagonist', lazy='dynamic')
    posts = db.relationship('Post', backref='Protagonist', lazy='dynamic')
    requestrole = db.relationship('RoleRequest', backref='Protagonist', lazy='dynamic')
    sponsorship = db.relationship('Sponsorship', backref='Protagonist', lazy='dynamic')
    sponsorship_request = db.relationship('SponsorshipRequest', backref='Protagonist', lazy='dynamic')
    sponsorship_request_faq = db.relationship('SponsorshipRequestFAQ', backref='Protagonist', lazy='dynamic')
    sponsorship_faq = db.relationship('SponsorshipFAQ', backref='Protagonist', lazy='dynamic')
    additional_sports = db.relationship('AdditionalSports', backref='Protagonist', lazy='dynamic')
    sponsorship_accept = db.relationship('SponsorshipAccept', backref='Protagonist', lazy='dynamic')
    sponsorship_accept_inv = db.relationship('SponsorshipAcceptInv', backref='Protagonist', lazy='dynamic')
    sponsorship_apply = db.relationship('SponsorshipApply', backref='Protagonist', lazy='dynamic')
    blog = db.relationship('Blog', backref = 'blog_author', lazy= 'dynamic')
    campaign = db.relationship('Campaign', backref = 'campaign_author', lazy= 'dynamic')
    update = db.relationship('Update', backref = 'update_author', lazy= 'dynamic')
    cam_boost = db.relationship('CampaignBoost', backref='Protagonist', lazy='dynamic')
    post_boost = db.relationship('PostBoost', backref='Protagonist', lazy='dynamic')
    sponsor_boost = db.relationship('SponsorshipBoost', backref='Protagonist', lazy='dynamic')
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='Protagonist', lazy='dynamic')
    campaign_comments = db.relationship('CampaignComment', backref='campaign_author', lazy='dynamic')
    campaign_faq = db.relationship('CampaignFAQ', backref='campaign_author', lazy='dynamic')
    Campaign_budget = db.relationship('CampaignBudget', backref='campaign_author', lazy='dynamic')
    donation_comments = db.relationship('DonationComments', backref='Protagonist', lazy='dynamic')
    donation_updates = db.relationship('DonationUpdates', backref='Protagonist', lazy='dynamic')
    dash = db.relationship('SocialDash', backref='Protagonist', lazy='dynamic')
    update_comments = db.relationship('UpdateComment', backref='update_author', lazy='dynamic')
    blog_comments = db.relationship('BlogComment', backref='blog_author', lazy='dynamic')
    links = db.relationship('Links', backref='Protagonist', lazy='dynamic')
    intrest = db.relationship('Intrest', backref='Protagonist', lazy='dynamic')
    sports =  db.relationship('Sports', backref='Protagonist', lazy='dynamic')
    brandbrief = db.relationship('BrandBrief', backref='Protagonist', lazy='dynamic')
    achievement = db.relationship('Achievement', backref='Protagonist', lazy='dynamic')
    events = db.relationship('Events', backref='Protagonist', lazy='dynamic')
    bio = db.relationship('Bio', backref='Protagonist', lazy='dynamic')
    event_intrested = db.relationship('EventsIntrest', backref='Protagonist', lazy='dynamic')
    eventsfaq = db.relationship('EventsFAQ', backref='Protagonist', lazy='dynamic')
    travel = db.relationship('Travel', backref='Protagonist', lazy='dynamic')
    special_event = db.relationship('Special_event', backref='Protagonist', lazy='dynamic')
    media = db.relationship('Media', backref='Protagonist', lazy='dynamic')
    post_liked = db.relationship(
        'PostLike',
        foreign_keys='PostLike.user_id',
        backref='user', lazy='dynamic')
    comment_liked = db.relationship(
        'CommentLike',
        foreign_keys='CommentLike.user_id',
        backref='user', lazy='dynamic')
    blog_liked = db.relationship(
        'BlogLike',
        foreign_keys='BlogLike.user_id',
        backref='user', lazy='dynamic')
    blog_comment_liked = db.relationship(
        'BlogCommentLike',
        foreign_keys='BlogCommentLike.user_id',
        backref='user', lazy='dynamic')
    campaign_liked = db.relationship(
        'CampaignLike',
        foreign_keys='CampaignLike.user_id',
        backref='user', lazy='dynamic')
    campaign_sub = db.relationship(
        'CampaignSub',
        foreign_keys='CampaignSub.user_id',
        backref='user', lazy='dynamic')
    events_intrested = db.relationship(
        'EventsIntrest',
        foreign_keys='EventsIntrest.user_id',
        backref='user', lazy='dynamic')
    campaign_comment_liked = db.relationship(
        'CampaignCommentLike',
        foreign_keys='CampaignCommentLike.user_id',
        backref='user', lazy='dynamic')
    update_liked = db.relationship(
        'UpdateLike',
        foreign_keys='UpdateLike.user_id',
        backref='user', lazy='dynamic')
    update_comment_liked = db.relationship(
        'UpdateCommentLike',
        foreign_keys='UpdateCommentLike.user_id',
        backref='user', lazy='dynamic')
    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)
    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic')

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == post.id).count() > 0

    def like_comment(self, comment):
        if not self.has_liked_comment(comment):
            like = CommentLike(user_id=self.id, comment_id=comment.id)
            db.session.add(like)

    def unlike_comment(self, comment):
        if self.has_liked_comment(comment):
            CommentLike.query.filter_by(
                user_id=self.id,
                comment_id=comment.id).delete()

    def has_liked_comment(self, comment):
        return CommentLike.query.filter(
            CommentLike.user_id == self.id,
            CommentLike.comment_id == comment.id).count() > 0

    def like_blog(self, blog):
        if not self.has_liked_blog(blog):
            like = BlogLike(user_id=self.id, blog_id=blog.id)
            db.session.add(like)

    def unlike_blog(self, blog):
        if self.has_liked_blog(blog):
            BlogLike.query.filter_by(
                user_id=self.id,
                blog_id=blog.id).delete()

    def has_liked_blog(self, blog):
        return BlogLike.query.filter(
            BlogLike.user_id == self.id,
            BlogLike.blog_id == blog.id).count() > 0

    def like_blogcomment(self, blogcomment):
        if not self.has_liked_blogcomment(blogcomment):
            like = BlogCommentLike(user_id=self.id, blog_comment_id=blogcomment.id)
            db.session.add(like)



    def unlike_blogcomment(self, blogcomment):
        if self.has_liked_blogcomment(blogcomment):
            BlogCommentLike.query.filter_by(
                user_id=self.id,
                blog_comment_id=blogcomment.id).delete()

    def has_liked_blogcomment(self, blogcomment):
        return BlogCommentLike.query.filter(
            BlogCommentLike.user_id == self.id,
            BlogCommentLike.blog_comment_id == blogcomment.id).count() > 0

    def like_campaign(self, campaign):
        if not self.has_liked_campaign(campaign):
            like = CampaignLike(user_id=self.id, campaign_id=campaign.id)
            db.session.add(like)

    def unlike_campaign(self, campaign):
        if self.has_liked_campaign(campaign):
            CampaignLike.query.filter_by(
                user_id=self.id,
                campaign_id=campaign.id).delete()

    def has_liked_campaign(self, campaign):
        return CampaignLike.query.filter(
            CampaignLike.user_id == self.id,
            CampaignLike.campaign_id == campaign.id).count() > 0


    def sub_campaign(self, campaign):
        if not self.has_sub_campaign(campaign):
            sub = CampaignSub(user_id=self.id, campaign_id=campaign.id)
            db.session.add(sub)

    def unsub_campaign(self, campaign):
        if self.has_sub_campaign(campaign):
            CampaignSub.query.filter_by(
                user_id=self.id,
                campaign_id=campaign.id).delete()

    def has_sub_campaign(self, campaign):
        return CampaignSub.query.filter(
            CampaignSub.user_id == self.id,
            CampaignSub.campaign_id == campaign.id).count() > 0
    
    def in_events(self, events):
        if not self.has_in_events(events):
            inn = EventsIntrest(user_id=self.id, events_id=events.id)
            db.session.add(inn)

    def out_events(self, events):
        if self.has_in_events(events):
            EventsIntrest.query.filter_by(
                user_id=self.id,
                events_id=events.id).delete()

    def has_in_events(self, events):
        return EventsIntrest.query.filter(
            EventsIntrest.user_id == self.id,
            EventsIntrest.events_id == events.id).count() > 0

    def like_campaigncomment(self, campaigncomment):
        if not self.has_liked_campaigncomment(campaigncomment):
            like = CampaignCommentLike(user_id=self.id, campaign_comment_id=campaigncomment.id)
            db.session.add(like)

    def unlike_campaigncomment(self, campaigncomment):
        if self.has_liked_campaigncomment(campaigncomment):
            CampaignCommentLike.query.filter_by(
                user_id=self.id,
                campaign_comment_id=campaigncomment.id).delete()

    def has_liked_campaigncomment(self, campaigncomment):
        return CampaignCommentLike.query.filter(
            CampaignCommentLike.user_id == self.id,
            CampaignCommentLike.campaign_comment_id == campaigncomment.id).count() > 0

    def like_update(self, update):
        if not self.has_liked_update(update):
            like = UpdateLike(user_id=self.id, update_id=update.id)
            db.session.add(like)

    def unlike_update(self, update):
        if self.has_liked_update(update):
            UpdateLike.query.filter_by(
                user_id=self.id,
                update_id=update.id).delete()

    def has_liked_update(self, update):
        return UpdateLike.query.filter(
            UpdateLike.user_id == self.id,
            UpdateLike.update_id == update.id).count() > 0

    def like_updatecomment(self, updatecomment):
        if not self.has_liked_updatecomment(updatecomment):
            like = UpdateCommentLike(user_id=self.id, update_comment_id=updatecomment.id)
            db.session.add(like)

    def unlike_updatecomment(self, updatecomment):
        if self.has_liked_updatecomment(updatecomment):
            UpdateCommentLike.query.filter_by(
                user_id=self.id,
                update_comment_id=updatecomment.id).delete()

    def has_liked_updatecomment(self, updatecomment):
        return UpdateCommentLike.query.filter(
            UpdateCommentLike.user_id == self.id,
            UpdateCommentLike.blog_comment_id == updatecomment.id).count() > 0

    def role_is_brand(self, user):
        user.is_role = "Brand"
        

    def role_is_creators(self, user):
        user.is_role = "Creators"

    def role_is_mentor(self, user):
        user.is_role ="Mentor"
        

    def has__donated(self, post):
        return Donation.query.filter(
            Donation.user_id == self.id,
            Donation.post_id == post.id).count() > 0



    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.is_role == 'Brand':
                self.role = Role.query.filter_by(name='Brand').first()
            if self.is_role == 'Mentor':
                self.role = Role.query.filter_by(name='Mentor').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        self.follow(self)


    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_brand(self):
        return self.can(Permission.MODERATE)

    def is_administrator(self):
        return self.can(Permission.ADMIN)


    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)


    def is_following(self, user):
        if user.id is None:
            return False
        return self.followed.filter_by(
            followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        if user.id is None:
            return False
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')



    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()

    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n





    def __repr__(self):
        return f"User('{self.username}', '{self.user_id}', '{self.email}', '{self.image_file}', '{self.id}', '{self.last_message_read_time}', '{self.is_role}',  '{self.category}',  '{self.sub_category}', '{self.web_url}')"

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

    def is_brand(self):
        return False


    def is_mentor(self):
        return False

    def has_liked_post(self, post):
        return False

    def has_liked_comment(self, comment):
        return False

    def has_liked_blog(self, blog):
        return False

    def has_liked_blogcomment(self, blogcomment):
        return False

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)

class RoleRequest( db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime,
                            default=datetime.utcnow)

class Post( db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    story_line = db.Column(db.String(500), nullable=False)
    story_text = db.Column(db.Text, nullable=False)
    youtube_link = db.Column(db.String(500), nullable=True)
    image_file = db.Column(db.String(20), default='default.jpg')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    likes = db.relationship('PostLike', backref='post', lazy='dynamic')
    boost = db.relationship('PostBoost', backref='post', lazy='dynamic')

    def __repr__(self):
        return f"Post('{self.Protagonist}', '{self.date_posted}')"



class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    likes = db.relationship('CommentLike', backref='comment', lazy='dynamic')



    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

db.event.listen(Comment.body, 'set', Comment.on_changed_body)


class PostBoost(db.Model):
    __tablename__ = 'postboost'
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.Text)
    target_audience = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    amount = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

class Sports(db.Model):
    __tablename__ = 'sports'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    level_of_playing = db.Column(db.Text)
    current_team = db.Column(db.Text)
    tournament = db.Column(db.Text)

def __repr__(self):
        return f"Address('{self.Protagonist}', '{self.id}')"

class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    street = db.Column(db.Text)
    city = db.Column(db.Text)
    zip_code = db.column(db.text)
    country = db.Column(db.Text)

def __repr__(self):
        return f"Address('{self.Protagonist}', '{self.id}')"


class Occupation(db.Model):
    __tablename__ = 'occupation'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    occupation_name = db.Column(db.Text)
    occupation_company = db.Column(db.Text)
    occupation_start_date =  db.Column(db.DateTime, index=True, default=datetime.utcnow)
    occupation_end_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)


def __repr__(self):
        return f"Occupation('{self.Protagonist}', '{self.occupation_company}', '{self.occupation_name}', '{self.id}' )"


class Links(db.Model):
    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    facebook_id = db.Column(db.Text)
    twitter_id = db.Column(db.Text)
    instagram_id = db.Column(db.Text)
    snapchat_id = db.Column(db.Text)

def __repr__(self):
        return f"Links( '{self.Protagonist}' , '{self.facebook_id}', '{self.twitter_id}', '{self.instagram_id}', '{self.snapchat_id}' )"

class BrandBrief(db.Model):
    __tablename__ = 'brandbrief'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    business_description = db.Column(db.Text)
    current_market_perception = db.Column(db.Text)
    brand_goals = db.Column(db.Text)
    brand_psychology = db.Column(db.Text)

def __repr__(self):
        return f"Links( '{self.Protagonist}' , '{self.business_description}', '{self.current_market_perception}', '{self.brand_goals}', '{self.brand_psychology}' )"

class Intrest(db.Model):
    __tablename__ = 'intrest'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    intrest_type = db.Column(db.Text)

def __repr__(self):
        return f"Intrest( '{self.Protagonist}', '{self.intrest_type}', '{self.intrest_names}' )"


class Achievement(db.Model):
    __tablename__ = 'achievements'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    medal_count = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

def __repr__(self):
        return f"Achievement('{self.medal}', '{self.medal_count}', '{self.Protagonist}' )"

class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_type = db.Column(db.String)
    event_name = db.Column(db.String)
    event_category = db.Column(db.String)
    event_description = db.Column(db.String)
    image_file = db.Column(db.String(20), default='default.jpg')
    event_location = db.Column(db.String)
    event_start_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    event_end_date =  db.Column(db.DateTime, index=True, default=datetime.utcnow)
    event_frequency = db.Column(db.String)
    event_links = db.Column(db.String)
    intrest = db.relationship('EventsIntrest', backref='events', lazy='dynamic')
    faq = db.relationship('EventsFAQ', backref='events', lazy='dynamic')
def __repr__(self):
        return f"Events('{self.event_name_}', '{self.event_location}', '{self.event_status}', '{self.Protagonist}' )"


class EventsIntrest(db.Model):
    __tablename__ = 'eventsintrest'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    events_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class EventsFAQ(db.Model):
    __tablename__ = 'eventsfaq'
    id = db.Column(db.Integer, primary_key=True)
    que = db.Column(db.Text)
    ans = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    events_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(EventsFAQ.que, 'set', EventsFAQ.on_changed_body)

class Travel(db.Model):
    __tablename__ = 'travel'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    place = db.Column(db.String)
    start_date =  db.Column(db.DateTime, index=True, default=datetime.utcnow)
    end_date =  db.Column(db.DateTime, index=True, default=datetime.utcnow)

def __repr__(self):
        return f"Travel('{self.place}', '{self.Protagonist}' )"

class Special_event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    life_event = db.Column(db.String)
    life_event_start_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    life_event_end_date =  db.Column(db.DateTime, index=True, default=datetime.utcnow)


def __repr__(self):
        return f"Special_event('{self.life_event}', '{self.Protagonist}')"

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    media_name = db.Column(db.String)
    media_format = db.Column(db.String)

def __repr__(self):
        return f"Media('{self.media_name}', '{self.media_name}', '{self.Protagonist}' )"




class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blog_city = db.Column(db.String(50), nullable=False)
    blog_category = db.Column(db.String(50), nullable=False)
    blog_story_line = db.Column(db.String(500), nullable=False)
    blog_story_text = db.Column(db.Text, nullable=False)
    blog_youtube_link = db.Column(db.String(500), nullable=True)
    blog_youtube_tagline = db.Column(db.String(500), nullable=True)
    blog_date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    blogcomments = db.relationship('BlogComment', backref='blog', lazy='dynamic')
    likes = db.relationship('BlogLike', backref='blog', lazy='dynamic')


    def __repr__(self):
        return f"Blog('{self.blog_author}', '{self.date_posted}')"



class BlogComment(db.Model):
    __tablename__ = 'blogcomments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    likes = db.relationship('BlogCommentLike', backref='blogcomment', lazy='dynamic')

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

db.event.listen(BlogComment.body, 'set', BlogComment.on_changed_body)


class PostLike(db.Model):
    __tablename__ = 'postlikes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class CommentLike(db.Model):
    __tablename__ = 'commentlikes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class BlogLike(db.Model):
    __tablename__ = 'bloglikes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class BlogCommentLike(db.Model):
    __tablename__ = 'blogcommentlikes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blog_comment_id = db.Column(db.Integer, db.ForeignKey('blogcomments.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image_file = db.Column(db.String(20), default='default.jpg')
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))


class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(20), default='default.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String)
    goal = db.Column(db.Text, nullable=False)
    location = db.Column(db.String, nullable=False)
    language = db.Column(db.String)
    business_category = db.Column(db.String)
    service_category = db.Column(db.String)
    headline_1 = db.Column(db.Text, nullable=False)
    headline_2 = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    ad_format = db.Column(db.String)
    links = db.Column(db.String)
    action = db.Column(db.Text)
    campaign_start_date = db.Column(
        db.DateTime, index=True, default=datetime.utcnow)
    campaign_end_date = db.Column(
        db.DateTime, index=True, default=datetime.utcnow)
    target_age_range = db.Column(db.Integer)
    target_category = db.column(db.Text)
    sub_goals = db.Column(db.Integer)
    campaigncomments = db.relationship(
        'CampaignComment', backref='campaign', lazy='dynamic')
    campaignfaq = db.relationship(
        'CampaignFAQ', backref='campaign', lazy='dynamic')
    likes = db.relationship('CampaignLike', backref='campaign', lazy='dynamic')
    sub = db.relationship('CampaignSub', backref='campaign', lazy='dynamic')
    campaignbudget = db.relationship(
        'CampaignBudget', backref='campaign', lazy='dynamic')
    boost = db.relationship('CampaignBoost', backref='campaign', lazy='dynamic')

    def __repr__(self):
        return f"Campaign('{self.campaign_author}', '{self.Campaign_start_date}', '{self.Campaign_end_date}')"


class CampaignBudget(db.Model):
    __tablename__ = 'campaignbudget'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)


class CampaignComment(db.Model):
    __tablename__ = 'campaigncomments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    likes = db.relationship('CampaignCommentLike',
                            backref='campaigncomment', lazy='dynamic')

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(CampaignComment.body, 'set', CampaignComment.on_changed_body)


class CampaignFAQ(db.Model):
    __tablename__ = 'campaignfaq'
    id = db.Column(db.Integer, primary_key=True)
    que = db.Column(db.Text)
    ans = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(CampaignFAQ.que, 'set',CampaignFAQ.on_changed_body)


class CampaignLike(db.Model):
    __tablename__ = 'campaignlikes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class CampaignCommentLike(db.Model):
    __tablename__ = 'campaigncommentlikes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    campaign_comment_id = db.Column(
        db.Integer, db.ForeignKey('campaigncomments.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class CampaignSub(db.Model):
    __tablename__ = 'campaignsub'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class CampaignBoost(db.Model):
    __tablename__ = 'campaignboost'
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.Text)
    target_audience = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    amount = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    


class Donation(db.Model):
    __tablename__ = 'donation'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    donation_id = db.Column(db.Integer, db.ForeignKey('donationreason.id'), nullable=False)
    amount = db.Column(db.Integer)
    time_created = db.Column(db.DateTime)

    def __repr__(self):
        return f"Donation('{self.Protagonist}', '{self.id}')"


class DonationReason(db.Model):
    __tablename__ = 'donationreason'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Text)
    title = db.Column(db.Text)
    short = db.Column(db.Text)
    description = db.Column(db.Text)
    image_file = db.Column(db.String(20), default='default.jpg')
    goal = db.Column(db.Text)
    target_amount = db.Column(db.Integer)
    amount_prefilled  = db.Column(db.Integer)
    end_method = db.Column(db.Text)
    link = db.Column(db.Text)
    country = db.Column(db.Text)
    address = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, index=True, default=datetime.utcnow) 
    donation = db.relationship('Donation', backref='donationreason', lazy='dynamic')
    donationcomments = db.relationship('DonationComments', backref='donationreason', lazy='dynamic')
    updates = db.relationship('DonationUpdates', backref='donationreason', lazy='dynamic')

class DonationComments(db.Model):
    __tablename__ = 'donationcomments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    donationreason_id = db.Column(db.Integer, db.ForeignKey('donationreason.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(DonationComments.body, 'set', DonationComments.on_changed_body)


class DonationUpdates(db.Model):
    __tablename__ = 'donationupdates'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    donationreason_id = db.Column(db.Integer, db.ForeignKey('donationreason.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(DonationUpdates.body, 'set', DonationUpdates.on_changed_body)


    
  

class Update(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    update_location = db.Column(db.String(50))
    image_file = db.Column(db.String(20), default='default.jpg')
    update_text = db.Column(db.String(500), nullable=False)
    update_date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updatecomments = db.relationship('UpdateComment', backref='update', lazy='dynamic')
    likes = db.relationship('UpdateLike', backref='blog', lazy='dynamic')


    def __repr__(self):
        return f"Update('{self.update_author}', '{self.update_date_posted}')"

class UpdateComment(db.Model):
    __tablename__ = 'updatecomments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    update_id = db.Column(db.Integer, db.ForeignKey('update.id'))
    likes = db.relationship('UpdateCommentLike', backref='updatecomment', lazy='dynamic')

class UpdateLike(db.Model):
    __tablename__ = 'updatelikes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    update_id = db.Column(db.Integer, db.ForeignKey('update.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class UpdateCommentLike(db.Model):
    __tablename__ = 'updatecommentlikes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    update_comment_id = db.Column(db.Integer, db.ForeignKey('updatecomments.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Sponsorship(db.Model):
    __tablename__ = 'sponsorship'
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(20), default='default.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String)
    network = db.Column(db.String)
    concept = db.Column(db.String)
    product_link = db.Column(db.String)
    target_category = db.Column(db.String)
    type_infu = db.Column(db.String)
    category = db.Column(db.String)
    payment_mode = db.Column(db.String)
    price_range = db.Column(db.String)
    duration = db.Column(db.String)
    target_age_range = db.Column(db.String)
    content = db.Column(db.String)
    target_gender = db.Column(db.String)
    start_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    apply = db.relationship('SponsorshipApply', backref='sponsorship', lazy='dynamic')
    faq = db.relationship(
        'SponsorshipFAQ', backref='sponsorship', lazy='dynamic')
    def __repr__(self):
        return f"Sponsorship('{self.name}', '{self.Protagonist}' )"


class SponsorshipFAQ(db.Model):
    __tablename__ = 'sponsorshipfaq'
    id = db.Column(db.Integer, primary_key=True)
    que = db.Column(db.Text)
    ans = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sponsor_id = db.Column(
        db.Integer, db.ForeignKey('sponsorship.id'))


class SponsorshipApply(db.Model):
    __tablename__ = 'sponsorshipapply'
    id = db.Column(db.Integer, primary_key=True)
    network = db.Column(db.Text)
    amount = db.Column(db.Integer)
    concept = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsorship.id'))
    invitations = db.relationship('SponsorshipAcceptInv', backref='sponsorshipapply', lazy='dynamic')
    

class SponsorshipRequest(db.Model):
    __tablename__ = 'sponsorshiprequest'
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(20), default='default.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String)
    requirements = db.Column(db.String)
    brand_preference = db.Column(db.String)
    already_sponsored = db.Column(db.String)
    Category = db.Column(db.String)
    project_type = db.Column(db.String)
    pay = db.Column(db.String)
    link = db.Column(db.String)
    first_time = db.Column(db.String)
    start_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    sports = db.relationship('AdditionalSports', backref='sponsorshiprequest', lazy='dynamic')
    accept = db.relationship('SponsorshipAccept', backref='sponsorshiprequest', lazy='dynamic')
    boost = db.relationship('SponsorshipBoost', backref='sponsorshiprequest', lazy='dynamic')
    faq = db.relationship('SponsorshipRequestFAQ', backref='sponsorshiprequest', lazy='dynamic')

    def __repr__(self):
        return f"SponsorshipRequest('{self.title}', '{self.Protagonist}' )"


class SponsorshipRequestFAQ(db.Model):
    __tablename__ = 'sponsorshiprequestfaq'
    id = db.Column(db.Integer, primary_key=True)
    que = db.Column(db.Text)
    ans = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sponsor_request_id = db.Column(
        db.Integer, db.ForeignKey('sponsorshiprequest.id'))


class AdditionalSports(db.Model):
    __tablename__ = 'additionalsports'
    id = db.Column(db.Integer, primary_key=True)
    profession_type = db.Column(db.Text)
    game = db.Column(db.Text)
    target_audience = db.Column(db.Text)
    visitors = db.Column(db.Text)
    event_scope = db.Column(db.Text)
    visibility_material = db.Column(db.Text)
    communication_plan = db.Column(db.Text)
    digital_return = db.Column(db.Text)
    logo = db.Column(db.Text)
    hospitality = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sponsor_request_id = db.Column(db.Integer, db.ForeignKey('sponsorshiprequest.id'))
    

class SponsorshipAccept(db.Model):
    __tablename__ = 'sponsorshipaccept'
    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.Text)
    amount = db.Column(db.Integer)
    goal = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    sponsor_request_id = db.Column(db.Integer, db.ForeignKey('sponsorshiprequest.id'))


class SponsorshipAcceptInv(db.Model):
    __tablename__ = 'sponsorshipacceptinv'
    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.Text)
    amount = db.Column(db.Integer)
    goal = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    sponsor_request_id = db.Column(db.Integer, db.ForeignKey('sponsorshipapply.id'))


class SponsorshipBoost(db.Model):
    __tablename__ = 'Sponsorshipboost'
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.Text)
    target_audience = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    amount = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sponsor_request_id = db.Column(db.Integer, db.ForeignKey('sponsorshiprequest.id'))

class Rewards(db.Model):
    __tablename__ = 'rewards'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    points = db.Column(db.Integer)
    action = db.Column(db.Text)
    address = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class Bio(db.Model):
    __tablename__ = 'bio'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    goal = db.Column(db.Text)
    hurdles = db.Column(db.Text)
    rank = db.Column(db.Text)
    accomplished = db.Column(db.Text)
    fear = db.Column(db.Text)
    finance = db.Column(db.Text)
    market = db.Column(db.Text)
    other = db.Column(db.Text)
    motivate = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

class SocialDash(db.Model):
    __tablename__ = "socialdash"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    likes = db.Column(db.Integer)
    views = db.Column(db.Integer)
    share = db.Column(db.Integer)
    comment = db.Column(db.Integer)
    category = db.Column(db.Text)
    engagments = db.Column(db.Float)


