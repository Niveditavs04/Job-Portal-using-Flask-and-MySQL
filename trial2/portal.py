import mysql.connector
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from werkzeug.exceptions import abort
from trial2.user import login_required
from trial2.models import Model1,Model2,Model3
from trial2.employer import jobtypeget,skillget
from trial2.seeker import getprofile
bp = Blueprint('portal', __name__)


cnx = mysql.connector.connect(user='root', password='Mysql@123',
                                  host='localhost')
model2=Model1()
model2.connect(host='localhost', user='root', password='Mysql@123', database='db2')

model3=Model3()
model3.connect(host='localhost', user='root', password='Mysql@123', database='db3')

model4=Model2()
model4.connect(host='localhost', user='root', password='Mysql@123', database='db4')



def fetch_posts(job_title=None, company=None):
  

    cursor = cnx.cursor() 
   # Base query to fetch job posts with company names
    query = "SELECT jp.pid,  jp.createdt, jp.jobdesc FROM db4.job_post jp JOIN db2.company c ON jp.company_id = c.id WHERE jp.is_active = 'y'"

    # Add search filters if provided
    if job_title:
        query += f" or jp.jobdesc LIKE '%{job_title}%'"
    if company:
        query += f" or c.company_name LIKE '%{company}%' order by jp.jobdesc"  

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

@bp.route('/apply_job/<int:post_id>', methods=('GET', 'POST'))
@login_required
def apply_job(post_id):
    cursor = cnx.cursor()
    cursor.execute(
            'SELECT user_type_id FROM db1.user_account WHERE id = %s', (g.user[0],)
        )
    user = cursor.fetchone()[0]
    if user==1:
        insert_query = "INSERT INTO db4.job_post_activity (uacid,job_post_id,job_app_status_id ,apply_date) VALUES (%s, %s, %s, CURDATE())"
        values = (g.user[0], post_id ,1)
        cursor.execute(insert_query, values)
        cnx.commit()
        cursor.close()
        flash('Applied Successfully', 'error')
        return redirect(url_for('seeker.generalseek'))
    else:
        flash('Failed to Apply,you must be a seeker to apply!!', 'error')
        return redirect(url_for('portal.hello_flask'))
    
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

def delete_app_by_id(post_id):
    cursor = cnx.cursor()
    try:
        # Execute the SQL DELETE statement
        query = "DELETE FROM db4.job_post_activity WHERE activity_id = %s"
        cursor.execute(query, (post_id,))
        # Commit the transaction
        cnx.commit()
        # Return True to indicate successful deletion
        return True
    except Exception as e:
        # If an error occurs, rollback the transaction
        cnx.rollback()
        # Print or log the error message
        print(f"Error deleting application with ID {post_id}: {e}")
        # Return False to indicate failure
        return False
    finally:
        # Close the cursor
        cursor.close()


@bp.route('/delete_application/<int:app_id>', methods=['POST'])
@login_required
def delete_application(app_id):
    # Implement the logic to delete the post from the database
    # Example: You might have a function like delete_post_by_id(post_id)
    #          in your database module
    
    # For demonstration purposes, let's assume you have a delete_post_by_id function
    # in your database module
    if delete_app_by_id(app_id):
        flash('Application deleted successfully', 'success')
    else:
        flash('Failed to delete application', 'error')
    
    return redirect(url_for('seeker.generalseek')) # Redirect to the dashboard or any other page after deletion


@bp.route('/viewjp/<int:post_id>', methods=('GET', 'POST'))
@login_required
def viewjp(post_id):
    post=get_a_post(post_id)
    return render_template('postings/jp.html', post=post)


def get_a_post(post_id,check_author=True):
    cursor = cnx.cursor()
    query = ("SELECT "
             "jp.pid, "
             "jp.createdt, "
             "jp.jobdesc, "
             "c.company_name, "
             "l.pid, "
             "ad.street,"
             "ad.city,"
             "ad.state,"
             "ad.country,"
             "ad.zip,"
             "GROUP_CONCAT(f.skill_set_name) AS skill_set_names, "
             "jp.posted_by "
             "FROM "
             "db4.job_post jp "
             "INNER JOIN db2.company c ON jp.company_id = c.id "
             "INNER JOIN db4.job_type l ON jp.job_type_id = l.pid "
             "INNER JOIN db4.job_location ad ON jp.joblocid = ad.id "
             "INNER JOIN db4.job_post_skillset s ON s.job_post_id = jp.pid "
             "INNER JOIN db3.seeker_skill_set f ON s.skill_setid = f.id "
             "WHERE jp.pid = %s "
             "GROUP BY jp.pid "
             ";")
    value = (post_id,)  # Need to pass parameters as a tuple
    cursor.execute(query, value)
    post = cursor.fetchone()
    if post is None:
        abort(404, f"Post id {post_id} doesn't exist.")

    '''if check_author and post[11] != g.user[0]:
        abort(403)'''
    cnx.commit()
    cursor.close()  # Close cursor
     
    
   
    return post


@bp.route('/update_post/<int:post_id>', methods=['GET','POST'])
@login_required
def update_post(post_id):

    # Implement the logic to update the post from the database
    
    post = get_a_post(post_id)
    print(post)
    
    skills = skillget()

    if request.method == 'POST':
        type = int(request.form.get('type', post[4]))
        body = request.form.get('body', post[2])
        company=request.form.get('Company', post[3])
        street=request.form.get('street', post[5])
        city=request.form.get('City', post[6])
        state=request.form.get('State', post[7])
        country=request.form.get('Country', post[8])
        zip=request.form.get('zip', post[9])
        selected_skills = request.form.getlist('skill')
        skill_level = request.form.get('skill_level')
        skill_level_id = 1 if skill_level == 'Basic' else 2 if skill_level == 'Medium' else 3
        error = None
        print("comp:",company)
        if not type:
            error = 'Type is required.'

        if error is not None:
            flash(error)
        else:
             # Update data in the database
            cursor2 = model2.get_cursor()
            cursor2.execute("SELECT id FROM company where company_name=%s", (company,))
            comp_row = cursor2.fetchone()
            print('compid:',comp_row)

            if comp_row is None:
    # Handle the case where no company with the given name is found
    # For example, you could raise an error or set a default value
                flash('Company not found.')
                return redirect(url_for('/'))

            comp_id = comp_row[0]
            model2.commit()
            cursor2.close()
            if selected_skills:
                # Update job post skillset
                cursor3 = model3.get_cursor()
                 # Prepare a string with placeholders for each selected skill
                placeholders = ', '.join(['%s'] * len(selected_skills))
                # Execute the query with the selected skills
                cursor3.execute("SELECT id FROM seeker_skill_set WHERE skill_set_name IN ({})".format(placeholders), selected_skills)
                skill_ids = [result[0] for result in cursor3.fetchall()]
                model3.commit()
                cursor3.close()
                cursor4 = model4.get_cursor()
                for skill_id in skill_ids:
                    cursor4.execute("UPDATE job_post_skillset SET skill_setid = %s, skill_level = %s WHERE job_post_id = %s",
                        (skill_id, skill_level_id, post_id))
                model4.commit()
                cursor4.close()
            
                

            cursor4 = model4.get_cursor()
            cursor4.execute("SELECT joblocid FROM job_post WHERE pid = %s", (post_id,))
            jloc = cursor4.fetchone()[0]
            # Update job location
            cursor4.execute("UPDATE job_location SET street = %s, city = %s, state = %s, country = %s, zip = %s WHERE id = %s",
                        (street, city, state, country, zip, jloc))
            # Update job post
            cursor4.execute("UPDATE job_post SET job_type_id = %s, company_id = %s, jobdesc = %s , createdt = curdate() WHERE pid = %s",
                        (type, comp_id, body, post_id))
        
            
            model4.commit()
            cursor4.close()
            return redirect(url_for('employer.dashemp'))
        


    return render_template('postings/update.html', post=post,skills=skills)

def latestoffers(userid):
    cursor = cnx.cursor()

    # Query to fetch job post IDs based on matching skills
    query = """
        SELECT DISTINCT jps.job_post_id
        FROM db4.job_post_skillset jps
        WHERE EXISTS (
            SELECT 1
            FROM db3.skill_set sss 
            WHERE sss.user_account_id = %s
            AND sss.skill_set_id = jps.skill_setid
            AND sss.skill_level <= jps.skill_level
        )
    """
    value = (userid,)
    cursor.execute(query, value)
    pids = [pid[0] for pid in cursor.fetchall()]

    # Query to fetch job offers with company names for the retrieved job post IDs
    if pids:
        placeholders = ','.join(['%s'] * len(pids))
        offers_query = f"""
            SELECT jp.pid, jp.createdt, jp.jobdesc 
            FROM db4.job_post jp 
            JOIN db2.company c ON jp.company_id = c.id 
            WHERE jp.pid IN ({placeholders})
        """
        cursor.execute(offers_query, pids)
        offers = cursor.fetchall()
    else:
        offers = []

    cursor.close()
    return offers

@bp.route('/joboffer', methods=['GET','POST'])
@login_required
def joboffer():
    userid=g.user[0]
    offers=latestoffers(userid)
    
    return render_template('postings/joboffers.html',posts=offers)

def get_actions():
    cursor = cnx.cursor()
    cursor.execute("SELECT actionname FROM db4.job_app_action")
    actions = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    return  actions

def appliacantget(app_id,jpalid):
    cursor = model4.get_cursor()
    query = """
        SELECT 
            jp.pid,
            l.uacid,
            l.apply_date,l.activity_id,
            c.status_desc
        FROM 
            job_post jp
        INNER JOIN 
            job_post_activity l ON jp.pid = l.job_post_id
        INNER JOIN
            job_application_status c ON l.job_app_status_id = c.id
        WHERE 
             l.activity_id=%s
        
    """
    value = (jpalid,)  # Need to pass parameters as a tuple
    cursor.execute(query, value)
    post = cursor.fetchone()
    cursor.close()  # Close cursor

    if not post:  # Check if the list is empty
        abort(404, f"No applicant found for user ID {app_id}.")

    return post

def reviewproces(app_id,jpalid):
    cursor = cnx.cursor()
    cnx.commit()
    cursor.close()


@bp.route('/applicant_profile/<int:app_id>', methods=['GET', 'POST'])
@login_required
def applicant_profile(app_id):
    profile=getprofile(app_id)
    
    print(profile)
    return render_template('postings/vp.html',profile=profile)
      


@bp.route('/review_app/<int:app_id>/<int:jpalid>', methods=['GET','POST'])
@login_required
def review_app(app_id,jpalid):
    userid=g.user[0]
    actions=get_actions()
    post=appliacantget(app_id,jpalid)
    if request.method == 'POST':
        # Retrieve form data
        selected_action = request.form.get('action')
        cursor = cnx.cursor()
        cursor.execute("SELECT MAX(id) FROM db4.jpal")
        max_id = cursor.fetchone()[0]
        new_id = max_id + 1 if max_id is not None else 1
        cursor.execute("SELECT id FROM db4.job_app_action where actionname=%s", (selected_action,))

        at_id = cursor.fetchone()[0]
        # Check if userid exists in jpal table
        cursor.execute("SELECT COUNT(*) FROM db4.jpal WHERE userid = %s", (userid,))
        count = cursor.fetchone()[0]

        if count > 0:
            # If userid exists, update the corresponding row
            cursor.execute("UPDATE db4.jpal SET jpactivity_id = %s, jpaction_id = %s, actiondt = CURDATE() WHERE userid = %s", (jpalid, at_id, userid))
        else:
            # If userid doesn't exist, insert a new row
            cursor.execute("INSERT INTO db4.jpal (id,jpactivity_id, jpaction_id, actiondt, userid) VALUES (%s,%s, %s, CURDATE(), %s)", (new_id,jpalid, at_id, userid))
        cnx.commit()
        cursor.close()
        return redirect(url_for('employer.dashemp'))



    return render_template('postings/review.html',actions=actions,post=post)

@bp.route('/track_visit/<int:app_id>', methods=['GET'])
def track_visit(app_id):
    userid=g.user[0]
    cursor = cnx.cursor()
    cursor.execute("SELECT MAX(id) FROM db3.profile_visit_log")
    max_id = cursor.fetchone()[0]
    new_id = max_id + 1 if max_id is not None else 1
    cursor.execute("Insert into db3.profile_visit_log  (id,seeker_profile_id, user_account_id, visit_date,is_resume_downloaded, is_job_notification_sent) VALUES(%s,%s,%s,NOW(),%s,%s)",
                        (new_id,app_id ,userid,True, False ))
    cnx.commit()
    cursor.close()
        
    return 'OK'