var flag = true;

relievetask = function (task_id) {
    flag = false;
    $.getJSON('/App/relievetask/',{'task_id':task_id,},function (data) {
          alert('已与该委托者解除任务，任务将重新放回任务大厅');
          location.reload();
          event.preventDefault();

    })
};
finishtask = function (task_id) {
    flag = false;
    alert('任务已完成，快去评价吧！');
    $.getJSON('/App/finishtask/',{'task_id':task_id,},function(data){
        window.location.href='/App/taskcontent/task_id/';
    })
};
modifytask = function (task_id) {
    flag = false;
    alert('开始修改任务信息');
    window.location.href='/App/modifytask/'+task_id.toString()+'/';

};

$(function () {
    $('a').click(function () {
        if(!flag){
            return false;
        }
    });
});