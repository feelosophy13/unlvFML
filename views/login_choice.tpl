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
     	     <a href="/newpost" class="noLinkDec"><button type="button" class="btn btn-default navbar-right">Post FML</button></a>
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

  <div class="col-xs-6 col-sm-3"></div>
  <div class="col-xs-6 col-sm-3">
	<a href="/login" class="noLinkDec"><button type="button" class="btn btn-danger btn-lg">Log in</button></a>
  </div>
  <!-- Add the extra clearfix for only the required viewport -->
  <div class="clearfix visible-xs-block"></div>
  <div class="col-xs-6 col-sm-3">
  	<a href="/newpost"><button type="button" class="btn btn-default btn-lg">Submit anonymously</button></a>
  </div>
  <div class="col-xs-6 col-sm-3"></div>

		  </div>
      </div>

      <footer>
        <p>&copy; FML@UNLV 2014</p>
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
