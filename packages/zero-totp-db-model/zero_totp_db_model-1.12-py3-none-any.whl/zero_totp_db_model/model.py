
from .model_init import db

if db is None:
    raise Exception("Database not initialized. Please call init_db(db) before importing models")


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    mail = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    username = db.Column(db.String(256), nullable=False, unique=True)
    derivedKeySalt = db.Column(db.String(256), nullable=False)
    isVerified = db.Column(db.Boolean, nullable=False)
    passphraseSalt = db.Column(db.String(256), nullable=False)
    createdAt = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(256), nullable=False, default="user")
    isBlocked =  db.Column(db.Boolean, nullable=False, default=False)
    last_login_date = db.Column(db.String(20), nullable=True)


class ZKE_encryption_key(db.Model):
    __tablename__ = "ZKE_encryption_key"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    ZKE_key = db.Column(db.String(256), nullable=False)

class TOTP_secret(db.Model):
    __tablename__ = "totp_secret_enc"
    uuid = db.Column(db.String(256), primary_key=True, nullable=False, autoincrement=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    secret_enc = db.Column(db.Text, nullable=False)



class Oauth_tokens(db.Model):
    __tablename__ = "oauth_tokens"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    enc_credentials = db.Column(db.Text, nullable=False)
    cipher_nonce = db.Column(db.Text, nullable=False)
    cipher_tag = db.Column(db.Text, nullable=False)
    expires_at = db.Column(db.Integer, nullable=False)


class GoogleDriveIntegration(db.Model):
    __tablename__ = "google_drive_integration"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    isEnabled = db.Column(db.Boolean, nullable=False, default=False)
    lastBackupCleanDate = db.Column(db.String(256), nullable=True, default=None)


class Preferences(db.Model):
    __tablename__ = "preferences"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    favicon_preview_policy = db.Column(db.String(256), nullable=True, default="enabledOnly")
    derivation_iteration = db.Column(db.Integer, nullable=True, default=700000)
    minimum_backup_kept = db.Column(db.Integer, nullable=True, default=20)
    backup_lifetime = db.Column(db.Integer, nullable=True, default=30)
    vault_autolock_delay_min = db.Column(db.Integer, nullable=True, default=10)

class EmailVerificationToken(db.Model):
    __tablename__ = "email_verification_token"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False, unique=True)
    token = db.Column(db.String(256), nullable=False)
    expiration = db.Column(db.String(256), nullable=False)
    failed_attempts = db.Column(db.Integer, nullable=False, default=0)

class RateLimiting(db.Model):
    __tablename__ = "rate_limiting"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    ip = db.Column(db.String(45), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=True)
    action_type = db.Column(db.String(256), nullable=False) # send_verification_email, failed_login 
    timestamp = db.Column(db.DateTime, nullable=False)
    
class Notifications(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.String(36), primary_key=True, nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.String(20), nullable=False)
    enabled = db.Column(db.Boolean, nullable=False, default=True)
    expiry = db.Column(db.String(20), nullable=True, default=None)
    authenticated_user_only =  db.Column(db.Boolean, nullable=False, default=False)


class RefreshToken(db.Model):
    __tablename__ = "refresh_token"
    id = db.Column(db.String(36), primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    hashed_token = db.Column(db.String(64), nullable=False, unique=True)
    expiration = db.Column(db.String(20), nullable=False)
    session_token_id = db.Column(db.String(36), nullable=False)
    revoke_timestamp = db.Column(db.String(20), nullable=True, default=None)

class SessionToken(db.Model):
    __tablename__ = "session_token"
    id = db.Column(db.String(36), primary_key=True, nullable=False)
    token = db.Column(db.String(36), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    expiration = db.Column(db.String(20), nullable=False)
    revoke_timestamp = db.Column(db.String(20), nullable=True, default=None)