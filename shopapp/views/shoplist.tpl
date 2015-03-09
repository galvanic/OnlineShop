% rebase base


<h3> Assign the items to each flatmate</h3>

<form action="/{{date}}" method="post" enctype="multipart/form-data" id="myForm">

	<table>

		<tr> 
			<th> Item </th>
			<th> Price </th>
			<th> People </th>
		</tr>

		% for idx, item in rows:
		<tr>
			<td>{{idx}}. {{item.name}}</td>
			<td>{{item.price}}</td>
			<td>

				% for name, person_id in flatmates:
				<input type="checkbox" id="{{idx}}{{name}}" name="{{item.item_id}}" value="{{person_id}}">
				<label for="{{idx}}{{name}}">{{name}}</label>
				% end

			</td>
		</tr>
		% end

	</table>
	
	<input type="submit" id="" name="submit" value="Split my bill" />

</form>