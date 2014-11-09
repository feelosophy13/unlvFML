import sys
import re
import datetime
import pytz



# The Blog Post Data Access Object handles interactions with the Posts collection
class BlogPostDAO:

    # constructor for the class
    def __init__(self, database):
        self.db = database
        self.posts = database.posts

    # inserts the blog entry and returns a permalink for the entry
    def insert_entry(self, body, author):
        
        ## create a permalink
        # utc_timestamp = datetime.datetime.now(tz = pytz.utc)  # obtain timestamp in UTC
        # permalink = str(utc_timestamp)[:-6]  # truncate the timezone specifier (e.g. cut off "+00:00" from "2014-11-01 21:48:31.602066+00:00")
        utc_timestamp = datetime.datetime.utcnow()
        permalink = str(utc_timestamp)
        exp = re.compile('\W|\s')  # match anything not alphanumeric (including whitespace)
        permalink = exp.sub('', permalink)  # permalink is timestamp in UTC

        # build a new post
        post = {"a": author,
                "b": body,
                "p":permalink,
                "c": [],  # 'c' for comments field
                "t": utc_timestamp}  # don't even bother putting in timestamps in PT because they are converted to UTC timestamps in MongoDB

        # now insert the post
        try:
            self.posts.insert(post)
        except:
#            print "Error inserting post"
#            print "Unexpected error:", sys.exc_info()[0]
            bottle.redirect('/internal_error')

        return permalink
        
    # returns an array of posts, reverse ordered
    def get_posts(self, n_posts, page_num):
        n_posts_skip = (page_num - 1) * n_posts
        cursor = self.posts.find().sort('t', direction=-1).skip(n_posts_skip).limit(n_posts)  # sort by date in descending order (recent posts first)
        l = []
                    
        for post in cursor:
            utc_timestamp = post['t']  # naive datetime instance (contains no timezone info in the object)
            pt_timestamp_formatted = convert_utc_to_formatted_pt(utc_timestamp)
            post['t'] = pt_timestamp_formatted  # replace the naive datetime instance with a new timestamp in Pacific Time
            
            if 'c' not in post:
                post['c'] = []
                
            l.append({'b':post['b'], 
                      't':post['t'],
                      'p':post['p'],
                      'a':post['a'],
                      'c':post['c']})
        return l
        
    # determine if next_page_exists (next page exists if there are more previous posts)    
    def next_page_exists(self, n_posts_per_page, page_num):
        n_posts_skip = n_posts_per_page * page_num
        cursor = self.posts.find().skip(n_posts_skip).limit(1)
        
        count = 0
        for post in cursor:
            count += 1

        if count > 0:  # if there are more posts to be displayed
            return True
        return False


    # determine if previous_page_exists (previous page always exists unless the current page number is 1)
    def previous_page_exists(self, page_num):
        return page_num != 1

        
    # find a post corresponding to a particular permalink
    def get_post_by_permalink(self, permalink):

        post = self.posts.find_one({'p': permalink})

        if post is not None:
            # fix up likes values. set to zero if data is not present for comments that have never been liked
            for comment in post['c']:
                if 'n' not in comment:  # "n" for number of likes
                    comment['n'] = 0

            # fix up the timestamp
            utc_timestamp = post['t']
            pt_timestamp_formatted = convert_utc_to_formatted_pt(utc_timestamp)
            post['t'] = pt_timestamp_formatted

        return post

    # add a comment to a particular blog post
    def add_comment(self, permalink, username, body, utc_timestamp):

        comment = {'u': username, 'b': body, 't': utc_timestamp}

        try:
            self.posts.update({'p': permalink}, {'$push': {'c': comment}}, upsert=False, manipulate=False, safe=True)
            return True

            """
            last_error = self.posts.update({'p': permalink}, {'$push': {'c': comment}}, upsert=False, manipulate=False, safe=True)
            return last_error['n']          # return the number of documents updated
            """
        except:
#            print "Could not update the collection, error"
#            print "Unexpected error:", sys.exc_info()[0]
            return False

    # increments the number of likes on a particular comment. Returns the number of documented updated
    def increment_likes(self, permalink, comment_ordinal):

        post = self.get_post_by_permalink(permalink)
        if post is not None:
            mongo_comment_num_likes_key = 'comments.' + str(comment_ordinal) + '.num_likes'
            self.posts.update({'p': permalink}, {'$inc': {mongo_comment_num_likes_key: 1}})
            
        return 0


def convert_utc_to_formatted_pt(utc_timestamp):
    utc_tz = pytz.timezone('UTC')  # UTC timezone
    utc_timestamp = utc_tz.localize(utc_timestamp)  # datetime instance with UTC timezone info stored in the object (no longer naive instance)
    pt_tz = pytz.timezone('US/Pacific')  # specify the timezone to convert to
    pt_timestamp = utc_timestamp.astimezone(pt_tz)  # timestamp in Pacific Time (Standard or Daylight-Savings automatically calculated)
    pt_timestamp_formatted = pt_timestamp.strftime("%A, %B %d, %Y")
#    pt_timestamp = pt_timestamp.strftime("%A, %B %d, %Y at %I:%M %p")  # specify the date format

    return pt_timestamp_formatted
