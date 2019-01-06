var headings = document.getElementsByClassName ("heading");

function ToggleDescription (heading)
{
	return function ()
	{
		var description = heading.getElementsByClassName ("description");
		if (description.length > 0)
		{
			description[0].classList.toggle ("hidden");
			MinimiseOtherHeadings (description[0]);
		}
	}
}

function MinimiseOtherHeadings (descriptionToExclude)
{
	var descriptions = document.getElementsByClassName ("description");

	for (var i = 0; i < descriptions.length; i++) 
	{
		if (! descriptions[i].classList.contains ("hidden") && (descriptions[i] != descriptionToExclude))
		{
			descriptions[i].classList.add ("hidden");	
		}
	}
}

for (var i = 0; i < headings.length; i++) 
{
	headings[i].onclick = ToggleDescription (headings[i]);
}
