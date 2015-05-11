$(window).resize(function () {
	$(".row_content").on(
	{
		mouseenter: function () {
			$(this).children('.explain_space').css('display','block');
		},
		mouseleave: function () {
			$(this).children('.explain_space').css('display','none');
		}
	});
}).resize();