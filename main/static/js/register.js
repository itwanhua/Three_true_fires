'use strict';
var token = $('input[name=csrfmiddlewaretoken]').val();

$(function(){
	$.ajaxSetup({
		data:{csrfmiddlewaretoken:'{{ csrf_token }}'}
	});

	$('.form_text_ipt input').focus(function(){
		$('.ececk_warning').hide();
	});

	$("#send_code").click(function() {
		var username = $('#username').val();
		if (! /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/.test(username)) {
			$('.ececk_warning').show();
			$('.ececk_warning_text').text('邮箱格式有误！')
			return false;
		}
		// 通过Ajax技术连接服务器后端校验用户名是否已被注册
		console.log("校验名字...")
		$.ajax({
			url: "/check_username",
			data: {
				username: username
			},
			success: function(data){
				if (data["err"] === 0){
					// 用户名没有被注册
					var s = 60;
					$("#send_code").prop("disabled", true);
					$("#send_code").html(s + "S");
					
					var timer = window.setInterval(function() {
						--s;
						if (s === 0) {
							window.clearInterval(timer);
							$("#send_code").html("重新发送");
							$("#send_code").prop("disabled", false);
							return;
						}
						$("#send_code").html(s + "S");
					}, 1000);
					// 通过ajax请求后端发送验证码
					console.log("申请发送验证码")
					$.ajax({
						type: "POST",
						url: "/send_code",
						data: {
							csrfmiddlewaretoken: token,
							email: username
						},
						dataType: "json",
						success: function(data) {
							if (data["err"] === 0) {
								// 发送验证码成功！
							}
							else {
								// 失败
								alert("发送验证码失败！" + data["desc"]);
							}
						},
						error: function() {
							alert("发送请求失败，请检查网络连接！");
						}
					});

				} else if (data["err"] === 1) {
					// 用户名已经被注册
					console.log("1111111111111")
					$('.ececk_warning').show();
					$('.ececk_warning_text').text('该邮箱已经注册！')
					return flase;
				}
			}
		});
	});

	$('#submit').click(function (){
		console.log("11111111111")
		var username = $('#username').val();
        var password = $('#password').val();
        var password2 = $('#password2').val();
		var code = $('#code').val();
		if (username.trim() == '' || password.trim() == '' || password2.trim() == '' || code.trim() == '') {
			$('.ececk_warning').show();
			$('.ececk_warning_text').text('请输入完整信息！')
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
			$('.ececk_warning_text').text('密码中只能含有数字、字母、下滑下划线，其它字符无效！')
			return false;
        }
        if (password2 !== password) {
			$('.ececk_warning').show();
			$('.ececk_warning_text').text('两次输入密码不一致！')
			return false;
		}
		if (! /^\d{6}$/.test(code)) {
			$('.ececk_warning').show();
			$('.ececk_warning_text').text('验证码为六位数字！')
			return false;
		}
		return true;
	});
});
