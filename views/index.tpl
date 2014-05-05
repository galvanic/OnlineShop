% rebase base


<h2>What is this ?</h2>

<p>
This small webapp allows you to easily split a shared online shopping bill, taking the hassle and awkwardness out of joint shopping. It works like this:
</p>
<ol>
	<li>You input your <em>bill</em> (the last confirmation email sent by Ocado) and your <em>flatmates' names</em></li>
	<li>You input <em>who bought what</em> and if an item was <em>shared by multiple people</em></li>
	<li>The app tells you <em>who owes what</em></li>
</ol>
<p>
	<a href="/pasteshop">Give It A Try</a>
</p>


% if shops:

	<h2>Your Previous Shops</h2>
	<ol>
	% for shop_date in shops:
		<li><a href="#">{{shop_date}}</a></li>
	% end
	</ol>

% end