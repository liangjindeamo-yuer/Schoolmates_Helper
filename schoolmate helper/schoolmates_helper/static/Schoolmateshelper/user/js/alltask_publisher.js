relievetask = function (task_id) {
    $.getJSON('/App/relievetask/',{'task_id':task_id,},function (data) {
          alert('已与该委托者解除任务，任务将重新放回任务大厅');
          location.reload();
    })
}