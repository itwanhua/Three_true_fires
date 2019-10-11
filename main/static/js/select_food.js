 // 页面加载，像服务器发出请求，获取商品数据
 
 $.ajax({
    url: "/get_food",
    success: function(data) {
        if (data["err"] === 0){
            // 成功获取数据
            for (var f in data["foods"]) {
                var a_parent_div_class = "item-food item-food-" + f
                // console.log(a_parent_div_class)
                $(".row").append(
                    "<div class='col-3'>\n" + 
                        "<div class='" + a_parent_div_class + "'>\n" + 
                            "<a class='" + f + "'>\n" +  
                                "<div class='price'>\n"+
                                    "<img src='../static/img/icon/huo.png'>\n"+
                                    "<span class='cost'>"+data["foods"][f]['price']+"</span><span>￥/"+data['foods'][f]['size']+"</span>\n"+
                                "</div>\n"+
                                "<div class='select'>\n" + 
                                    "<img src='../static/img/icon/jia.png' class='add'>\n" + 
                                    "<input type='text' value='0' disabled>\n" + 
                                    "<img src='../static/img/icon/jian.png' class='del'>\n" + 
                                "</div>\n" + 
                                "<h3>" + data["foods"][f]["fname"] + "</h3>\n" + 
                            "</a>\n" + 
                        "</div>\n" + 
                    "</div>"
                )
                // console.log(data["foods"][f]["img_path"])
                // console.log("/static/img/food/f-4.jpg")
                $("a[class='" + f + "']").css("background-image", "url("+data["foods"][f]["img_path"]+")")
                // $(".row a").css("background", "url("+ "/static/img/food/f-4.jpg" +")")
            }
            
        }
        else if (data["err"] === 1){
            console.log(data["desc"])
        }
    }
});

var token = $('input[name=csrfmiddlewaretoken]').val();

$(function(){
    $.ajaxSetup({
		data:{csrfmiddlewaretoken:'{{ csrf_token }}'}
	});

    var count = 0;
    var foods = {};
	var is_login = false;

    $.ajax({
        url: "/is_login",
        success: function(data){
            console.log(data)
            if (data["err"] === 0){
                // 已登录！
                is_login = true;
            }
            else {
                // 未登录
                is_login = false;
            }
        }
    });

    $('.row').delegate('.select .add','click',function(){
        pname = $(this).parent().next().html()
        count = parseInt($(this).next().val()) + 1
        price = parseInt($(this).parent().prev().children(".cost").html())
        elem = $(this).next()
        elem.val(count)
        foods[pname]= [count,price,elem]
        add()
        // console.log(foods[$(this).parent().next().html()])
    });

    $('.row').delegate('.select .del','click',function(){
        if (parseInt($(this).prev().val()) > 1){
            pname = $(this).parent().next().html()
            count = parseInt($(this).prev().val()) - 1
            price = parseInt($(this).parent().prev().children(".cost").html())
            elem = $(this).prev()
            elem.val(count)
            foods[pname][0]= count
            add()
            // console.log(foods[$(this).parent().next().html()])
        }
        else{
            pname = pname = $(this).parent().next().html()
            count = 0 
            $(this).prev().val(count)
            delete foods[pname]
            add()
            // console.log(foods)
            // console.log(foods[$(this).parent().next().html()])
        }
    });

    function add(){
        $('.car_info .good_list').remove()
        var sum = 0;
        var count = 0;
        for(var i in foods){
            count += foods[i][0];
            var pic = foods[i][0] * foods[i][1]
            sum += pic
            $('.car_info #top').after(
            "<tr class='good_list'><td><span name='good_name'>"+i+"</span></td><td><span name='good_count'>×"+foods[i][0] +"</span></td><td><span name='good_price'>"+pic+ "￥</span></td>"
            )
        }
        $('.car_info #sum_cnt').html(count+"件")
        $('.car_info #sum_pic').html(sum +"￥")
    };

    
    $("#clear").on("click",function(){
        $('.car_info .good_list').remove()
        for(var j in foods){
           foods[j][2].val(0)
        }
        foods = []
        $('.car_info #sum_cnt').html("件")
        $('.car_info #sum_pic').html("￥")
    });


    $(".car_info").delegate('#sub_order','click',function(){
        var gname = new Array()
        var gcont = new Array()
        var gpic = new Array()
        $('[name="good_name"]').each(function(key,value){
                        gname[key] = $(this).html()});

        $('[name="good_count"]').each(function(key,value){
                        gcont[key] = $(this).html()});

        $('[name="good_price"]').each(function(key,value){
                        gpic[key] = $(this).html()});
        // console.log(gname,gcont,gpic)
        if(Object.keys(foods).length != 0){
           $.ajax({
                type:"POST",
                url:"/order",
                data:{
                    csrfmiddlewaretoken:token,
                    order_name:JSON.stringify(gname),
                    order_count:JSON.stringify(gcont),
                    order_price:JSON.stringify(gpic),
                    sum_price:$('.car_info #sum_pic').html(),
                    sum_count: $('.car_info #sum_cnt').html()
                },
                success:function(data){  
                    localStorage.setItem('callbackHTML',data);
                    window.location.href = window.location.href.split('/food')[0] + '/submit';
                },
                error:function(){
                    alert("提交失败，请检查网络！")
                },  
           });
        }
    });



    $('.car').on('click',function(){
        // 若为登录状态，则可以进入购物车下单
        if (is_login == true) {
            $('#dialog').show("slow"); 
        }
        // 未登录状态，弹窗提示登陆
        else {
            alert("请登录！")
        }
    });

    $('.title img').on('click',function(){
        $('#dialog').hide("slow"); 
    });


    // 用户中心点击事件
    $("#nickname").bind({
        "click":function(){
            $(".user").hide()
            $(".user_menu").show()
        },
    });

})


