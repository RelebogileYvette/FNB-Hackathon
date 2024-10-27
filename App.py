from flask import Flask, redirect, render_template

app = Flask(__name__)

# Route for the Home Page


@app.route('/')
def home():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup():return redirect('/options')

@app.route('/')
def booking():
    return render_template('booking.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/options')
def options():
    return render_template('options_to_select.html')




if __name__ == '__main__':
    app.run(debug=True)
