% rebase base

<%
flatmate_names = " ".join(flatmates)
flatmates = list(enumerate(flatmates, 1))
%>

<h3> Assign the items to each flatmate</h3>

<form action="/{{date}}" method="post" enctype="multipart/form-data" id="myForm">

	<input type="hidden" id="flatmate_names" name="flatmate_names" value="{{flatmate_names}}" />

	<table>

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

	</table>
	
	<input type="submit" id="" name="submit" value="Split my bill" />

</form>