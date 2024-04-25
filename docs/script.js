$(document).ready(function () {
    var header = $('header'); // 更改为与HTML中类名匹配的选择器
    var originalTop = header.offset().top;

    $(window).scroll(function() {
        if ($(this).scrollTop() > originalTop) {
            header.addClass('-fixed');
        } else {
            header.removeClass('-fixed');
        }
    });
});