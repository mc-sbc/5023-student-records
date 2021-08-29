import csv

from flask import render_template, request

from app import app

def load_staff():
    # A utility function to load the staff' grades from the csv file
    staff = []
    with open('staff.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            staff.append(row)
    return staff

@app.route('/')
def index():
    # Load the staff from the CSV file for the table
    staff = load_staff()
    # Return the index view with the list of staff for display
    return render_template('index.html', staff = staff)

@app.route('/add_compliance', methods = ['GET', 'POST'])
def add_staff():
    # Check if the form has been submitted (is a POST request)
    if request.method == 'POST':
        # Get data from the form and put in dictionary
        staff = {}
        staff['VIT'] = request.form.get('VIT') == 'on'
        staff['mandatory_rep'] = request.form.get('mandatory_rep') == 'on'

        # Load the staff from the CSV file and add the new staff
        staff = load_staff()
        staff.append(staff)

        # Open up the csv file and overwrite the contents
        with open('staff.csv', 'w', newline='') as file:
            fieldnames = ['name', 'VIT', 'mandatory_rep']
            writer = csv.DictWriter(file, fieldnames = fieldnames)
            writer.writeheader()
            writer.writerows(staff)
        
        # Returns the view with a message that the staff has been added
        return render_template('add_success.html', staff = staff)

    # When there is a GET request, the view with the form is returned
    return render_template('add_compliance.html')