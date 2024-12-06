def forms():
    print("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Form</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .error {
            color: red;
            font-size: 0.9em;
        }
    </style>
</head>
<body>

    <div class="container mt-5">
        <h2 class="text-center text-primary mb-4 display-4">Contact Form</h2>
        <form id="contactForm">
            <div class="mb-3">
                <label for="fullName" class="form-label">Full Name:</label>
                <input type="text" class="form-control" id="fullName" name="fullName" maxlength="25">
                <div class="error" id="nameError"></div>
            </div>

            <div class="mb-3">
                <label for="email" class="form-label">Email:</label>
                <input type="email" class="form-control" id="email" name="email" maxlength="30">
                <div class="error" id="emailError"></div>
            </div>

            <div class="mb-3">
                <label for="phone" class="form-label">Phone Number:</label>
                <input type="text" class="form-control" id="phone" name="phone" maxlength="25">
                <div class="error" id="phoneError"></div>
            </div>

            <div class="mb-3">
                <button type="submit" class="btn btn-primary">Submit</button>
                <button type="reset" class="btn btn-secondary" onclick="resetForm()">Reset</button>
            </div>
        </form>
    </div>

    <!-- Bootstrap JS (with Popper) -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.getElementById('contactForm').addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the default form submission

            // Clear previous error messages
            document.getElementById('nameError').innerText = '';
            document.getElementById('emailError').innerText = '';
            document.getElementById('phoneError').innerText = '';

            // Get input values
            const fullName = document.getElementById('fullName').value.trim();
            const email = document.getElementById('email').value.trim();
            const phone = document.getElementById('phone').value.trim();

            // Validation flags
            let isValid = true;

            // Name validation
            if (fullName === '' || fullName.length < 2) {
                document.getElementById('nameError').innerText = 'Full Name must be at least 2 characters long.';
                isValid = false;
            }

            // Email validation
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (email === '' || !emailPattern.test(email)) {
                document.getElementById('emailError').innerText = 'Please enter a valid email address.';
                isValid = false;
            }

            // Phone number validation
            const phonePattern = /^\d+$/;
            if (phone === '' || !phonePattern.test(phone)) {
                document.getElementById('phoneError').innerText = 'Phone Number must contain only digits.';
                isValid = false;
            }

            // If valid, show success message (can be replaced with actual submission logic)
            if (isValid) {
                alert('Form submitted successfully!');
            }
        });

        function resetForm() {
            document.getElementById('nameError').innerText = '';
            document.getElementById('emailError').innerText = '';
            document.getElementById('phoneError').innerText = '';
        }
    </script>

</body>
</html>
""")
    return

def booklist():
    print("""Book.js
import "../App.css";

function Book({ title, author, price, image_path }) {
  return (
    <div class="book">
      <img src={image_path} alt={title} />
      <h2>{title}</h2>
      <h3>{author}</h3>
      <h4>{price}</h4>
    </div>
  );
}

export default Book;


BooksList.js
import Book from "./Book";
import "../App.css";

function BookList({ books }) {
  return (
    <div class="bookslist">
      {books.map((book) => (
        <Book
          title={book.title}
          author={book.author}
          price={book.price}
          image_path={book.image_path}
        />
      ))}
    </div>
  );
}

export default BookList;


App.js
import BookList from "./components/BookList";
import "./App.css";

function App() {
  const books = [
    {
      title: "The Alchemist",
      author: "Paulo Coelho",
      price: "$10",
      image_path:
        "https://m.media-amazon.com/images/I/61HAE8zahLL._AC_UF1000,1000_QL80_.jpg",
    },
    {
      title: "The Little Prince",
      author: "Antoine de Saint-Exupéry",
      price: "$15",
      image_path:
        "https://m.media-amazon.com/images/I/61NGp-UxolL._AC_UF1000,1000_QL80_.jpg",
    },
    {
      title: "The Book Thief",
      author: "Markus Zusak",
      price: "$12",
      image_path:"https://m.media-amazon.com/images/I/91JGwQlnu7L._AC_UF1000,1000_QL80_.jpg",
    },
  ];

  return (
    <div class="App">
      <h1 class="header">Bookstore</h1>
      <BookList books={books} />
    </div>
  );
}

export default App;


App.css
.bookslist {
  display: flex;
  flex-wrap: wrap;
  color: #333;
}

.header {
  background-color: #333;
  color: #fff;
  padding: 10px;
  text-align: center;
  border-radius: 5px;
}

.book {
  width: 30%;
  text-align: center;
  margin: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
}

.book img {
  width: 50%;
  height: auto;
}

.App {
  font-family: "Trebuchet MS", "Lucida Sans Unicode", "Lucida Grande",
    "Lucida Sans", Arial, sans-serif;
}

""")
    return

def callback():
    print("""function step1(){
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            console.log("Order placed successfully");
            resolve();
        }, 2000);
    });
}

function step2(){
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            console.log("Payment processed successfully");  
            resolve();
        }, 4000);
    });
}

function step3(){
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            console.log("Order being prepared");
            resolve();
        }, 3000);
    });
}

function finalStep(){
    console.log("Order delivered successfully");
}

step1()
    .then(() => {
        return step2();
    })
    .then(() => {
        return step3();
    })
    .then(() => {
        return finalStep();
    })
    .catch((err) => {
        console.log(err);
    });

console.log("Other services are running in the background");



/*  */
function step1(){
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            console.log("Order placed successfully");
            resolve();
        }, 2000);
    });
}

function step2(){
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            console.log("Payment processed successfully");  
            resolve();
        }, 4000);
    });
}

function step3(){
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            console.log("Order being prepared");
            resolve();
        }, 3000);
    });
}

function finalStep(){
    console.log("Order delivered successfully");
}

async function main() {
    try {
        await step1();
        await step2();
        await step3();
        finalStep();
    } catch (err) {
        console.log(err);
    }
}
main();
console.log("Other services are running in the background");


/*  */
const delay = (message, time) =>
  new Promise((resolve) =>
    setTimeout(() => {
      console.log(message);
      resolve();
    }, time)
  );

async function processOrder() {
  try {
    await delay("Step 1: Order placed successfully", 2000);
    await delay("Step 2: Payment processed", 4000);
    await delay("Step 3: Order being prepared", 3000);
    console.log("Step 4: Order delivered! Enjoy your meal!");
  } catch (error) {
    console.log("Something went wrong:", error);
  }
}

processOrder();
console.log("Other services are running in the background... bye!");

""")
    return

def sql():
    print("""CREATE TABLE employee (
    eid INT PRIMARY KEY,
    fname VARCHAR(50) NOT NULL,
    lname VARCHAR(50) NOT NULL,
    doj DATE NOT NULL,
    salary DECIMAL(10, 2) NOT NULL
);

INSERT INTO employee (eid, fname, lname, doj, salary) VALUES
(1, 'Amit', 'Sharma', '2020-02-10', 55000.00),
(2, 'Priya', 'Rao', '2019-05-20', 66000.00),
(3, 'Vikas', 'Patel', '2021-11-01', 48000.00),
(4, 'Sonia', 'Nair', '2018-07-15', 82500.00),
(6, 'Suresh', 'Verma', '2021-09-01', 72000.00),
(7, 'Deepika', 'Iyer', '2017-12-12', 93500.00),
(8, 'Rohit', 'Gupta', '2018-01-05', 75900.00),
(9, 'Pooja', 'Malhotra', '2020-06-18', 52000.00);

UPDATE employee 
SET salary = salary * 1.10 
WHERE eid = 4;


DELETE FROM employee 
WHERE eid = 3;


UPDATE employee 
SET salary = salary * 1.10 
WHERE doj < '2020-01-01';


SELECT fname, lname, salary 
FROM employee 
ORDER BY salary DESC 
LIMIT 3;


SELECT fname, lname, salary 
FROM employee 
WHERE salary > (SELECT AVG(salary) FROM employee);
""")
    return

def docker():
    print("""Dockerfile:
# Use the official Python image
FROM python:3.12
# Set the working directory
WORKDIR /app
# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt
# Copy the project files
COPY . /app/
# Run Django's development server on port 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
Settings.py

Django settings for myproject project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/


from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-kq&wh#z6pxalkoc9u!9xv5!p$*-v$8wj#6kx@*%l40r)4m8i)a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'mydb'),
        'USER': os.getenv('DB_USER', 'myuser'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'mypassword'),
        'HOST': os.getenv('DB_HOST', 'mysql-db'),  # Hostname of the MySQL container
        'PORT': '3306',  # Port mapped for MySQL on host
    }
}
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = 'static/'
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
""")
    return
def form_django():
    print("""models.py

from django.db import models

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    date_of_joining = models.DateField()
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

forms.py
from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'date_of_joining', 'salary', 'position']

views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from .forms import EmployeeForm

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

def employee_create(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employee_form.html', {'form': form})

def employee_update(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee_form.html', {'form': form})

def employee_delete(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == "POST":
        employee.delete()
        return redirect('employee_list')
    return render(request, 'employee_confirm_delete.html', {'employee': employee})


urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('create/', views.employee_create, name='employee_create'),
    path('update/<int:id>/', views.employee_update, name='employee_update'),
    path('delete/<int:id>/', views.employee_delete, name='employee_delete'),
]


templates/employee_list.html
<!DOCTYPE html>
<html>
<head>
    <title>Employee List</title>
</head>
<body>
    <h1>Employee List</h1>
    <table border="1">
        <tr>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Email</th>
            <th>Date of Joining</th>
            <th>Salary</th>
            <th>Position</th>
            <th>Actions</th>
        </tr>
        {% for employee in employees %}
        <tr>
            <td>{{ employee.first_name }}</td>
            <td>{{ employee.last_name }}</td>
            <td>{{ employee.email }}</td>
            <td>{{ employee.date_of_joining }}</td>
            <td>{{ employee.salary }}</td>
            <td>{{ employee.position }}</td>
            <td>
                <a href="{% url 'employee_update' employee.id %}">Edit</a>
                <a href="{% url 'employee_delete' employee.id %}">Delete</a>
            </td>
        </tr>
        {% empty %}
        <tr>
            <td colspan="7">No employees found.</td>
        </tr>
        {% endfor %}
    </table>
    <a href="{% url 'employee_create' %}">Add New Employee</a>
</body>
</html>


templates/employee_form.html
<!DOCTYPE html>
<html>
<head>
    <title>Employee Form</title>
</head>
<body>
    <h1>{{ employee.id|default:"New Employee" }}</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Save</button>
    </form>
    <a href="{% url 'employee_list' %}">Back to List</a>
</body>
</html>


templates/employee_confirm_delete.html
<!DOCTYPE html>
<html>
<head>
    <title>Delete Employee</title>
</head>
<body>
    <h1>Are you sure you want to delete {{ employee.first_name }} {{ employee.last_name }}?</h1>
    <form method="post">
        {% csrf_token %}
        <button type="submit">Yes, Delete</button>
    </form>
    <a href="{% url 'employee_list' %}">Cancel</a>
</body>
</html>


myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_name.urls')),  # Replace 'app_name' with the name of your app
]
""")
    return
def ML():
    print("""Models.py
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

glass = fetch_openml(name = "glass", version = 1)
X = glass.data
y = glass.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators = 100, random_state = 42)
model.fit(X_train, y_train)

joblib.dump(model, 'glass_classification_model.pkl')

Views.py
from django.shortcuts import render
from .forms import GlassPredictionForm
import joblib

def predict_glass_type(request):
    prediction = None
    if request.method == 'POST':
        form = GlassPredictionForm(request.POST)
        if form.is_valid():
            model = joblib.load('glass_classification_model.pkl')

            features = form.get_features_as_array()

            prediction = model.predict(features)[0]
    else:
        form = GlassPredictionForm()

    return render(request, 'Prediction.html', {'form': form, 'prediction': prediction})

Forms.py
from django import forms
import numpy as np

class GlassPredictionForm(forms.Form):
    feature_1 = forms.FloatField(label="RI")
    feature_2 = forms.FloatField(label="Na")
    feature_3 = forms.FloatField(label="Mg")
    feature_4 = forms.FloatField(label="Al")
    feature_5 = forms.FloatField(label="Si")
    feature_6 = forms.FloatField(label="K")
    feature_7 = forms.FloatField(label="Ca")
    feature_8 = forms.FloatField(label="Ba")
    feature_9 = forms.FloatField(label="Fe")

    def get_features_as_array(self):
        # Manually collect values from the form fields
        features = np.array([
            self.cleaned_data['feature_1'],
            self.cleaned_data['feature_2'],
            self.cleaned_data['feature_3'],
            self.cleaned_data['feature_4'],
            self.cleaned_data['feature_5'],
            self.cleaned_data['feature_6'],
            self.cleaned_data['feature_7'],
            self.cleaned_data['feature_8'],
            self.cleaned_data['feature_9']
        ])
        return features.reshape(1, -1)

Prediction.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Glass Type Prediction</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            display: flex;
            gap: 20px;
        }
        .form-container, .result-container {
            flex: 1;
        }
        form {
            display: grid;
            gap: 10px;
        }
        label {
            font-weight: bold;
        }
        .result-container {
            padding: 20px;
            background-color: #f0f0f0;
            border: 1px solid #ccc;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="form-container">
            <h1>Glass Type Prediction</h1>
            <form method="POST">
                {% csrf_token %}
                {{ form.as_p }}
                <div>
                    <button type="submit">Predict</button>
                </div>
            </form>
        </div>
        
        <div class="result-container">
            {% if prediction %}
            <h2>Prediction Result:</h2>
            <p>The predicted glass type is: <strong>{{ prediction }}</strong></p>
            {% else %}
            <p>Enter values and click Predict to see the result.</p>
            {% endif %}
        </div>
    </div>
</body>
</html>     
""")
    return

def portfolio():
    print("""my_view.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My View</title>

    <!-- Load the static template tag library -->
    {% load static %}

    <!-- Link to the external stylesheet -->
    <link rel="stylesheet" href="{% static 'css/styles.css' %}">
</head>
<body>
    <h1>Welcome to Tom's Portfolio</h1>

    <!-- Displaying personal information from the dictionary -->
    <h2>About Tom:</h2>
    <p>Name: {{ my_dict.name }}</p>
    <p>Age: {{ my_dict.age }}</p>
    <p>City: {{ my_dict.city }}</p>

    <!-- Displaying the list of items (projects, skills, etc.) -->
    <h2>Projects and Skills</h2>
    <ul>
        {% for item in itemList %}
        <li>{{ item }}</li>
        {% endfor %}
    </ul>
</body>
</html>

 
indexstatic.html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Tom's Portfolio</title>
    <link rel="stylesheet" href="{% static 'css/styles.css' %}" />
    <script src="{% static 'js/scripts.js' %}" defer></script>
  </head>
  <body>
    <div class="container">
      <h1>Welcome to Tom's Portfolio</h1>

      <p id="greeting-message">Feel free to explore!</p>

      <!-- Button to trigger the greeting update -->
      <button onclick="showGreeting()">Click me for a greeting</button>
    </div>
  </body>
</html>


 
script.js
// Alert users when they visit the site
window.onload = function () {
  alert("Welcome to Tom's Portfolio!");
};

// Additional feature: dynamically update content when clicking a button
function showGreeting() {
  const message = document.getElementById("greeting-message");
  message.innerText = "Thanks for visiting!";
}


 
styles.css
/* General styles for the body */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 20px;
  background-color: #f4f4f4;
  color: #333;
}

/* Styling the h1 headings */
h1 {
  color: #2c3e50;
  font-size: 2.5rem;
  text-align: center;
  margin-bottom: 20px;
}

/* Styling the h2 subheadings */
h2 {
  color: #2980b9;
  font-size: 1.8rem;
  margin-bottom: 15px;
}

/* Styling the unordered list items */
ul {
  list-style-type: square;
  padding-left: 20px;
}

li {
  font-size: 1.2rem;
  margin-bottom: 10px;
}

/* Styling images to have rounded corners */
img {
  border-radius: 15px;
  max-width: 100%;
  height: auto;
  display: block;
  margin: 0 auto 20px;
}

/* Styling for a responsive container */
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}


 
views.py
from django.shortcuts import render

def my_view(request):
    items = ["Project A", "Skill B", "Project C", "Skill D"]
    my_dict = {"name": "Tom", "age": 30, "city": "New York"}

    context = {
        "author": "Rajiv Gupta",
        "data": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "itemList": items,
        "my_dict": my_dict,
    }

    return render(request, 'my_view.html', context)


 
myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('portfolio', views.my_view, name='my_view'),
]

 
myproject.urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('myapp/', include('myapp.urls')),
]





""")
    return

def regform():
    print("""App.js
import React from "react";
import RegistrationForm from "./RegistrationForm";
import "./App.css"; // We'll create a separate CSS file for styling

function App() {
  return (
    <div className="app-container">
      <h1>Register</h1>
      <RegistrationForm />
    </div>
  );
}

export default App;


RegistrationForm.js
import React, { useState } from "react";

function RegistrationForm() {
  // Step 1: Set up the form fields state using useState hook
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  });

  // Step 2: Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  // Step 3: Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault(); // Prevent default form submission behavior
    alert(`Name: ${formData.name}\nEmail: ${formData.email}\nPassword: ${formData.password}`);
    
    // Reset form state after successful submission
    setFormData({
      name: "",
      email: "",
      password: "",
    });
  };

  return (
    <form className="registration-form" onSubmit={handleSubmit}>
      <div>
        <label htmlFor="name">Name:</label>
        <input
          type="text"
          id="name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
        />
      </div>

      <div>
        <label htmlFor="email">Email:</label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
        />
      </div>

      <div>
        <label htmlFor="password">Password:</label>
        <input
          type="password"
          id="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
        />
      </div>

      <button type="submit">Register</button>
    </form>
  );
}

export default RegistrationForm;


index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <App />
);

App.css
.app-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  font-family: Arial, sans-serif;
}

h1 {
  color: #333;
}

.registration-form {
  background-color: #f9f9f9;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  width: 100%;
}

.registration-form div {
  margin-bottom: 15px;
  margin-right: 15px;
}

.registration-form label {
  display: block;
  margin-bottom: 5px;
  color: #555;
}

.registration-form input {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

button:hover {
  background-color: #0056b3;
}

@media (max-width: 600px) {
  .registration-form {
    padding: 15px;
  }

  button {
    font-size: 14px;
  }
}

""")
    return


def sql_django():
    print("""Settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # Django REST Framework
    'employees',      # Your employee app
]
Employees/models.py
from django.db import models

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    date_joined = models.DateField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
employees/serializers.py
from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
employees/views.py
from rest_framework import viewsets
from .models import Employee
from .serializers import EmployeeSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
employees/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
employee_management/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('employees.urls')),
]
CRUD OPERATIONS
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "John@company.com",
    "department": "Finance",
    "date_joined": "2024-01-01"
}
""")