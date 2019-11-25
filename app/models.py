from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5


followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('authuser.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('authuser.id'))
)

#My Authuser Class for chapel photo db
class Authuser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='mb.jpg')
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    couples = db.relationship('Couple', backref='authuser', lazy=True) # See 16:10min YT
    wedding_package = db.relationship('Weddingpackage', backref='authuser', lazy=True)
    followed = db.relationship(
        'Authuser', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Authorized User('{self.username}', '{self.email}', '{self.image_file}')"

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Couple.query.join(
            followers, (followers.c.followed_id == Couple.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Couple.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Couple.timestamp.desc())

# Youtube CH6 Userauth 22:00 left off
@login.user_loader
def load_user(user_id):
    return Authuser.query.get(int(user_id))


class Couple(db.Model):   # Called Couple for initial record. Sometimes other ppl pay im calling them customers
    id = db.Column(db.Integer, primary_key=True)
    p1_first_name = db.Column(db.String(30), nullable=False)
    p1_surname = db.Column(db.String(100), nullable=False)
    p2_first_name = db.Column(db.String(30), nullable=False)
    p2_surname = db.Column(db.String(100), nullable=False)
    mail_street_address_1 = db.Column(db.String(100), nullable=True)
    mail_street_address_2 = db.Column(db.String(100), nullable=True)
    mail_city = db.Column(db.String(100), nullable=True)
    mail_state_province = db.Column(db.String(100), nullable=True)
    mail_country = db.Column(db.String(100), nullable=False)
    mail_postal_code = db.Column(db.String(30), nullable=False)
    email_p1 = db.Column(db.String(120), unique=True, nullable=True)
    email_p2 = db.Column(db.String(120), unique=True, nullable=True)
    telephone_number = db.Column(db.String(120), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    note = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('authuser.id'))
    # Above I believe this records who FK created the record https://youtu.be/cYWiDiIUxQc?t=919

    def __repr__(self):
        return f"Couple('{self.p1_first_name}', '{self.p1_surname}', '{self.p2_first_name}', '{self.p2_surname}' '{self.date_created}')"


class Weddingpackage(db.Model):   # Wedding Pkgs/ Need to make a pkg ie Earth Angel diff desc as needed overtime
    id = db.Column(db.Integer, primary_key=True)
    wedding_package = db.Column(db.String(60), nullable=False)
    wedding_package_desc = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('authuser.id'))
    # Above I believe this records who FK created the record https://youtu.be/cYWiDiIUxQc?t=919
    #couple_id = db.Column(db.Integer, db.ForeignKey('couple.id'), nullable=False)
    # Above I believe this records who FK created the record https://youtu.be/cYWiDiIUxQc?t=919
    ## client_id = db.Column(db.Integer, db.ForeignKey('couple.id'), nullable=False)
