checktask = function () {
    var $comment = $('#comment_input');
    var comment = $comment.val().trim();
    if (!comment) {
        var $comment_info = $('#comment_info');
        $comment_info.html('好歹说两句').css('color', 'grey');
        alert("评论不能为空");
        return false;
    }
    alert('添加评价成功');
    return true;
};
