<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="favicon.ico">

    <title>F*ck My Life @ UNLV</title>

    <!-- Bootstrap core CSS -->
    <link href="../static/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="../static/css/starter-template.css" rel="stylesheet">
    <link href="../static/css/custom.css" rel="stylesheet">

    <!-- Just for debugging purposes. Don't actually copy these 2 lines! -->
    <!--[if lt IE 9]><script src="../js/ie8-responsive-file-warning.js"></script><![endif]-->
    <script src="../static/js/ie-emulation-modes-warning.js"></script>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
    
    <script>
    	function increment_like(1) {
    	
    	}
    </script>
  </head>

  <body>

    <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="/">UNLV FML</a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">

 			%if (username == None or len(username) == 0):
 			<div class="navbar-form navbar-right">
     	     <a href="/signup" class="noLinkDec"><button type="button" class="btn btn-default navbar-right">Sign up</button></a>
			</div>

          <form class="navbar-form navbar-right" role="form" method="post" action="/login">
            <div class="form-group">
              <input type="text" placeholder="Email" class="form-control" name="email">
            </div>
            <div class="form-group">
              <input type="password" placeholder="Password" class="form-control" name="password">
            </div>
            <button type="submit" class="btn btn-danger">Log in</button>
          </form>

			%else:
			<div class="navbar-form navbar-right">
     	     <a href="/logout" class="noLinkDec"><button type="button" class="btn btn-default navbar-right">Log out</button></a>
			</div>

			<div class="navbar-form navbar-right">
     	     <a href="/newpost" class="noLinkDec"><button type="button" class="btn btn-danger navbar-right">Post FML</button></a>
			</div>

			<p class="" id="navbar-greeting">
				Hello, {{username}}!
			</p>
			%end
          
        
        </div><!--/.nav-collapse -->
      </div>
    </nav>

    <div class="container">
      <div class="starter-template">
	      <div class="row">
 			 <div class="col-md-6 col-md-offset-3"><!-- centering the posts in the middle -->

<div class="panel panel-default">
  <div class="panel-heading">
    <h3 class="panel-title"><b>{{post['t']}}</b><br></h3>
  </div>
  <div class="panel-body">
  	<div class='largeFontSize'>
	{{!post['b']}}<br />
	</div>
	
	<br />
	<a href="#">
	%if ('c' in post):
	%numComments = len(post['c'])
	%else:
	%numComments = 0
	%end
	{{numComments}} comments</a>

   </div>
</div>
<br />

<!-- display comments -->
<h4>Comments</h4>

%if ('c' in post):
%numComments = len(post['c'])
%else:
%numComments = 0
%end

%for i in range(0, numComments):

<!--
<form action="/like" method="POST">
<input type="hidden" name="permalink", value="{{post['p']}}">
<input type="hidden" name="comment_ordinal", value="{{i}}">
Likes: {{post['c'][i]['n']}} <input type="submit" value="Like">
</form>
-->

<blockquote class="commentBoxes">
  <p>{{post['c'][i]['b']}}</p>
  <footer><b>{{post['c'][i]['u']}}</b> on <i>{{post['c'][i]['t']}}</i></footer>
</blockquote>

<!--
<p class="text-center">On <i>{{post['c'][i]['t']}}</i>, <b>{{post['c'][i]['u']}}</b> wrote:</p>
<blockquote>
  <p>{{post['c'][i]['b']}}</p>
</blockquote>
-->


%end
<!-- display comments -->

<br />

%if (username == None or len(username) == 0):
You must <a href='/login'>log in</a> to post comments.
%else:

<!-- form to add a comment -->
Add a comment:
<form role="form" action="/newcomment" method="POST">
	<div class="form-group">
		<input type="hidden" name="permalink", value="{{post['p']}}">
		<textarea class="form-control" rows="5" id="commentBody" placeholder="Got anything to say?" name="commentBody" maxlength="400">{{newCommentBody}}</textarea>
	</div>
	<br />
	{{errors}}
	<br />
	<button type="submit" class="btn btn-lg btn-danger" value="Submit">Submit</button>
</form>
<!-- form to add a comment -->

%end
			 </div>
		  </div>
      </div>

     <footer>
<div class="row">
  <div class="col-md-6 col-md-offset-3"><!-- centering content in the middle -->
    <p><b>Questions? Concerns? Suggestions?</b> Contact <a href='mailto:feelosophy13@gmail.com' target='_blank'>feelosophy13@gmail.com</a>.</p>
    <p>
      <small>
	  This site is not affiliated, associated, authorized, endorsed by, or in any way officially connected with the University of Nevada Las Vegas, or any of its subsidiaries or its affiliates. This site does not represent the image and brand of the University of Nevada Las Vegas. Our non-commercial use of the university name or university marks is in strict compliance with the university's license guidelines under news reporting and other fair uses that do not undermine the university’s rights in its marks. The official University of Nevada Las Vegas web site is available at <a href='http://www.unlv.edu/' target='_blank'>www.unlv.edu</a>. 
	  </small>
    </p>
  </div>
</div>
      </footer>

    </div><!-- /.container -->



    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="../static/js/bootstrap.min.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="../static/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>
