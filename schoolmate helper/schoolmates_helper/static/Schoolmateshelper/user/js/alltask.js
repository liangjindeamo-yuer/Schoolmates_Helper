var flag = true;

$(function () {
    $('a').click(function () {
        if (!flag) {
            return false;
        }
    });
});

on_click_alltask = function (task_id, is_login) {
    flag = false;
    $.getJSON('/App/receivetask/', {'task_id': task_id, 'is_login': is_login}, function (data) {
        if (data['status'] === 200) {
            alert('任务已接受，请到个人中心查看');
        } else if (data['status'] === 905) {
            alert('请先激活您的账户');
            flag=true;
        } else if (data['status'] === 906) {
            alert('请先登录您的账户!');
            flag=true;
        }
        location.reload();
    })
};