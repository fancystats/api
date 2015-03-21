from flask import Flask

app = Flask(__name__)
app.config.from_object('api.config.Config')
app.config.from_envvar('FANCYSTATS_SETTINGS', silent=True)
