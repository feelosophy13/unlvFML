import os
import pymongo
import blogPostDAO
import sessionDAO
import userDAO
import bottle
import cgi
import re
import datetime
import pytz

"""
@bottle.post('/like_post')
def like():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    permalink = bottle.request.forms.get('permalink'); cgi.escape(permalink)
    post = posts.get_post_by_permalink(permalink)

    if post is None:
        bottle.redirect("/post_not_found")
        return

    # process like
    return 'success'


@bottle.post('/unlike_post')
def unlike():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    permalink = bottle.request.forms.get("permalink"); cgi.escape(permalink)
    post = posts.get_post_by_permalink(permalink)

    if post is None:
        bottle.redirect("/post_not_found")
        return

    # process unlike
    return 'success'


# used to process a like on a comment
@bottle.post('/like_comment')
def post_comment_like():
    permalink = bottle.request.forms.get("permalink"); permalink = cgi.escape(permalink)
    comment_ordinal_str = bottle.request.forms.get("comment_ordinal"); comment_ordinal_str = cgi.escape(comment_ordinal_str)
    comment_ordinal = int(comment_ordinal_str)
    post = posts.get_post_by_permalink(permalink)

    if post is None:
        bottle.redirect("/post_not_found")
        return

    # it all looks good. increment the ordinal
    posts.increment_likes(permalink, comment_ordinal)

    bottle.redirect("/post/" + permalink)
"""


@bottle.route('/static/css/<filename>')
def serve_static(filename):
    return bottle.static_file(filename, root='static/css')


@bottle.route('/static/js/<filename>')
def serve_static(filename):
    return bottle.static_file(filename, root='static/js')


@bottle.route('/')
@bottle.route('/<page_num:int>')
def main_page(page_num = 1):  # by default, page_num = 1
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    n_posts_per_page = 10
    l = posts.get_posts(n_posts_per_page, page_num)
    previous_page_exists = posts.previous_page_exists(page_num)
    next_page_exists = posts.next_page_exists(n_posts_per_page, page_num)
    previous_page_num = page_num - 1
    next_page_num = page_num + 1

    return bottle.template('main', dict(myposts=l, username=username,
                                        page_num=page_num,
                                        previous_page_exists=previous_page_exists,
                                        next_page_exists=next_page_exists,
                                        previous_page_num=previous_page_num,
                                        next_page_num=next_page_num))


# displays a particular blog post
@bottle.get("/post/<permalink>")
def show_post(permalink="notfound"):
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    permalink = cgi.escape(permalink)
    post = posts.get_post_by_permalink(permalink)

    if post is None:
        bottle.redirect("/post_not_found")

    # init comment form field for additional comment
    newCommentBody = ""

    # format comment timestamps
    if len(post['c']) > 0:  # if there is at least one comment inside a post
        comments = []
        for comment in post['c']:
            utc_timestamp = comment['t']
            pt_timestamp_formatted = convert_utc_to_formatted_pt(utc_timestamp)
            comment = {'u': comment['u'], 'b': comment['b'], 't': pt_timestamp_formatted, 'n': comment['n']}
            comments.append(comment)
        post['c'] = comments

    return bottle.template("entry_template", dict(post=post, username=username, errors="", newCommentBody=newCommentBody))


# used to process a comment on a blog post
@bottle.post('/newcomment')
def post_new_comment():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    body = bottle.request.forms.get("commentBody")  # will be escaped later (after the body length has been verified)
    permalink = bottle.request.forms.get("permalink"); permalink = cgi.escape(permalink)
    post = posts.get_post_by_permalink(permalink)

    # if user is not logged in (which she/he should be since only logged-in users can submit comments)
    if username is None:
        bottle.redirect('/login')

    # if post not found, redirect to post not found error
    if post is None:
        bottle.redirect("/post_not_found")
        return

    if body == "" or len(body) > 400:
        comment = {'username': username, 'body': ""}
        errors = "What are you doing? No funny business is allowed here!"
        return bottle.template("entry_template",
                               dict(post=post, username=username, errors=errors, comment=comment))

    else:  # if it all looks good
        # obtain a timestamp
        utc_timestamp = datetime.datetime.utcnow()  # obtain timestamp in UTC

        # escape, strip left and right ends, and put paragraph breaks in the comment body
        body = cgi.escape(body, quote=True)
        body = body.strip()
        newline = re.compile('\r?\n')
        body = newline.sub("<p>", body)

        # insert and redirect
        posts.add_comment(permalink, username, body, utc_timestamp)
        bottle.redirect("/post/" + permalink)


# Displays the form allowing a user to add a new post. Only works for logged in users
@bottle.get('/newpost')
def get_newpost():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)  # see if user is logged in
    if username is None:
        bottle.redirect('/login')
            # return bottle.template("newpost_template", dict(body = "", errors="", username="Anonymous"))

    return bottle.template("newpost_template", dict(body = "", errors="", username=username))


# Post handler for setting up a new post.
# Only works for logged in user.
@bottle.post('/newpost')
def post_newpost():
    post = bottle.request.forms.get("body")
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)  # see if user is logged in
    if username is None:
        username = "Anonymous"

    if post == "":
        errors = "You can't submit a blank post, dummy! :P"
        return bottle.template("newpost_template", dict(username=username,
                                                        body="", errors=errors))
    if len(post) > 800:
        bottle.redirect('/')

    ## if all looks good
    escaped_post = cgi.escape(post, quote=True)  # escape the post
    escaped_post = escaped_post.strip()  # strip left and right ends
    newline = re.compile('\r?\n')
    formatted_post = newline.sub("<p>", escaped_post)  # substitute some <p> for the paragraph breaks
    permalink = posts.insert_entry(formatted_post, username)

    ## bottle.redirect to the main page
    bottle.redirect('/')


# displays the initial blog signup form
@bottle.get('/signup')
def present_signup():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    if username:
        bottle.redirect("/")

    return bottle.template("signup",
                           dict(username="", password="",
                                password_error="",
                                email="", username_error="", email_error="",
                                verify_error =""))


@bottle.post('/signup')
def process_signup():

    email = bottle.request.forms.get("email")
    username = bottle.request.forms.get("username")
    password = bottle.request.forms.get("password")
    password2 = bottle.request.forms.get("password2")

    # set these up in case we have an error case
    errors = {'username': cgi.escape(username), 'email': cgi.escape(email)}
    if validate_signup(username, password, password2, email, errors):

        if not users.add_user(email, username, password):
            # this was a duplicate
            errors['username_error'] = "Darn... That username or email ID is already taken. Try another?"
            return bottle.template("signup", errors)

        session_id = sessions.start_session(username)
        bottle.response.set_cookie("session", session_id)
        bottle.redirect("/")
    else:  # if user did not validate
        return bottle.template("signup", errors)


# displays the initial blog login form
@bottle.get('/login')
def present_login():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    if username:
        bottle.redirect("/")
    return bottle.template("login",
                           dict(username="", email="", password="",
                                email_error="", match_error=""))


# handles a login request
@bottle.post('/login')
def process_login():

    email = bottle.request.forms.get("email")
    password = bottle.request.forms.get("password")
    errors = {'email_error': '', 'match_error': ''}
    user_record = users.validate_login(email, password, errors)

    if user_record:  # if valid login credentials provided
        # username is stored in the user collection in the username key
        session_id = sessions.start_session(user_record['u'])

        if session_id is None:
            bottle.redirect("/internal_error")
        cookie = session_id

        # Warning, if you are running into a problem whereby the cookie being set here is
        # not getting set on the redirect, you are probably using the experimental version of bottle (.12).
        # revert to .11 to solve the problem.
        bottle.response.set_cookie("session", cookie)
        bottle.redirect("/")

    else:  # if invalid login credential provided
        return bottle.template("login",
                               dict(username=None, email=cgi.escape(email), password="",
                                    email_error=errors['email_error'], match_error=errors['match_error']))


@bottle.get("/post_not_found")
@bottle.get('/internal_error')
@bottle.view('error_template')
def present_internal_error():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    return bottle.template("error_template", dict(username=None))


@bottle.get('/logout')
def process_logout():
    cookie = bottle.request.get_cookie("session")
    sessions.end_session(cookie)
    bottle.response.set_cookie("session", "")
    bottle.redirect("/")


## helper functions

# validates that the user information is valid for new signup, return True of False
# and fills in the error string if there is an issue
def validate_signup(username, password, password2, email, errors):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{1,30}$")
    PASS_RE = re.compile(r"^.{3,30}$")
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

    errors['username_error'] = ""
    errors['password_error'] = ""
    errors['verify_error'] = ""
    errors['email_error'] = ""

    if not USER_RE.match(username):
        errors['username_error'] = "Oops! Invalid username. Just letters and numbers, please."
        return False
    if not PASS_RE.match(password):
        errors['password_error'] = "Sorry. Invalid password. At least 3 characters, k?"
        return False
    if password != password2:
        errors['verify_error'] = "Grr... The passwords must match!"
        return False
    if not EMAIL_RE.match(email):
        errors['email_error'] = "Trying to fool me? That's an invalid email address."
        return False

    return True


def convert_utc_to_formatted_pt(utc_timestamp):
    utc_tz = pytz.timezone('UTC')  # UTC timezone
    utc_timestamp = utc_tz.localize(utc_timestamp)  # datetime instance with UTC timezone info stored in the object (no longer naive instance)
    pt_tz = pytz.timezone('US/Pacific')  # specify the timezone to convert to
    pt_timestamp = utc_timestamp.astimezone(pt_tz)  # timestamp in Pacific Time (Standard or Daylight-Savings automatically calculated)
    pt_timestamp_formatted = pt_timestamp.strftime("%B %d, %Y")
#    pt_timestamp = pt_timestamp.strftime("%A, %B %d, %Y at %I:%M %p")  # specify the date format

    return pt_timestamp_formatted


connection = pymongo.mongo_client.MongoClient(os.environ['OPENSHIFT_MONGODB_DB_HOST'], int(os.environ['OPENSHIFT_MONGODB_DB_PORT']))
database = connection.blog

posts = blogPostDAO.BlogPostDAO(database)
users = userDAO.UserDAO(database)
sessions = sessionDAO.SessionDAO(database)

def application(environ, start_response):
    return bottle.default_app().wsgi(environ,start_response)

if __name__ == "__main__":
    bottle.debug(True)
    run(reloader=True)
