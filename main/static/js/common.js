'use strict';

$(function(){
	$('.form_text_ipt input').focus(function(){
		$('.ececk_warning').hide();
	});

	$('#submit').click(function (){
		var username = $('#username').val();
		var password = $('#password').val();
		if (username.trim() == '' || password.trim() == '') {
			$('.ececk_warning').show();
			$('.ececk_warning_text').text('邮箱和密码不能为空！')
			return false;
		}
		if (! /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/.test(username)) {
			$('.ececk_warning').show();
			$('.ececk_warning_text').text('邮箱格式有误！')
			return false;
		}
		if (password.length < 6 || password.length > 16) {
			$('.ececk_warning').show();
			$('.ececk_warning_text').text('密码长度为6~16个有效字符')
			return false;
		}
		if (! /^[a-zA-Z0-9_?!/*-+.]+$/.test(password)) {
			$('.ececk_warning').show();
			$('.ececk_warning_text').text('密码中含有无效字符！')
			return false;
		}
		return true;
	});
});
