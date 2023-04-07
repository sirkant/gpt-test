<!DOCTYPE html>
<html> 
<head>
    <meta charset="utf-8">
    <title>My website</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <script> 
    $(document).ready(function() {
        $('.nav-link').click(function() {
            $('.active').removeClass('active');
            $(this).addClass('active');
        });
    }); 
</script>
</head>
<body>
    <nav class="navbar navbar-default navbar-expand-lg navbar-light bg-light">
        <div class="navbar-header">
            <a class="navbar-brand" href="#">My Website </a>
            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span> 
            </button>
        </div>
        <div class="collapse navbar-collapse" id="myNavbar">
            <ul class=" nav navbar-nav">
                <li><a class="nav-link active" href="#Home">Home</a></li>
                <li><a class="nav-link" href="#About">About us</a></li>
                <li><a class="nav-link" href="#Contact">Contact us</a></li>
            </ul>
        </div>
    </nav>
    <div class="container">
        <!-- content goes here -->
    </div>
</body>
</html>