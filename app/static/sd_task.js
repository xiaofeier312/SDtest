/**
 * Created by xiaofeier312 on 2018/7/25.
 */


$(document).ready(function () {
    $('td button').click(function () {
        sub_task_id=$(this).attr('id').slice(3);
        console.log('click id----:');
        console.log(sub_task_id);
        console.log($(this).html());
        $.ajax({
            type:'GET',
            url: '/task/complete_sub_task/'+sub_task_id,
            sucess:function(data){
                alert('Success!');
            }
        })
    })
})