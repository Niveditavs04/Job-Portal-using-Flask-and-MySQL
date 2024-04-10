import mysql.connector
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from werkzeug.exceptions import abort
from trial2.user import login_required
from trial2.models import Model1,Model2,Model3
from trial2.employer import jobtypeget,skillget
bp = Blueprint('portal', __name__)


cnx = mysql.connector.connect(user='root', password='Mysql@123',
                                  host='localhost')
model2=Model1()
model2.connect(host='localhost', user='root', password='Mysql@123', database='db2')

model4=Model2()
model4.connect(host='localhost', user='root', password='Mysql@123', database='db4')

model3=Model3()
model3.connect(host='localhost', user='root', password='Mysql@123', database='db3')


def fetch_posts(job_title=None, company=None):
  

    cursor = cnx.cursor() 
   # Base query to fetch job posts with company names
    query = "SELECT jp.pid,  jp.createdt, jp.jobdesc FROM db4.job_post jp JOIN db2.company c ON jp.company_id = c.id WHERE jp.is_active = 'y'"

    # Add search filters if provided
    if job_title:
        query += f" and jp.jobdesc LIKE '%{job_title}%'"
    if company:
        query += f" AND c.company_name LIKE '%{company}%' order by jp.jobdesc"  

    # Execute the query
    cursor.execute(query)

    # Fetch all results
    job_posts = cursor.fetchall()

    # Close cursor and connection
    cursor.close()
    # Extract job IDs, descriptions, and creation dates separately
    

    return job_posts


@bp.route('/', methods=['GET', 'POST'])
def hello_flask():
    # Render the HTML template named 'home.html'
    if request.method == 'POST':
        job_title = request.form.get('job_title')
        company = request.form.get('company')

        # Fetch posts based on job title and company
        job_posts = fetch_posts(job_title, company)
        
        return render_template('postings/search.html',job_posts=job_posts)
    return render_template('auth/home.html')

@bp.route('/searchjobs', methods=('GET', 'POST'))

def searchjobs():
    job_posts = fetch_posts()
    
    return render_template('postings/search.html',job_posts=job_posts)

@bp.route('/apply_jobs', methods=('GET', 'POST'))
@login_required
def apply_job():
    return render_template('postings/applyjob.html')

def get_post(id, check_author=True):
    cursor = cnx.cursor()
    query = ("SELECT "
             "jp.pid, "
             "jp.createdt, "
             "jp.jobdesc, "
             "c.company_name, "
             "l.job_type, "
             "CONCAT(ad.street, ', ', ad.city, ', ', ad.state, ', ', ad.country, ', ', ad.zip) AS address, "
             "GROUP_CONCAT(f.skill_set_name) AS skill_set_names "
             "FROM "
             "db4.job_post jp "
             "INNER JOIN db2.company c ON jp.company_id = c.id "
             "INNER JOIN db4.job_type l ON jp.job_type_id = l.pid "
             "INNER JOIN db4.job_location ad ON jp.joblocid = ad.id "
             "INNER JOIN db4.job_post_skillset s ON s.job_post_id = jp.pid "
             "INNER JOIN db3.seeker_skill_set f ON s.skill_setid = f.id "
             "WHERE jp.posted_by = %s "
             "GROUP BY jp.pid "
             "ORDER BY jp.pid;")
    value = (id,)  # Need to pass parameters as a tuple
    cursor.execute(query, value)
    posts = cursor.fetchall()
    cursor.close()  # Close cursor
    cnx.commit()  # Commit transaction if needed

    if not posts:  # Check if the list is empty
        abort(404, f"Post id {id} doesn't exist.")

    

    return posts

@bp.route('/alljobposts', methods=('GET', 'POST'))
def alljobposts():
    id=g.user[0]
    posts = get_post(id)
    return render_template('postings/alljobs.html', posts=posts)

def delete_post_by_id(post_id):
    cursor = cnx.cursor()
    try:
        # Execute the SQL DELETE statement
        query = "DELETE FROM db4.job_post WHERE pid = %s"
        cursor.execute(query, (post_id,))
        # Commit the transaction
        cnx.commit()
        # Return True to indicate successful deletion
        return True
    except Exception as e:
        # If an error occurs, rollback the transaction
        cnx.rollback()
        # Print or log the error message
        print(f"Error deleting post with ID {post_id}: {e}")
        # Return False to indicate failure
        return False
    finally:
        # Close the cursor
        cursor.close()


@bp.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    # Implement the logic to delete the post from the database
    # Example: You might have a function like delete_post_by_id(post_id)
    #          in your database module
    
    # For demonstration purposes, let's assume you have a delete_post_by_id function
    # in your database module
    if delete_post_by_id(post_id):
        flash('Post deleted successfully', 'success')
    else:
        flash('Failed to delete post', 'error')
    
    return redirect(url_for('employer.dashemp')) # Redirect to the dashboard or any other page after deletion

@bp.route('/update_jobpost/<int:post_id>', methods=['POST'])
@login_required
def update_jobpost(post_id):
    if request.method == 'POST':
        # Retrieve form data
        selected_job = request.form.get('job')
        selected_skill = request.form.get('skill')
        user_account_id = g.user[0]  # Assuming g.user contains the current user's information
        skill_level = request.form.get('skill_level')
        companyName = request.form.get('companyName')
        jobdesc = request.form.get('jobDescription')
        addressZip = request.form.get('addressZip')
        skill_level_id = 1 if skill_level == 'Basic' else 2 if skill_level == 'Medium' else 3
        addressStreet = request.form.get('addressStreet')
        addressCity = request.form.get('addressCity')
        addressCountry = request.form.get('addressCountry')
        addressState = request.form.get('addressState')
        
        # Update data in the database
        cursor = model2.get_cursor()
        cursor.execute("SELECT id FROM company where company_name=%s", (companyName,))
        comp_id = cursor.fetchone()
        model2.commit()
        cursor.close()

        cursor3 = model3.get_cursor()
        cursor3.execute("SELECT id FROM seeker_skill_set where skill_set_name=%s", (selected_skill,))
        skill_id = cursor3.fetchone()
        model3.commit()
        cursor3.close()

        cursor4 = model4.get_cursor()
        cursor4.execute("SELECT pid FROM job_type where job_type=%s", (selected_job,))
        jt_id = cursor4.fetchone()

        cursor4.execute("SELECT joblocid FROM job_post WHERE pid = %s", (post_id,))
        jloc = cursor4.fetchone()
        if not jloc:
            # Handle case where job post with given ID doesn't exist
            flash('Job post not found.', 'error')
            return redirect(url_for('employer.dashemp'))
        
        # Update job location
        cursor4.execute("UPDATE job_location SET street = %s, city = %s, state = %s, country = %s, zip = %s WHERE id = %s",
                        (addressStreet, addressCity, addressState, addressCountry, addressZip, jloc[0]))
        
        # Update job post
        cursor4.execute("UPDATE job_post SET job_type_id = %s, company_id = %s, jobdesc = %s , createdt = curdate() WHERE pid = %s",
                        (jt_id[0], comp_id[0], jobdesc, post_id))
        
        # Update job post skillset
        cursor4.execute("UPDATE job_post_skillset SET skill_setid = %s, skill_level = %s WHERE job_post_id = %s",
                        (skill_id[0], skill_level_id, post_id))

        model4.commit()
        cursor4.close()
        return redirect(url_for('employer.dashemp'))
    
    jobs = jobtypeget()
    skills = skillget()
    return render_template('postings/update.html', jobs=jobs, skills=skills)
def update_post(post_id):
    # Implement the logic to delete the post from the database
    # Example: You might have a function like delete_post_by_id(post_id)
    #          in your database module
    
    # For demonstration purposes, let's assume you have a delete_post_by_id function
    # in your database module
    if update_jobpost(post_id):
        flash('Post Updated successfully', 'success')
    else:
        flash('Failed to update post', 'error')
    
    return redirect(url_for('employer.dashemp')) # Redirect to the dashboard or any other page after deletion

