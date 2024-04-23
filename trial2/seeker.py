import functools
import mysql.connector
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from trial2.user import login_required
from trial2.models import Model1,Model2

bp = Blueprint('seeker', __name__, url_prefix='/seeker')
#table connections
model3=Model1()
model3.connect(host='localhost', user='root', password='Mysql@123', database='db3')
model4=Model2()
model4.connect(host='localhost', user='root', password='Mysql@123', database='db4')
    

@bp.route('/generalseek', methods=('GET', 'POST'))
@login_required
def generalseek():
    user_id = g.user[0]  # Assuming g.user[0] contains the user ID
    
    total_apps = get_total_appliedjobs(user_id)  # Function to retrieve total posts by user ID from the database

    
    return render_template('seeker/dashboard.html',total_apps=total_apps)

def get_total_appliedjobs(user_id):
    cursor = model4.get_cursor()
    query = "SELECT COUNT(*) FROM job_post_activity WHERE uacid = %s"
    cursor.execute(query, (user_id,))
    total_apps = cursor.fetchone()[0]  # Fetch the count from the first column of the first row
    cursor.close()  # Close cursor
    return total_apps

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
        skill_level = request.form.get('skill_level')
        skill_level_id = 1 if skill_level == 'Basic' else 2 if skill_level == 'Medium' else 3
        
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
                               (user_account_id, skill_id, skill_level_id))  # Assuming skill level is always 1 for simplicity
            
            model3.commit()
            cursor.close()
            
            return redirect(url_for('seeker.generalseek'))
    
    skills = get_skills()  # You need to implement the get_skills function to fetch skill set names
    return render_template('seeker/skill.html', skills=skills)

def getprofile(user_id):
    cursor = model3.get_cursor()
    query = """
        SELECT 
            jp.user_account_id,
            jp.first_name,
            jp.last_name,
            CONCAT(jp.current_salary, ', ', jp.currency, ', ', jp.is_annually_monthly) AS Salary,
            CONCAT(c.certificate_degree_name, ', ', c.major, ', ', c.institute_university_name) AS degree,
            c.percentage,
            c.cgpa,
            c.start_date,
            c.completion_date,
            l.description,
            l.is_current_job,
            l.start_date,
            l.end_date,
            l.job_title,
            l.job_location_city,
            l.job_location_country,
            l.job_location_state,
            s.skill_level,
            GROUP_CONCAT(f.skill_set_name) AS skill_set_names
        FROM 
            job_seeker_profile jp
        INNER JOIN
            education_detail c ON jp.user_account_id = c.user_account_id
        INNER JOIN 
            experience_detail l ON jp.user_account_id = l.user_account_id
        INNER JOIN 
            skill_set s ON jp.user_account_id = s.user_account_id
        INNER JOIN 
            seeker_skill_set f ON s.skill_set_id = f.id
        WHERE 
            jp.user_account_id = %s
        GROUP BY 
            jp.user_account_id,
            jp.first_name,
            jp.last_name,
            jp.current_salary,
            jp.currency,
            jp.is_annually_monthly,
            c.certificate_degree_name,
            c.major,
            c.institute_university_name,
            c.percentage,
            c.cgpa,
            c.start_date,
            c.completion_date,
            l.description,
            l.is_current_job,
            l.start_date,
            l.end_date,
            l.job_title,
            l.job_location_city,
            l.job_location_country,
            l.job_location_state,
            s.skill_level
    """
    value = (user_id,)  # Need to pass parameters as a tuple
    cursor.execute(query, value)
    profile = cursor.fetchone()
    cursor.close()  # Close cursor
    return profile



@bp.route('/view_profile', methods=('GET', 'POST'))
@login_required
def view_profile():
    user_id = g.user[0]  # Assuming g.user contains the current user's information

    profile=getprofile(user_id)
    print(profile)
    return render_template('seeker/profile.html',profile=profile)




@bp.route('/update_profile', methods=('GET', 'POST'))
@login_required
def update_profile():
    user_id = g.user[0]  # Assuming g.user contains the current user's information
    #update queries are remaining
    skills=get_skills()
    post=getprofile(user_id)
    if request.method == 'POST':
    
        fn = request.form.get('fn', post[1])
        ln=request.form.get('Ln', post[2])
        degree = request.form['degree']
        major = request.form['major']
        university = request.form['university']
        perc=request.form.get('percentage', post[5])
        cgpa=request.form.get('cgpa', post[6])
        estdt=request.form.get('st_date', post[7])
        eedt=request.form.get('end_date', post[8])
        current_salary = request.form.get('current_salary')
        is_annually_monthly = request.form.get('is_annually_monthly')
        currency = request.form.get('currency')
        profiledesc=request.form.get('profiledesc', post[9])
        is_current_job = int(request.form.get('is_current_job'))
        jstdt=request.form.get('jst_date', post[11])
        jenddt=request.form.get('jend_date', post[12])
        jtitle=request.form.get('JobTitle', post[13])
        jloc=request.form.get('jloc', post[14])
        jloc1=request.form.get('jloc', post[15])
        jloc2=request.form.get('jloc', post[16])
        selected_skills = request.form.getlist('skill')
        skill_level = request.form.get('skill_level')
        skill_level_id = 1 if skill_level == 'Basic' else 2 if skill_level == 'Medium' else 3
        error = None
        if error is not None:
            flash(error)
        cursor = model3.get_cursor()
        # Update job_seeker_profile table
        update_profile_query = """
            UPDATE job_seeker_profile 
            SET first_name = %s, last_name = %s, current_salary = %s, currency = %s, is_annually_monthly = %s 
            WHERE user_account_id = %s
        """
        update_profile_values = (fn, ln, current_salary, 
                                 currency, is_annually_monthly, user_id)
        cursor.execute(update_profile_query, update_profile_values)
         # Update education_detail table
        update_education_query = """
            UPDATE education_detail 
            SET certificate_degree_name = %s, major = %s, percentage = %s, cgpa = %s, 
                start_date = %s, completion_date = %s ,institute_university_name=%s
            WHERE user_account_id = %s
        """
        update_education_values = (degree, major, perc, 
                                  cgpa,  estdt, eedt,university, user_id)
        cursor.execute(update_education_query, update_education_values)
        # Update experience_detail table
        update_experience_query = """
            UPDATE experience_detail 
            SET description = %s, is_current_job = %s, start_date = %s, end_date = %s, 
                job_title = %s, job_location_city = %s, job_location_country = %s, job_location_state = %s 
            WHERE user_account_id = %s
        """
        update_experience_values = (profiledesc, is_current_job, 
                                     jstdt, jenddt, jtitle, 
                                     jloc, jloc1, jloc2, user_id)
        cursor.execute(update_experience_query, update_experience_values)
        model3.commit()
        cursor.close()
        if selected_skills:
            cursor = model3.get_cursor()
            
             # Prepare a string with placeholders for each selected skill
            placeholders = ', '.join(['%s'] * len(selected_skills))
            # Execute the query with the selected skills
            cursor.execute("SELECT id FROM seeker_skill_set WHERE skill_set_name IN ({})".format(placeholders), selected_skills)
            skill_ids = [result[0] for result in cursor.fetchall()]
            # First, delete existing skills for the user
            delete_skills_query = """
            DELETE FROM skill_set WHERE user_account_id = %s
             """
            cursor.execute(delete_skills_query, (user_id,))
            # Insert selected skill set IDs into the skill_set table
            for skill_id in skill_ids:
                cursor.execute("INSERT INTO skill_set (user_account_id, skill_set_id, skill_level) VALUES (%s, %s, %s)",
                               (user_id, skill_id, skill_level_id))  # Assuming skill level is always 1 for simplicity
            
            model3.commit()
            cursor.close()
        return redirect(url_for('seeker.generalseek'))



       
        
    return render_template('seeker/update.html',post=post,skills=skills)

def getappliedjobs(user_id):
    cursor=model4.get_cursor()
    query="SELECT activity_id ,job_post_id,  apply_date, status_desc FROM job_post_activity inner join job_application_status on job_app_status_id=id  WHERE uacid=%s"

    value = (user_id,)  # Need to pass parameters as a tuple
    cursor.execute(query, value)
    # Fetch all results
    applied_jobs = cursor.fetchall()

    # Close cursor and connection
    cursor.close()
    # Extract job IDs, descriptions, and creation dates separately
    

    return applied_jobs


@bp.route('/appliedjobs', methods=('GET', 'POST'))
@login_required
def appliedjobs():
    user_id = g.user[0]  # Assuming g.user contains the current user's information

    applied_jobs=getappliedjobs(user_id)

    return render_template('seeker/applied_jobs.html',applied_jobs=applied_jobs)




