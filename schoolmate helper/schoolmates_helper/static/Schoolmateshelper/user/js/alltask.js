$(function () {

})

on_click_alltask = function (task_id,is_login) {
     $.getJSON('/App/receivetask/',{'task_id':task_id,'is_login':is_login},function (data) {
         if(data['status']===200){
             alert('任务已接受，请到个人中心查看');
         }
         else if (data['status']===905){
             alert('请先激活您的账户');
         }
         else if (data['status']===906){
             alert('请先登录您的账户!');
         }
         location.reload();
     })
}