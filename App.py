from flask import Flask, render_template

app = Flask(__name__)

# Route for the Home Page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/')
def booking():
    return render_template('booking.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
