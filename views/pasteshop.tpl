% rebase base

<h3></h3>
		
<form action="/newshop" method="post" enctype="multipart/form-data" id="myForm">

	<label for="flatmate_names">Enter the names of your flatmates here (seperated by a space):</label>
	<input type="text" id="flatmate_names" name="flatmate_names" />

	<label for="shoptext">Paste your Ocado confirmation email here:</label>
	<textarea id="shoptext" name="shoptext">{{default_shop}}</textarea>

	<input type="submit" id="submit" name="submit" value="Upload Shop" />

</form>
