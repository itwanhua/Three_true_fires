"use strict";

$(function() {
    var token = $('input[name=csrfmiddlewaretoken]').val();
    $.ajaxSetup({
        data:{csrfmiddlewaretoken:'{{ csrf_token }}'}
    });


    $.ajax({
        type: "POST",
        url: "/order_center",
        data:{
            csrfmiddlewaretoken: token,
            nickname: $("#nickname").val()
        },
        success: function(data) {
            // 获取用户个人资料
            console.log(data)
            if (data["err"] === 0) {
                for (var f in data['info']) {
                    console.log(data['info'])
                    $(".order_info").append("<tr><td class='order_details'><a id='details' href='#'>"+data['info'][f]['order_id']+"</a></td><td>"+data['info'][f]['otime']+"</td><td>"+data['info'][f]['customer']+"</td><td>"+data['info'][f]['phone']+"</td><td>"+data['info'][f]['total_money']+"￥</td><td class='addr'>"+data['info'][f]['target_addr']+"</td></tr>")
                }
            } else {
                $(".order_info").append("<tr><td colspan=6>暂无历史订单</td></tr>")
            }
        },
        error: function(data) {
            alert("网络错误！")
        }
    });


    $("table").delegate("#details", "click", function() {
        // 点击订单号查看详情
        console.log("00000")
        $.ajax({
            type: "POST",
            data: {
                csrfmiddlewaretoken: token,
                order_id: $(this).html()
            },
            url: "/get_history_order_info",
            success: function(data) {
                console.log(data)
                $(".order_detail").show()
                $(".info").hide()
                $("h1").html("订单号：" + data["item"][0]["order_id"])
                for ( var f in data["item"]) {
                    console.log(data["item"])
                    $(".odet").append('<tr><td class="food_name">'+ data["item"][f]["oname"] +'</td><td class="food_num">×'+ data["item"][f]["onumber"] +'</td><td class="food_price">'+ data["item"][f]["oprice"] +'￥</td></tr>')
                }

                $("a[href='/food']").attr("href", "/order_center")
            }
        })
    })

})