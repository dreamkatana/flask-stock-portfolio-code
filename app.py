from flask import Flask, escape, render_template, request, session, redirect, url_for

app = Flask(__name__)


# TEMPORARY - Set the secret key to a temporary value!
app.secret_key = 'BAD_SECRET_KEY'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html', company_name='TestDriven.io')


@app.route('/users/<username>')
def user_profile(username):
    return f'<h1>Welcome {escape(username)}!</h1>'


@app.route('/blog_posts/<int:post_id>')
def display_blog_post(post_id):
    return f'<h1>Blog Post #{post_id}...</h1>'


@app.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        # DEBUG - Print the form data to the console
        for key, value in request.form.items():
            print(f'{key}: {value}')

        # Save the form data to the session object
        session['stockSymbol'] = request.form['stockSymbol']
        session['numberOfShares'] = request.form['numberOfShares']
        session['sharePrice'] = request.form['sharePrice']
        return redirect(url_for('list_stocks'))
    else:
        return render_template('add_stock.html')


@app.route('/stocks')
def list_stocks():
    return render_template('stocks.html')
