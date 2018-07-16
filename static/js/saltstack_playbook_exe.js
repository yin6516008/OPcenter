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
    });

    // tbody里input的全选与反选
    $("#chooseTbody").find(":checkbox").click(function () {
        $('.choose').attr('disabled', false);
        var length1 = $("#chooseTbody").find(":checkbox").length;
        var length2 = $("#chooseTbody").find(":checked").length;
        if (length1==length2) {
            $("#chooseAll").prop("checked",true);
        } else {
            $("#chooseAll").prop("checked",false);
        }
        // tbody 中每个input 勾选状态与选择按钮状态保持一致
        if (length2 > 0) {
            $('.choose').attr('disabled', false);
            // 点击选择按钮
            var arr = [];
            // var ckdNum = $("#chooseTbody").find(":checked");
            var ckdNum = $("#chooseTbody").find(":checkbox").prop('checked');
            for (var i = 0; i < ckdNum.length; i++) {
                var trNum = ckdNum[i];
                arr.push($(trNum).parent().parent());
            }
            console.log(arr);
            $('.choose').click(function () {
                $(this).attr('disabled', true);
                $('#haveChosen').append(arr);
                $('#haveChosen > tr').find("td > input[type='checkbox']").prop('checked', false);
            })
        } else {
            $('.choose').attr('disabled', true);
        }
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

})