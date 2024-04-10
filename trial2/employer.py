import functools
import mysql.connector
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from trial2.user import login_required
from trial2.models import Model1,Model2,Model3

bp = Blueprint('employer', __name__, url_prefix='/employer')
#table connections
model2=Model1()
model2.connect(host='localhost', user='root', password='Mysql@123', database='db2')

model4=Model2()
model4.connect(host='localhost', user='root', password='Mysql@123', database='db4')

model3=Model3()
model3.connect(host='localhost', user='root', password='Mysql@123', database='db3')

#you can't write global variables in flask
@bp.route('/generale', methods=('GET', 'POST'))
@login_required
def generale():
    
    cursor = model2.get_cursor()
    cursor.execute("SELECT  company_name FROM company")
    companies = [row[0] for row in cursor.fetchall()]
    model2.commit()
    cursor.close()
    
    if request.method == 'POST':
        
        selected_company_id = request.form.get('companyOption')
        session['selected_company_id'] = selected_company_id
    # Process and store the selected company ID
        return redirect(url_for('employer.jobpost'))
     # Fetch company options from the database
   
    
    return render_template('Employer/empprofile.html', companies=companies)

def bsidget():
    cursor = model2.get_cursor()
    cursor.execute("SELECT business_stream_name FROM business_stream")
    streams = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    return streams


@bp.route('/compreg', methods=('GET', 'POST'))
@login_required
def compreg():
    if request.method == 'POST':
        # Retrieve form data
        selected_stream = request.form.get('stream')
        user_account_id = g.user[0]  # Assuming g.user contains the current user's information
        
        companyName = request.form['companyName']
        profiledesc = request.form['profiledesc']
       
        establishmentDate = request.form['establishmentDate']
        companyURL = request.form['companyURL']
        
        companyimgURL = request.form['companyimgURL']
        # Insert data into the database
       
        cursor = model2.get_cursor()
        cursor.execute("SELECT MAX(id) FROM company")
        max_id = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM business_stream where business_stream_name=%s", (selected_stream,))
        bs_id = cursor.fetchone()[0]
        new_id = max_id + 1 if max_id is not None else 1
        insert_query = "INSERT INTO company (company_name, profile_description, business_stream_id, establishment_date, company_website_url,id) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (companyName, profiledesc, bs_id, establishmentDate, companyURL,  new_id)

        cursor.execute(insert_query, values)
        cursor.execute("SELECT MAX(image_id) FROM company_image")
        img_id = cursor.fetchone()[0]
        newimg_id = img_id + 1 if img_id is not None else 1
        insert_query = "INSERT INTO company_image (image_id, company_id, image_url) VALUES (%s, %s, %s)"
        values = (newimg_id,new_id, companyimgURL )
        cursor.execute(insert_query, values)
        model2.commit()
        cursor.close()
        return redirect(url_for('employer.generale'))
    
    streams=bsidget()
    return render_template('Employer/comregister.html', streams=streams)


def jobtypeget():
    cursor4 = model4.get_cursor()
    cursor4.execute("SELECT job_type FROM job_type")
    jobs = [row[0] for row in cursor4.fetchall()]
    cursor4.close()
    
    return jobs

def skillget():
    cursor3 = model3.get_cursor()
    cursor3.execute("SELECT skill_set_name FROM seeker_skill_set")
    skills = [row[0] for row in cursor3.fetchall()]
    cursor3.close()
    
    return skills

@bp.route('/jobpost', methods=('GET', 'POST'))
@login_required
def jobpost():
    
    if request.method == 'POST':
        # Retrieve form data
        selected_job = request.form.get('job')
        selected_skill = request.form.get('skill')
        user_account_id = g.user[0]  # Assuming g.user contains the current user's information
        skill_level = request.form.get('skill_level')
        companyName = request.form['companyName']
        jobdesc = request.form['jobDescription']
        addressZip=request.form['addressZip']
        skill_level_id = 1 if skill_level == 'Basic' else 2 if skill_level == 'Medium' else 3
        addressStreet = request.form['addressStreet']
        addressCity = request.form['addressCity']
        addressCountry= request.form['addressCountry']
        addressState = request.form['addressState']
        # Insert data into the database
        cursor = model2.get_cursor()
        cursor.execute("SELECT id FROM company where company_name=%s", (companyName,))
        comp_id = cursor.fetchone()[0]
        model2.commit()
        cursor.close()

        cursor3 = model3.get_cursor()

        cursor3.execute("SELECT id FROM seeker_skill_set where skill_set_name=%s", (selected_skill,))
        skill_id = cursor3.fetchone()[0]
        model3.commit()
        cursor3.close()

        cursor4 = model4.get_cursor()
        cursor4.execute("SELECT MAX(pid) FROM job_post")
        max_id = cursor4.fetchone()[0]
        new_id = max_id + 1 if max_id is not None else 1
        cursor4.execute("SELECT MAX(id) FROM job_location")
        mj_id = cursor4.fetchone()[0]
        newj_id = mj_id + 1 if mj_id is not None else 1
        cursor4.execute("SELECT pid FROM job_type where job_type=%s", (selected_job,))

        jt_id = cursor4.fetchone()[0]

        
        insert_query = "INSERT INTO job_location (id, street, city, state, country, zip) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (newj_id, addressStreet, addressCity, addressState, addressCountry,  addressZip)

        cursor4.execute(insert_query, values)
        
        insert_query = "INSERT INTO job_post (pid, posted_by, job_type_id,company_id,is_cnm_hid,jobdesc,joblocid,is_active,createdt) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, CURDATE())"
        values = (new_id, user_account_id ,jt_id,comp_id,'y',jobdesc,newj_id,'y')
        cursor4.execute(insert_query, values)
        insert_query = "INSERT INTO job_post_skillset (skill_setid, job_post_id, skill_level) VALUES (%s, %s, %s)"
        values = (skill_id,new_id,skill_level_id)
        cursor4.execute(insert_query, values)

        model4.commit()
        cursor4.close()
        #session['has_posted_job'] = True
        return redirect(url_for('employer.dashemp'))
    
    jobs=jobtypeget()
    skills=skillget()

    
    
    return render_template('Employer/jobpost.html',jobs=jobs,skills=skills)


def get_total_posts_by_user_id(user_id):
    cursor = model4.get_cursor()
    query = "SELECT COUNT(*) FROM job_post WHERE posted_by = %s"
    cursor.execute(query, (user_id,))
    total_posts = cursor.fetchone()[0]  # Fetch the count from the first column of the first row
    cursor.close()  # Close cursor
    return total_posts

@bp.route('/dashemp', methods=('GET', 'POST'))
@login_required
def dashemp():
    user_id = g.user[0]  # Assuming g.user[0] contains the user ID
    
    total_posts = get_total_posts_by_user_id(user_id)  # Function to retrieve total posts by user ID from the database

    return render_template('Employer/dashemp.html', total_posts=total_posts)
    
    


