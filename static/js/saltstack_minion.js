$(function () {
    // 系统类型选择
    function sysTypeChoose() {
        $('.panel-type > div').find('input').click(function () {
            $(this).siblings('i').css('transform', 'rotate(180deg)');
            $(this).siblings('ul').slideDown(500);
            $(this).siblings('ul').find('li').each(function (i) {
                $(this).click(function () {
                    $(this).parent().siblings('input').val($(this).find('a').text());
                    $(this).parent().slideUp(500).siblings('i').css('transform', 'rotate(360deg)');
                })

            })
        });
    }
    sysTypeChoose();
    // 点击搜索框箭头显示隐藏列表
    var flag1 = true;
    $('.system_type > i').click(function () {
        if (flag1) {
            $(this).css('transform', 'rotate(180deg)');
            $(this).siblings('ul').slideDown(500);
            $('.panel-type > div > ul > li').click(function () {
                $(this).parent().siblings('input').val($(this).find('a').text());
                $(this).parent().slideUp(500).siblings('i').css('transform', 'rotate(360deg)');
            })
            flag1 = false;
        } else {
            $(this).css('transform', 'rotate(360deg)');
            $(this).siblings('ul').slideUp(500);
            flag1 = true;
        }
    })

    // var flag2 = true;
    // $('.choose-group > i').click(function () {
    //     if (flag2) {
    //         $(this).css('transform', 'rotate(180deg)');
    //         $(this).siblings('ul').slideDown(500);
    //         $('.choose-group > ul > li').click(function () {
    //             $(this).parent().siblings('input').val($(this).find('a').text());
    //             $(this).parent().slideUp(500).siblings('i').css('transform', 'rotate(360deg)');
    //         })
    //         flag2 = false;
    //     } else {
    //         $(this).css('transform', 'rotate(360deg)');
    //         $(this).siblings('ul').slideUp(500);
    //         flag2 = true;
    //     }
    // })

    // 鼠标移出隐藏列表
    $('.system_type > input').blur(function () {
        $('.system_type > ul').slideUp(500);
        $(this).siblings('i').css('transform', 'rotate(360deg)');
    })
    // $('.choose-group > input').blur(function () {
    //     $('.choose-group > ul').slideUp(500);
    //     $(this).siblings('i').css('transform', 'rotate(360deg)');
    // })

    // 选择分组
    $('.choose-group > button').click(function () {
        var lis = $('.choose-group > ul').children();
        for (var i = 0; i < lis.length; i++) {
            var li = lis[i];
            $(li).click(function () {
                $('.choose-group > button').text($(this).find('a').text());
                $('.choose-group > button > span').removeClass('caret');
            })
        }
    })


    // 添加信息
    $('.addInfo').click(function () {
        var id = $(this).attr('instanceId');
        var reg = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
        var ipv4 = $('.ipAddr').val();
        var city = $('.cityPosition').val();
        if ($('.ipAddr').val() == '' || $('.cityPosition').val() == '') {
            $('.closeBtn').attr('disabled', true);
        }
        // 验证IP地址
        $('.ipAddr').blur(function () {
            var ipv4 = $(this).val();
            var reg = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
            if (ipv4 == '') {
                $('.ip_err_blank').show();
                $('.ip_err_format').hide();
            } else if (!reg.test(ipv4)) {
                $('.ip_err_blank').hide();
                $('.ip_err_format').show();
            } else {
                $('.ip_err_blank').hide();
                $('.ip_err_format').hide();
            }
        });
        // 验证地理位置
        $('.cityPosition').bind('input propertychange',function () {
            var city = $(this).val();
            if (city != '') {
                $('.closeBtn').attr('disabled', false);
                $('.position_err_blank').hide();
            } else {
                $('.closeBtn').attr('disabled', true);
                $('.position_err_blank').show();
            }
        })
        $('.cityPosition').blur(function () {
            var city = $(this).val();
            if (city == '') {
                $('.position_err_blank').show();
            } else {
                $('.position_err_blank').hide();
                $('.closeBtn').attr('disabled', false);
            }
        })
        $('.closeBtn').click(function () {
            var ipv4 = $('.ipAddr').val();
            var city = $('.cityPosition').val();

            $.ajax({
                type: 'POST',
                url: '/saltstack/minion_add/',
                data: {
                    'id': id,
                    'ipv4': ipv4,
                    'city': city,
                },
                success: function (msg) {
                        console.log(msg);
                        $('.modal-backdrop').hide();
                        $('#addIpAndPosition').hide();
                        window.location.href = '/saltstack';
                }
            })
        })
        // 点击×号或点击取消，清空模态框内容
        $('.close > span:eq(0)').click(function () {
            $('.ipAddr').val('');
            $('.cityPosition').val('');
            $('.ip_err_blank').hide();
            $('.ip_err_format').hide();
            $('.position_err_blank').hide();
        });
        $('.modal-footer > button:eq(0)').click(function () {
            $('.ipAddr').val('');
            $('.cityPosition').val('');
            $('.ip_err_blank').hide();
            $('.ip_err_format').hide();
            $('.position_err_blank').hide();
        })
    })

    //搜索
    // function search() {
    //     $('.tab_search').click(function () {
    //         var id = $('.panel-type > label:eq(0)').find('input').val();
    //         var ipv4 = $('.panel-type > label:eq(1)').find('input').val();
    //         var osfinger = $('.panel-type > div').find('input').val();
    //         if (id == '' && ipv4 == '' && osfinger == '') {
    //             alert('请至少填入一项！');
    //             return false;
    //         } else {
    //             $.ajax({
    //                 type: 'POST',
    //                 url: '/saltstack/minion_search/',
    //                 data: {
    //                     'id': id,
    //                     'ipv4': ipv4,
    //                     'osfinger': osfinger
    //                 },
    //                 success: function (msg) {
    //                     console.log(msg);
    //                 }
    //             })
    //         }
    //     })
    // }
    // search();
    
    // 刷新列表
    function refrshList() {
        $('.tab_refresh').click(function () {
            $.ajax({
                type: 'POST',
                url: '/saltstack/minion_test/',
                data: {
                    'id': '*'
                },
                success: function (msg) {
                    console.log(msg);
                }
            })
        })
    }
    refrshList();

    // 状态检测
        if ($('#check_status').prop('checked', false) && $('#tbody').find(':checkbox').prop('checked', false)) {
            $('.management > button').attr('disabled', true);
            $('.management > a').attr('disabled', true);
        } else {
            $('.management > button').attr('disabled', false);
            $('.management > a').attr('disabled', false);
        }

        var th_arr = [];
        $('#check_status').click(function () {
            var ckd = $(this).prop('checked');
            $('#tbody').find(':checkbox').prop('checked', ckd);
            if (ckd) {
                $('.management > button').attr('disabled', false);
                $('.management > a').attr('disabled', false);
                var idNum = $('#tbody > tr');
                for (var i = 0; i < idNum.length; i++) {
                    var idArr = idNum[i];
                    th_arr.push($(idArr).find('td').eq(2).attr('salt_id'));
                }
                console.log(th_arr);
                // 提交状态
                $('.management > button').click(function () {
                    $.ajax({
                        type: 'POST',
                        url: '/saltstack/minion_test/',
                        data: {
                            'id': JSON.stringify(th_arr)
                        },
                        success: function (msg) {
                            var data = JSON.parse(msg);
                            console.log(data);
                            if (data.code == 0) {
                                window.location.reload();
                            }
                        }
                    })
                })
            } else {
                $('.management > button').attr('disabled', true);
                $('.management > a').attr('disabled', true);
            }
        });

    $('#tbody').find(':checkbox').click(function () {
            var len1=$('#tbody').find(':checkbox').length;
            var len2=$('#tbody').find(':checked').length;
            if(len1==len2){
                $('#check_status').prop('checked', true);
            }else{
                $('#check_status').prop('checked', false);
            }
            if (len2 > 0) {
                $('#implementCheck').attr('disabled', false);

            } else {
                $('.management > button').attr('disabled', true);
                $('.management > a').attr('disabled', true);

            }
        });
    $('#implementCheck').click(function () {
        var tb_arr = [];
        var checkedNum = $('#tbody').find(':checked');
        for (var i = 0; i < checkedNum.length; i++) {
            var perChecked = $(checkedNum[i]).parent().siblings('td:eq(1)').attr('salt_id');
            tb_arr.push(perChecked);
        }
        console.log(tb_arr);
        $.ajax({
            type: 'POST',
            url: '/saltstack/minion_test/',
            data: {
                'id': JSON.stringify(tb_arr)
            },
            success: function (msg) {
                var data = JSON.parse(msg);
                if (data.code == 0) {
                    window.location.reload();
                }
            }
        })
    })


    // 主机管理
    function hostArrangement() {
        $('.host-content-transfer').find('input').click(function () {
            $(this).siblings('i').css('transform', 'rotate(180deg)');
            $(this).siblings('ul').slideDown(500);
            $(this).siblings('ul').find("li:not('.lastLi')").click(function () {
                $(this).parent().siblings('input').val($(this).find('a').text());
                $('#hostMove').attr('disabled', false);
                $('.lastLi').click(function () {
                    $('#hostMove').attr('disabled', true);
                    $(".host-content-transfer > ul").slideUp(500);
                    $('#chooseOrNewGroup').val('').focus().attr('placeholder', '请输入新建分组的名称');
                })
                $(this).parent().slideUp(500).siblings('i').css('transform', 'rotate(360deg)');
            })
        });
    }
    hostArrangement();
    // 点击搜索框箭头显示隐藏列表
    var hostFlag = true;
    $('.host-content-transfer > i').click(function () {
        if (hostFlag) {
            $(this).css('transform', 'rotate(180deg)');
            $(this).siblings('ul').slideDown(500);
            $(".host-content-transfer > ul > li:not('.lastLi')").click(function () {
                $(this).parent().siblings('input').val($(this).find('a').text());
                $('#hostMove').attr('disabled', false);
                $('.lastLi').click(function () {
                    $('#hostMove').attr('disabled', true);
                    $(".host-content-transfer > ul").slideUp(500);
                    $('#chooseOrNewGroup').val('').focus().attr('placeholder', '请输入新建分组的名称');
                })
                $(this).parent().slideUp(500).siblings('i').css('transform', 'rotate(360deg)');
            })
            hostFlag = false;
        } else {
            $(this).css('transform', 'rotate(360deg)');
            $(this).siblings('ul').slideUp(500);
            hostFlag = true;
        }
    })

    // 鼠标移出隐藏列表
    $('.host-content-transfer > input').blur(function () {
        $('.host-content-transfer > ul').slideUp(500);
        $(this).siblings('i').css('transform', 'rotate(360deg)');
    });
    // 分组管理
    // 未勾选主机ID禁止提交


    // if ($('#check_status').prop('checked', false) && $('#tbody').find(':checkbox').prop('checked', false)) {
    //     $('.management > a').attr('disabled', true);
    // } else {
    //     $('.management > a').attr('disabled', false);
    // }

    // $('#check_status').click(function () {
    //     var cked = $(this).prop('checked');
    //     $('#tbody').find(':checkbox').prop('checked', cked);
    //     if (cked) {
    //         $('.management > a').attr('disabled', false);
    //     } else {
    //         $('.management > a').attr('disabled', true);
    //     }
    // });
    // $('#tbody').find(':checkbox').click(function () {
    //
    //     var length1 = $('#tbody').find(':checkbox').length;
    //     var length2 = $('#tbody').find(':checked').length;
    //     if (length1 == length2) {
    //         $('#check_status').prop('checked', true);
    //     } else {
    //         $('#check_status').prop('checked', false);
    //     }
    //     if (length2 > 0) {
    //         $('.management > a').attr('disabled', false);
    //     } else {
    //         $('.management > a').attr('disabled', true);
    //
    //     }
    // })



    $('#arrangeHost').click(function () {
        $('#hostMove').attr('disabled', true);
        var host_arr = [];
        var hostNum = $('#tbody').find(':checked').prop('checked', true);
        for (var i = 0; i < hostNum.length; i++) {
            var perHostId = hostNum[i];
            host_arr.push($(perHostId).parent().parent().find('td:eq(2)').text());
        }
        $('.host-content > p > span').text(host_arr.length);
        if ($('.host-content > p > span').text() == 0) {
            $('#hostMove').attr('disabled', true);
        }

        $('#chooseOrNewGroup').focus(function () {
            if ($(this).val() == '') {
                $('#hostMove').attr('disabled', true);
            } else {
                $('#hostMove').attr('disabled', false);
                $('#hostMove').click(function () {
                    console.log(host_arr);
                    var hostName = $('#chooseOrNewGroup').val();
                    console.log(hostName);
                    $.ajax({
                        type: 'POST',
                        url: '/saltstack/project_manage/',
                        data: {
                            'id': JSON.stringify(host_arr),
                            'project': hostName
                        },
                        success: function (msg) {
                            var data = JSON.parse(msg);
                            console.log(data);
                        }
                    })
                });
            }
        })
        $('#chooseOrNewGroup').blur(function () {
            if ($(this).val() == '') {
                $('#hostMove').attr('disabled', true);
            } else {
                $('#hostMove').attr('disabled', false);
                $('#hostMove').click(function () {
                    console.log(host_arr);
                    var hostName = $('#chooseOrNewGroup').val();
                    console.log(hostName);
                    $.ajax({
                        type: 'POST',
                        url: '/saltstack/project_manage/',
                        data: {
                            'id': JSON.stringify(host_arr),
                            'project': hostName
                        },
                        success: function (msg) {
                            var data = JSON.parse(msg);
                            console.log(data);
                        }
                    })
                });
            }
        })
    });




    // 分页
    function  pagenation() {
        var re = /(\d+)\/$/.exec(window.location.pathname)
        if (re == null) {
            var paramNum = 1
        } else {
            var paramNum = re[1]
        }
        $('.pagination > li > a').each(function () {
            if($(this).text() == paramNum) {
                console.log(paramNum);
                $(this).css({ "backgroundColor": "#C6C6C7", "color": "#000" });
            }
        })
    }
    pagenation();
})