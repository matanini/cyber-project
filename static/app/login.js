// document.getElementById("register-submit").disabled = true

$(function() {

    $('#login-form-link').click(function(e) {
		$("#login-form").delay(100).fadeIn(100);
 		$("#register-form").fadeOut(100);
		$('#register-form-link').removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});
	$('#register-form-link').click(function(e) {
		$("#register-form").delay(100).fadeIn(100);
 		$("#login-form").fadeOut(100);
		$('#login-form-link').removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});

});

$('#register-password, #register-confirm-password').on('keyup', function () {
	if ($('#register-password').val() == $('#register-confirm-password').val()) {
	  $('#message').html('Matching').css('color', 'green');
	  if (($('register-username').val() != null && $('register-username').val() != '') &&
	      ($('register-password').val() != null && $('register-password').val() != '')&& 
	      ($('register-email').val() != null && $('register-email').val() != ''))
	   {
		$("register-submit").disabled = false
	  }
	} else 
	  $('#message').html('Not Matching').css('color', 'red');
	  $("register-submit").disabled = true
  });
