import functools
import mysql.connector
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from trial2.user import login_required
from trial2.models import Model1

bp = Blueprint('seeker', __name__, url_prefix='/seeker')
#table connections
model3=Model1()
model3.connect(host='localhost', user='root', password='Mysql@123', database='db3')


@bp.route('/generalseek', methods=('GET', 'POST'))
@login_required
def generalseek():
    return render_template('seeker/dashboard.html')

@bp.route('/generalseek/checkfill', methods=('GET', 'POST'))
@login_required
def checkfill():
    user_id = g.user[0]  # Assuming g.user contains the current user's information
    
    # Check if there are any education details associated with the user
    cursor = model3.get_cursor()
    cursor.execute('SELECT * FROM education_detail WHERE user_account_id = %s', (user_id,))
    education_details = cursor.fetchall()
    cursor.execute('SELECT * FROM experience_detail WHERE user_account_id = %s', (user_id,))
    experience_details = cursor.fetchall()
    cursor.execute('SELECT * FROM skill_set WHERE user_account_id = %s', (user_id,))
    skill_details = cursor.fetchall()
    cursor.close()

    # If education details exist, render the experience page, else render the education details page
    if education_details and experience_details and skill_details:
        return redirect(url_for('seeker.generalseek'))
    elif education_details and experience_details:
        return redirect(url_for('seeker.skillselect'))
    elif education_details:
        return redirect(url_for('seeker.filldtls'))
    else:
        return redirect(url_for('seeker.buildprofile'))
    

@bp.route("/progress", methods=["GET"])
@login_required
def progress():
    user_id = g.user[0]  # Assuming g.user contains the current user's information

    # Check if there are any education details associated with the user
    cursor = model3.get_cursor()
    cursor.execute('SELECT * FROM education_detail WHERE user_account_id = %s', (user_id,))
    education_details = cursor.fetchall()

    # Check if there are any experience details associated with the user
    cursor.execute('SELECT * FROM experience_detail WHERE user_account_id = %s', (user_id,))
    experience_details = cursor.fetchall()

    # Check if there are any skill details associated with the user
    cursor.execute('SELECT * FROM skill_set WHERE user_account_id = %s', (user_id,))
    skill_details = cursor.fetchall()


    cursor.close()

    # Return the result as a JSON response
    return jsonify({
        "educationDetails": bool(education_details),
        "experienceDetails": bool(experience_details),
        "skillDetails": bool(skill_details)
    })

@bp.route('/buildprofile', methods=('GET', 'POST'))
@login_required

def buildprofile():
    if request.method == 'POST':
        # Retrieve form data
        degree = request.form['degree']
        major = request.form['major']
        university = request.form['university']
        start_date = request.form['st_date']
        end_date = request.form['end_date']
        percentage = request.form['percentage']
        cgpa = request.form['cgpa']

        # Insert data into the database
       
        cursor = model3.get_cursor()
        cursor.execute(
            'INSERT INTO education_detail (user_account_id, certificate_degree_name, major, institute_university_name, start_date, completion_date, percentage, cgpa) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (g.user[0], degree, major, university, start_date, end_date, percentage, cgpa)
        )

        model3.commit()  # Commit the transaction
        cursor.close()

        # Redirect to a success page or any other page
        return redirect(url_for('seeker.filldtls'))

    return render_template('seeker/edudet.html')


@bp.route('/filldtls', methods=('GET', 'POST'))
@login_required
def filldtls():
    if request.method == 'POST':
        # Get form data
        user_id = g.user[0]  # Assuming g.user contains the current user's information
        is_current_job = int(request.form.get('is_current_job'))
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        job_title = request.form.get('job_title')
        company_name = request.form.get('company_name')
        job_location_city = request.form.get('job_location_city')
        job_location_state = request.form.get('job_location_state')
        job_location_country = request.form.get('job_location_country')
        current_salary = request.form.get('current_salary')
        is_annually_monthly = request.form.get('is_annually_monthly')
        currency = request.form.get('currency')

        description = request.form.get('description')

        # Insert data into the experience_detail table
        cursor = model3.get_cursor()

        cursor.execute('INSERT INTO job_seeker_profile (user_account_id, first_name, last_name, current_salary, is_annually_monthly, currency) VALUES (%s, %s, %s, %s, %s, %s)'
                      ,(user_id, first_name, last_name, current_salary, is_annually_monthly, currency))


        cursor.execute('INSERT INTO experience_detail (user_account_id, is_current_job, start_date, end_date, job_title, company_name, job_location_city, job_location_state, job_location_country, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (user_id, is_current_job, start_date, end_date, job_title, company_name, job_location_city, job_location_state, job_location_country, description))
        model3.commit()  # Commit the transaction
        cursor.close()

        # Redirect to another page or render a template
        return redirect(url_for('seeker.skillselect'))

    return render_template('seeker/experience.html')

def get_skills():
    cursor = model3.get_cursor()
    cursor.execute("SELECT skill_set_name FROM seeker_skill_set")
    skills = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    return skills

@bp.route('/skillselect', methods=('GET', 'POST'))
@login_required
def skillselect():
    if request.method == 'POST':
        selected_skills = request.form.getlist('skill')
        user_account_id = g.user[0]  # Assuming g.user contains the current user's information
        
        if selected_skills:
            cursor = model3.get_cursor()
            
             # Prepare a string with placeholders for each selected skill
            placeholders = ', '.join(['%s'] * len(selected_skills))
            # Execute the query with the selected skills
            cursor.execute("SELECT id FROM seeker_skill_set WHERE skill_set_name IN ({})".format(placeholders), selected_skills)
            skill_ids = [result[0] for result in cursor.fetchall()]
            
            # Insert selected skill set IDs into the skill_set table
            for skill_id in skill_ids:
                cursor.execute("INSERT INTO skill_set (user_account_id, skill_set_id, skill_level) VALUES (%s, %s, %s)",
                               (user_account_id, skill_id, 1))  # Assuming skill level is always 1 for simplicity
            
            model3.commit()
            cursor.close()
            
            return redirect(url_for('seeker.generalseek'))
    
    skills = get_skills()  # You need to implement the get_skills function to fetch skill set names
    return render_template('seeker/skill.html', skills=skills)

@bp.route('/update_profile', methods=('GET', 'POST'))
@login_required
def update_profile():
    return render_template('seeker/profile.html')

