"use strict";

$(function() {
    var token = $('input[name=csrfmiddlewaretoken]').val();
    $.ajaxSetup({
		data:{csrfmiddlewaretoken:'{{ csrf_token }}'}
    });

    // 修改按钮点击事件
    $("#modify").click(function() {
        $("input").removeAttr("disabled")
        $(this).hide("slow", function(){
            $("#submit").show("slow")
        })
    });

    // 提交事件触发
    $("#submit").click(function(){
        var nickname = $("#nickname").val()
        var realname = $("#realname").val()
        var phone = $("#phone").val()
        var address = $("#address").val()
        var remarks = $("#remarks").val()
        // 校验数据


        return true;
    });
    



    $.ajax({
        type: "GET",
        url: "get_user_info",
        data:{
            csrfmiddlewaretoken: token,
            nickname: $("#nickname").val()
        },
        success: function(data) {
            // 获取用户个人资料
            $("#realname").val(data["user_info"]["realname"])
            $("#phone").val(data["user_info"]["phone"])
            $("#address").val(data["user_info"]["target_addr"])
            $("#remarks").val(data["user_info"]["remarks"])
        },
        error: function(data) {
            alert("网络错误！")
        }
    });

})