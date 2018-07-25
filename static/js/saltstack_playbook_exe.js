$(function () {


    // -------------主机列表选择按钮---------
    // 页面初始化选择按钮和移除按钮默认处于禁止点击状态
    $('.choose').attr('disabled', true);
    $('.remove').attr('disabled', true);
    $('.empty').attr('disabled', true);
    $('.implement').attr('disabled', true);
    $('#receivedAll').attr('disabled', true);

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

        $('.choose').click(function () {
            $('#receivedAll').attr('disabled', false);
            $('.empty').attr('disabled', false);
            var thArr = [];
            var thArr_el = $("#chooseTbody").find(":checked");
            thArr.push($(thArr_el).parent().parent());
            $('#haveChosen').append(thArr);
            $('#haveChosen > tr').find("td > input[type='checkbox']").prop('checked', false);
            $('#chooseAll').prop('checked', false);
            $('.choose').attr('disabled', true);
            chooseFn1();
            chooseFn2();
        })
        // chooseFn1();
        // chooseFn2();
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
            $('#receivedAll').attr('disabled', false);
            $('.empty').attr('disabled', false);
            var arr = [];
            var ckdNum = $("#chooseTbody").find(":checked");
            for (var i = 0; i < ckdNum.length; i++) {
                var trNum = $(ckdNum[i]).parent().parent();
                arr.push(trNum);
            }
            $(this).attr('disabled', true);
            // console.log(arr);
            $('#haveChosen').append(arr);
            $('#haveChosen > tr').find("td > input[type='checkbox']").prop('checked', false);
            chooseFn2();
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
    function chooseFn1() {
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
            $('.remove').click(function () {
                $('#receivedAll').attr('disabled', true);
                $('.empty').attr('disabled', true);
                removeTr();
            })
        });
    }
    chooseFn1();

    function chooseFn2() {
        // tbody里input的全选与反选
        $("#haveChosen").find(":checkbox").click(function () {
            // $('.remove').attr('disabled', false);
            // $('.empty').attr('disabled', false);
            var length3 = $("#haveChosen").find(":checkbox").length;
            var length4 = $("#haveChosen").find(":checked").length;
            if (length3 == length4) {
                $("#receivedAll").prop("checked",true);
            } else {
                $("#receivedAll").prop("checked",false);
            }
            // tbody 中每个input 勾选状态与选择按钮状态保持一致
            if (length4 > 0) {
                $('.remove').attr('disabled', false);
                $('.empty').attr('disabled', false);
            } else {
                $('.remove').attr('disabled', true);
                $('.empty').attr('disabled', true);
            }
            $('.remove').click(function () {
                $('#receivedAll').attr('disabled', true);
                $('.empty').attr('disabled', true);
                removeTr();
            })
        });
    }
    chooseFn2();

    // 封装移除函数
    function removeTr() {
        var arr_sec = [];
        var ckdNumSec = $("#haveChosen").find(":checked");
        for (var i = 0; i < ckdNumSec.length; i++) {
            var trNumSec = $(ckdNumSec[i]).parent().parent();
            arr_sec.push(trNumSec);
        }
        $(this).attr('disabled', true);
        // console.log(arr_sec);
        $('#chooseTbody').prepend(arr_sec);
        $('#chooseTbody > tr').find("td > input[type='checkbox']").prop('checked', false);
        $('#receivedAll').prop('checked', false);
        $('.remove').attr('disabled', true);
        $('.empty').attr('disabled', true);
    }
    removeTr();

    // 清空所选
    $('.empty').click(function () {
        var arr_trd = [];
        var trNum = $('#haveChosen > tr');
        arr_trd.push(trNum);
        $('#chooseTbody').prepend(arr_trd);
        $(this).attr('disabled', true);
        $('#receivedAll').prop('checked', false);
        $('#receivedAll').attr('disabled', true);
    })

    //-----------------选择剧本--------------
    function choosePlaybook() {
        $('#playbookList').find(':radio').click(function () {
            if ($('#playbookList').find(':checked').length > 0) {
                $('.implement').attr('disabled', false);
            }
        });
        $('.implement').click(function () {
            var playbookId;
            var descInfo;
            var inputs = $('#playbookList').find(':radio');
            for (var i = 0; i < inputs.length; i++) {
                var input = inputs[i];
                if ($(input).prop('checked') == true) {
                    playbookId = $(input).parent().siblings('td:eq(0)').attr('playbook_id');
                    descInfo = $(input).parent().siblings('td:eq(2)').text();
                }
            }
            console.log(playbookId);
            var list = [];
            var list_el = $('#haveChosen').find(':checkbox');
            for (var i = 0; i < list_el.length; i++) {
                // console.log(list_el);
                var minionId = $(list_el[i]).parent().siblings('td:eq(0)').attr('minion_id');
                list.push(minionId);
            }
            console.log(list);
            $('.hostNum').text(list.length);
            $('.playbookType').text(descInfo);

            if ($('.hostNum').text() == 0) {
                $('#confirmImplement').attr('disabled', true);
            } else {
                $('#confirmImplement').attr('disabled', false);
            }
            $('#confirmImplement').click(function () {
                $.ajax({
                    type: 'POST',
                    url: '/saltstack/playbook_exe_sls/',
                    data: {
                        'minion_id_list': JSON.stringify(list),
                        'playbook_id': playbookId
                    },
                    success: function (msg) {
                        var data = JSON.parse(msg);
                        window.location.reload();
                        if (data.code == 0) {
                            // $('#implementLog').prepend(`
                            //                             <tr>
                            //                                 <td>${data.data.total}</td>
                            //                                 <td>${data.data.number}</td>
                            //                                 <td>${data.data.description}</td>
                            //                                 <td>${data.data.create_time}</td>
                            //                                 <td>${data.data.finish_time}</td>
                            //                             </tr>`);
                            $('#startImplement').hide();
                            $('.modal-backdrop').hide();
                        }
                    }
                });
            })
        })
    }
    choosePlaybook();
    
    //-----------查看详情-------------
    $('.showInfo').click(function () {
        $('#playbookResult').show();
        var number = $(this).siblings('td:eq(1)').attr('number');
        var jid = $(this).siblings('td:eq(1)').attr('jid');
        if (jid == 0) {
            $('.lookupJid').hide();
        } else {
            $('.jobId').text(jid);
        }
        var description = $(this).siblings('td:eq(2)').attr('description');
        var createTime = $(this).siblings('td:eq(3)').attr('ctime');
        var finishTime = $(this).siblings('td:eq(4)').attr('ftime');
        $('.jobNumber').text(number);
        $('.jobDesc').text(description);
        $('.jobCtime').text(createTime);
        $('.jobFtime').text(finishTime);
        console.log(number);
        $.ajax({
            type: 'POST',
            url: '/saltstack/playbook_exe_ret/',
            data: {'number': number},
            success: function (msg) {
                console.log(msg);
                $('#playbookResult').hide();
                var data = JSON.parse(msg);
                console.log(data);
                // if (data.code == 0) {
                //     // var obj = JSON.parse(data.data.infomation);
                //     // var obj = JSON.parse(data.data.infomation);
                    var jsonObj = JSON.stringify(data,null,2);
                    $('.wrap').text(jsonObj);
                //     $('.wrap').text(data.data.infomation);
                // }
            }
        })
    })
    // 左侧边栏
    $('#side-menu>li:nth-of-type(3)').addClass('active')
    $('#side-menu>li:nth-of-type(3)>ul').removeClass('ulhide')
    $('#side-menu>li:nth-of-type(3)>ul').addClass('collapse')
    $('#side-menu>li:nth-of-type(3)>ul').addClass('in')
})