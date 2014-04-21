<!DOCTYPE html>
<head>
<title> Split Milk </title>
		<link href='dist/css/bootstrap.css' rel='stylesheet'>
		<link href='style.css' rel='stylesheet'>
</head>

<body>
<div class="jumbotron">

	<div class="container">
		<div class='col-md-2'> <img src="images/smalllogo.png"> </div>
		<h1> Split Milk </h1>
	</div>

</div>

<div class="container">
	<h3>Your {{date}} bill is</h3>
		
	<table class='table table-hover'>

	% for flatmate, ftotal in money:
	<tr>
		<td>{{flatmate}}</td>
		<td>{{ftotal}}</td>
	</tr>
	% end
	<tr>
		<td>Total:</td>
		<td>{{total}}</td>
	</tr>

	</table>

</div>

</body>
