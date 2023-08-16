from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
class AdjustTemp(FlaskForm):
    MaxInt = StringField("Threshold for Internal Temperature ",validators=[DataRequired()])
    MaxOut = StringField("Threshold for External Temperature ",validators=[DataRequired()])
    Submit = SubmitField("Submit")