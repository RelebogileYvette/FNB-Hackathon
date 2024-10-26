from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']  # Make sure to handle passwords securely in a production app
        role = request.form['role']  # 'client' or 'freelancer'

        # Here, you would typically add the user to your database
        # For now, redirect based on role for demonstration
        if role == 'client':
            return redirect(url_for('client_profile', username=name))
        elif role == 'freelancer':
            return redirect(url_for('freelancer_profile', username=name))
        
        # Handle unexpected role or error
        return "Invalid role selected", 400

    return render_template('signup.html')

@app.route('/profile/client/<username>')
def client_profile(username):
    # Render client-specific profile page
    return render_template('client_profile.html', username=username)

@app.route('/profile/freelancer/<username>')
def freelancer_profile(username):
    # Render freelancer-specific profile page
    return render_template('freelancer_profile.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)