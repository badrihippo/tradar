from itsdangerous import URLSafeTimedSerializer
from .. import app

ts = URLSafeTimedSerializer(app.config.get('SECRET_KEY'))
