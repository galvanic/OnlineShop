<!DOCTYPE html>
<head>
<title> Insert name here </title>
		<link href='dist/css/bootstrap.css' rel='stylesheet'>
		<link href='style.css' rel='stylesheet'>
</head>

<body>
<div class="jumbotron">

	<div class="container">
		<div class='col-md-2'> <img src="images/logo.png"> </div>
		<h1> Split Milk </h1>
	</div>

</div>

<div class="container">
	<h3>Enter your bill</h3>
		
		<form action="/newshop" method="post" enctype="multipart/form-data" id="myForm">
			<textarea class="form-control" name="shoptext" rows="20">{{default_shop}}</textarea>
			<input type="submit" id="" name="submit" value="Upload Shop" />
		</form>

</div>

</body>