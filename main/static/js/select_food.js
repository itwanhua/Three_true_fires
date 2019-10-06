$(function(){
    var count = 0;
    var foods = {}; 

    $('.select .add').on('click',function(){
        count = parseInt($(this).next().val()) + 1
        $(this).next().val(count)
        foods[$(this).parent().next().html()]= count
        // console.log(foods[$(this).parent().next().html()])
    });

    $('.select .del').on('click',function(){
        if (parseInt($(this).prev().val()) > 1){
            count = parseInt($(this).prev().val()) - 1
            $(this).prev().val(count)
            foods[$(this).parent().next().html()]= count
            // console.log(foods[$(this).parent().next().html()])
        }
        else{
            count = 0 
            $(this).prev().val(count)
            delete foods[$(this).parent().next().html()]
            // console.log(foods)
            // console.log(foods[$(this).parent().next().html()])
        }
    });

    $('.car').on('click',function(){
        $('#dialog').show("slow"); 
    });

    $('.title img').on('click',function(){
        $('#dialog').hide("slow"); 
    });
})