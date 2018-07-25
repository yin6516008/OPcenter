$(function () {
    var divs = $('.wrapper-content');
    for (var i = 0; i < divs.length; i++) {
        var aTag = $(divs[i]).find('.btnShowAndDisplay');
        // console.log(aTag);
        var flag = true;
        $(aTag).click(function () {
            if (flag) {
                $(this).parent().parent().parent().siblings('.table-info').show();
                flag = false;
            } else {
                $(this).parent().parent().parent().siblings('.table-info').hide();
                flag = true;
            }
        })
    }

    var arr = [];
    var tds = $('.tbody > tr');
    for (var i = 0; i <tds.length; i++) {
        var td = tds[i];
        arr.push($(td).find('td:eq(3)'));
        arr.push($(td).find('td:eq(4)'));
        arr.push($(td).find('td:eq(5)'));
    }
    console.log(arr);
    for (var j = 0; j < arr.length; j++) {
        var eachTd = arr[j];
        $(eachTd).mouseenter(function () {
            console.log(123);
            if ($(this).find('div:eq(0)').text().length > 120) {
                $(this).find('.expand-div').show();
                $(this).find('.expand-div').text($(this).find('div:eq(0)').text());
            }
        }).mouseleave(function () {
            $('.expand-div').hide();
        })
    }
})