from flask import Flask, request, render_template_string, redirect, url_for, abort, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Initialize database
def init_db():
    try:
        conn = sqlite3.connect('challenge.db')
        cursor = conn.cursor()
        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS secrets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            secret_flag TEXT NOT NULL
        );
        INSERT OR IGNORE INTO users (username, password) VALUES ('admin', '9lM7O6GvHGD8pYansHvFyQnlGTuLtI'), ('user', 'user123');
        INSERT OR IGNORE INTO secrets (id, secret_flag) VALUES (1, 'i-CES{4dmIn_4cC3s5_9r4n73D}');
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            conn = sqlite3.connect('challenge.db')
            cursor = conn.cursor()

            # Vulnerable query
            query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            result = cursor.execute(query).fetchone()

            if result:
                user_role_query = f"SELECT username FROM users WHERE username='{username}'"
                user_role = cursor.execute(user_role_query).fetchone()[0]
                session['username'] = username

                if user_role == 'admin':
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('home'))
            else:
                return '<h1 class="text-center mt-5 text-danger">Login failed!</h1>'

            conn.close()
        except Exception as e:
            print(f"Error: {e}")
            return '<h1 class="text-center mt-5 text-danger">Internal Server Error</h1>'

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <div class="card">
                <div class="card-header text-center">
                    <h4>Login</h4>
                </div>
                <div class="card-body">
                    <form method="POST" action="/login">
                        <div class="mb-3">
                            <label for="username" class="form-label">Username</label>
                            <input type="text" class="form-control" id="username" name="username" required>
                        </div>
                        <div class="mb-3">
                            <label for="password" class="form-label">Password</label>
                            <input type="password" class="form-control" id="password" name="password" required>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">Login</button>
                    </form>
                </div>
            </div>
        </div>
    </body>
    <!--Use user and user123 for login find for the admin user password-->
    </html>
    ''')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Removes the session username
    return redirect(url_for('login'))  # Redirects to login page


@app.route('/home')
def home():
    if not is_user():
        return redirect(url_for('login'))
    
    # List of pages and their descriptions
    pages = [
        {'name': 'Home', 'url': url_for('home'), 'description': 'Welcome to the homepage'},
        {'name': 'About', 'url': url_for('about'), 'description': 'Learn more about us'},
        {'name': 'Project', 'url': url_for('project'), 'description': 'View our projects'},
        {'name': 'Contact', 'url': url_for('contact'), 'description': 'Get in touch with us'},
        {'name': 'Description', 'url': url_for('description'), 'description': 'Page for detailed descriptions'}
    ]
    
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Home</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="container-fluid">
                <a class="navbar-brand" href="{{ url_for('home') }}">Navbar</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link active" href="{{ url_for('home') }}">home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('about') }}">About</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('project') }}">Project</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('contact') }}">Contact</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('description') }}">Description</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('logout') }}">Logout</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
        
        <div class="container mt-5">
            <h3 class="text-center">Summary</h3>
            <div class="list-group">
                {% for page in pages %}
                    <a href="{{ page.url }}" class="list-group-item list-group-item-action">
                        <h5 class="mb-1">{{ page.name }}</h5>
                        <p class="mb-1">{{ page.description }}</p>
                    </a>
                {% endfor %}
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.min.js"></script>
    </body>
    </html>
    ''', pages=pages)



@app.route('/description', methods=['GET'])
def description():
    if not (is_user() or is_admin()):
        return redirect(url_for('login'))  # Forbidden

    # Allow users to input a custom SQL query
    user_query = request.args.get('query', '')
    if user_query:
        query = user_query
    else:
        # Default content to display when no query is provided
        cybersecurity_info = """
        Cybersecurity is a critical field in today's world, focusing on protecting systems, networks, and data 
        from digital attacks, theft, and damage. With the rise of digital transformation, organizations face 
        increasing challenges in securing sensitive information and maintaining secure systems.
        """
        # Render the static cybersecurity content
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Cybersecurity Vulnerabilities</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <a class="navbar-brand" href="{{ url_for('home') }}">Navbar</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link active" href="{{ url_for('home') }}">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('about') }}">About</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('project') }}">Project</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('contact') }}">Contact</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('description') }}">description</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('logout') }}">Logout</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
            <div class="container mt-5">
                <h3 class="text-center">Description</h3>
                <div class="alert alert-info" role="alert">
                    {{ cybersecurity_info }}
                </div>
            </div>
        <div class="container mt-5">
    <h3 class="text-center">Cybersecurity Vulnerabilities</h3>
    <p>Key aspects include:</p>
    <ul>
        <li>Preventing unauthorized access to data</li>
        <li>Securing networks from threats</li>
        <li>Ensuring data integrity and privacy</li>
        <li>Responding to incidents efficiently</li>
    </ul>
    <p>Continuous education, the implementation of best practices, and adopting robust security measures are essential to safeguarding digital assets.</p>

    <h4 class="mt-4">Common Web Vulnerabilities</h4>
    <table class="table table-bordered">
        <thead>
            <tr>
                <th>Vulnerability</th>
                <th>Description</th>
                <th>Risk</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>SQL Injection</td>
                <td>Attacks where malicious SQL statements are injected into database queries via web application input fields.</td>
                <td>Severe</td>
            </tr>
            <tr>
                <td>Cross-Site Scripting (XSS)</td>
                <td>A vulnerability where an attacker injects malicious scripts into web pages viewed by other users.</td>
                <td>Moderate</td>
            </tr>
            <tr>
                <td>Cross-Site Request Forgery (CSRF)</td>
                <td>An attack where a malicious site tricks the user into performing an action on another site where they are authenticated.</td>
                <td>High</td>
            </tr>
            <tr>
                <td>Authentication Bypass</td>
                <td>Exploiting flaws in authentication mechanisms to gain unauthorized access to systems.</td>
                <td>Severe</td>
            </tr>
            <tr>
                <td>Server-Side Request Forgery (SSRF)</td>
                <td>Attacks where the server is manipulated into making unauthorized requests to other internal or external systems.</td>
                <td>High</td>
            </tr>
            <tr>
                <td>Flag:</td><td>i-CES{CH4l13N9E_8Y_0xZ3r08y73}</td><td>HIGH</td>
            </tr>
            <tr>
                <td>Insecure Direct Object References (IDOR)</td>
                <td>Exploiting flaws in an application where user access to specific objects is not properly managed.</td>
                <td>Moderate</td>
            </tr>
            <tr>
                <td>Security Misconfigurations</td>
                <td>Errors in the configuration of security settings that can lead to vulnerabilities.</td>
                <td>High</td>
            </tr>
        </tbody>
    </table>
</div>

<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.min.js"></script>
</body>
</html>
        ''', cybersecurity_info=cybersecurity_info)

    try:
        conn = sqlite3.connect('challenge.db')
        cursor = conn.cursor()
        results = cursor.execute(query).fetchall()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
        abort(500)  # Internal Server Error

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>description</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
                                  <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="container-fluid">
                <a class="navbar-brand" href="{{ url_for('home') }}">Navbar</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link active" href="{{ url_for('home') }}">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('about') }}">About</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('project') }}">Project</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('contact') }}">Contact</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('description') }}">description</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('logout') }}">Logout</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
        
        <div class="container mt-5">
            <h3 class="text-center">description</h3>
            <div class="alert alert-danger" role="alert">
                Union attack performed! Here are the results:
            </div>
            <ul class="list-group mt-3">
                {% for user, password in users %}
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    {{ user }}
                    <span class="badge bg-primary rounded-pill">{{ password }}</span>
                </li>
                {% endfor %}
            </ul>
        </div>
    </body>
    </html>
    ''', users=results)


@app.route('/admin', methods=['GET'])
def admin_dashboard():
    if not is_admin():
        abort(403)  # Forbidden

    conn = sqlite3.connect('challenge.db')
    cursor = conn.cursor()

    try:
        secret_query = "SELECT secret_flag FROM secrets WHERE id=1"
        secret_flag = cursor.execute(secret_query).fetchone()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
        abort(500)  # Internal Server Error

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h3 class="text-center">Admin Dashboard</h3>
            <div class="alert alert-success text-center" role="alert">
                {{ secret_flag }}
            </div>
        </div>
    </body>
    </html>
    ''', secret_flag=secret_flag[0])


@app.route('/about')
def about():
    if not is_user():
        return redirect(url_for('login'))
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>About</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="container-fluid">
                <a class="navbar-brand" href="{{ url_for('home') }}">Navbar</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link active" href="{{ url_for('home') }}">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('about') }}">about</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('project') }}">Project</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('contact') }}">Contact</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('description') }}">Description</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('logout') }}">Logout</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
        
        <div class="container mt-5">
            <h3 class="text-center">About</h3>
            <div class="card">
                <div class="card-body">
                    <p>Innovative Computer Engineering Students' Society (i-CES) is established with the strong motive to educate, promote, explore ,research and compete in the field of Computer Engineering. It has been providing platform to students who show keen interest in Computer programming and related projects.It also conducts seminars, presentations, documentaries shows and Competitions timely with aim to enhance the engineering skill of technical students in more practical way.When its about National and Local level Programming competitions,Innovative Computer Engineer's Society (i-CES) is one of the best representative of Western Region Campus.</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/project')
def project():
    if not is_user():
        return redirect(url_for('login'))
    return render_template_string('''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>9 Cards</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <a class="navbar-brand" href="{{ url_for('home') }}">Navbar</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link active" href="{{ url_for('home') }}">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('about') }}">About</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('project') }}">project</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('contact') }}">Contact</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('description') }}">Description</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('logout') }}">Logout</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    
    <div class="container mt-5">
        <h3 class="text-center">9 Cards</h3>
        <div class="row">
            <div class="col-md-4 mb-4">
                <div class="card">
                    <div class="card-body">
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam scelerisque erat a nulla cursus.</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="card">
                    <div class="card-body">
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam scelerisque erat a nulla cursus.</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="card">
                    <div class="card-body">
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam scelerisque erat a nulla cursus.</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="card">
                    <div class="card-body">
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam scelerisque erat a nulla cursus.</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="card">
                    <div class="card-body">
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam scelerisque erat a nulla cursus.</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="card">
                    <div class="card-body">
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam scelerisque erat a nulla cursus.</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="card">
                    <div class="card-body">
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam scelerisque erat a nulla cursus.</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="card">
                    <div class="card-body">
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam scelerisque erat a nulla cursus.</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="card">
                    <div class="card-body">
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam scelerisque erat a nulla cursus.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>

    ''')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if not is_user():
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Contact</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="container-fluid">
                <a class="navbar-brand" href="{{ url_for('home') }}">Navbar</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link active" href="{{ url_for('home') }}">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('about') }}">About</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('project') }}">Project</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('contact') }}">contact</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('description') }}">Description</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('logout') }}">Logout</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>

        <div class="container mt-5">
            <h3 class="text-center">Contact</h3>
            <div class="card">
                <div class="card-body">
                    <p>Contact us at 
                        <br>Paschimanchal Campus, Lamachaur, Pokhara, Nepal
                        <br>icesnepal@gmail.com
                    </p>
                    <form action="{{ url_for('contact') }}" method="POST">
                        <div class="mb-3">
                            <label for="name" class="form-label">Name</label>
                            <input type="text" class="form-control" id="name" name="name" required>
                        </div>
                        <div class="mb-3">
                            <label for="email" class="form-label">Email</label>
                            <input type="email" class="form-control" id="email" name="email" required>
                        </div>
                        <div class="mb-3">
                            <label for="message" class="form-label">Message</label>
                            <textarea class="form-control" id="message" name="message" rows="4" required></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary">Send</button>
                    </form>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.min.js"></script>
    </body>
    </html>
    ''')



def is_admin():
    conn = sqlite3.connect('challenge.db')
    cursor = conn.cursor()
    username = session.get('username')
    if username:
        user_role_query = f"SELECT username FROM users WHERE username='{username}' AND username='admin'"
        result = cursor.execute(user_role_query).fetchone()
        conn.close()
        return result is not None
    conn.close()
    return False

def is_user():
    conn = sqlite3.connect('challenge.db')
    cursor = conn.cursor()
    username = session.get('username')
    if username:
        user_role_query = f"SELECT username FROM users WHERE username='{username}'"
        result = cursor.execute(user_role_query).fetchone()
        conn.close()
        return result is not None
    conn.close()
    return False

if __name__ == '__main__':
    init_db()
    app.run(debug=False)
