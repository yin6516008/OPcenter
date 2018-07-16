$(function () {
    // -------------主机列表选择按钮---------
    // 页面初始化选择按钮和移除按钮默认处于禁止点击状态
    $('.choose').attr('disabled', true);
    $('.remove').attr('disabled', true);
    $('.empty').attr('disabled', true);

    // thead里input的全选与反选
    $("#chooseAll").click(function () {
        var th_ckd = $(this).prop("checked");
        if (th_ckd) {
            $('.choose').attr('disabled', false);
        } else {
            $('.choose').attr('disabled', true);
        }
        $("#chooseTbody").find(":checkbox").prop("checked",th_ckd);
        forbidClick();
        var thArr = [];
        var allTr = $('#chooseTbody > tr').find('td').siblings('td:eq(4)');
        console.log(allTr.length);
        for (var i = 0; i < allTr.length; i++) {
            var tr = allTr[i];
            thArr.push($(tr));
        }
        console.log(thArr);
    });

    // tbody里input的全选与反选
    $("#chooseTbody").find(":checkbox").click(function () {
        $('.choose').attr('disabled', false);
        var length1 = $("#chooseTbody").find(":checkbox").length;
        var length2 = $("#chooseTbody").find(":checked").length;
        if (length1 == length2) {
            $("#chooseAll").prop("checked",true);
        } else {
            $("#chooseAll").prop("checked",false);
        }
        // tbody 中每个input 勾选状态与选择按钮状态保持一致
        if (length2 > 0) {
            $('.choose').attr('disabled', false);
        } else {
            $('.choose').attr('disabled', true);
        }

        $('.choose').click(function () {
            var arr = [];
            var ckdNum = $("#chooseTbody").find(":checked");
            for (var i = 0; i < ckdNum.length; i++) {
                var trNum = $(ckdNum[i]).parent().parent();
                arr.push(trNum);
            }
            $(this).attr('disabled', true);
            console.log(arr);
            $('#haveChosen').append(arr);
            $('#haveChosen > tr').find("td > input[type='checkbox']").prop('checked', false);
        })
    });

    // 处于离线状态对应的input框禁止勾选点击
    function forbidClick() {
        var trs = $('#chooseTbody > tr');
        for (var i = 0; i < trs.length; i++) {
            var tr = trs[i];
            if ($(tr).find('td').siblings('td:eq(4)').text() == '离线') {
                $(tr).find("td > input[type='checkbox']").attr('disabled', true);
                $(tr).find("td > input[type='checkbox']").prop('checked', false);
            }
        }
    }
    forbidClick();

    //-----------------已选择的主机操作部分--------------
    // thead里input的全选与反选
    $('#receivedAll').click(function () {
        var received_ckd = $(this).prop('checked');
        if (received_ckd) {
            $('.remove').attr('disabled', false);
            $('.empty').attr('disabled', false);
        } else {
            $('.remove').attr('disabled', true);
            $('.empty').attr('disabled', true);
        }
        $('#haveChosen').find(':checkbox').prop('checked',received_ckd);
    })


    //-----------------选择剧本--------------
    $('.implement').click(function () {
        var list = [];
        var list_el = $('#haveChosen').find(':checked');
        // console.log(list_el.length);
        for (var i = 0; i < list_el.length; i++) {
            console.log(list_el);
            var minionId = $(list_el[i]).parent().siblings('td:eq(0)').attr('minion_id');
            list.push(minionId);
        }
        console.log(list);
    })
})