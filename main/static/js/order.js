var token = $('input[name=csrfmiddlewaretoken]').val();

$.ajaxSetup({
    data:{csrfmiddlewaretoken:'{{ csrf_token }}'}});

$('#pay_btn').on("click",function(){
    var fname = new Array() ;
    var fcnt = new Array();
    var fpic = new Array();

    $('.fname').each(function(key,value){
        fname[key] = $(this).text()});
    $('.fcnt').each(function(key,value){
        fcnt[key] = $(this).text()});
    $('.fpic').each(function(key,value){
        fpic[key] = $(this).text()});
    
    $.ajax({
        type:"POST",
        url:'/submit',
        data:{
            csrfmiddlewaretoken:token,
            order_name:JSON.stringify(fname),
            order_count:JSON.stringify(fcnt),
            order_price:JSON.stringify(fpic),
            order_id:$('#order_id').html(),
            time: $('#time').html(),
            customer:$('#customer').val(),
            phone:$('#phone').val(),
            target_addr:$('#target_addr').val(),
            sum_cnt:$('#sum_cnt').html(),
            sum_pic:$("#sum_pic").html(),
            remarks:$("#remarks").val(),
        },
        success:function(data){
            if (data['code'] == 0){
                $("#pay_btn").remove();
                $(".pay").append("<span>订单提交成功！</span><br><span>店长正在努力制作您的美食，请稍后。。。。</span>")
            }
            else{
                console.log(data)
                alert("提交失败，请稍后重试！")
            }
        },
        err:function(){
            alert("网络出故障了，请检查后重试！")
        }
    })
    

});