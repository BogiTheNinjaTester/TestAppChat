from flask import Flask, render_template
from wtform_fields import *


app = Flask(__name__)
app.secret_key = 'replace later'

@app.route('/', methods=['GET', 'POST'])
def index():
    ''' TBD '''

    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        return 'Great success!'

    return render_template('index.html', form=registration_form)

if __name__ == "__main__":

    app.run(debug=True)
