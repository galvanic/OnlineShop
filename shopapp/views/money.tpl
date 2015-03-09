% rebase base

<h3>Your bill from the {{date}}</h3>
		
<table>

	% for flatmate, ftotal in money:
	<tr>
		<td>{{flatmate}}</td>
		<%
		ftotal = "%.2f" % ftotal
		%>
		<td>{{ftotal}}</td>
	</tr>
	% end
	<tr>
		<td>Total:</td>
		<td>{{total}}</td>
	</tr>

</table>