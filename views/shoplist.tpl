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

	<form action="/{{date}}" method="post" enctype="multipart/form-data" id="myForm">

		<h3> Assign the items </h3>

			<table class='table table-hover'>
				<tr> 
					<th> Item </th>
					<th> Price </th>
					<th> People </th>
				</tr>

				% for idx, name, price in rows:
				<tr>
					<td>{{idx}}. {{name}}</td>
					<td>{{price}}</td>
					<td>

						% for fidx, flatmate in flatmates:
						<input type="checkbox" id="{{idx}}{{flatmate}}" name="item{{idx}}" value="{{flatmate}}">
						  <label for="{{idx}}{{flatmate}}">{{flatmate}}</label>
						% end

					</td>
				</tr>
				% end

		<div class='col-md-2'  id="border-right">
		</div>
			</table>
			
		<input type="submit" id="" name="submit" value="Split my bill" />

	</form>
	
</div>

</body>