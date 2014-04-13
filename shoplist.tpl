% # template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)

<h1>Displaying shop {{date}}</h1>
<p>The shop items are as follows:</p>
<table>
% for row in rows:
  <tr>
  % for col in row:
    <td>{{col}}</td>
  % end
  </tr>
% end
</table>