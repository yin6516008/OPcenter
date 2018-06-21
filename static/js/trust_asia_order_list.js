$(function () {

    // 模态框--详情界面
    $('.btnDetail').click(function () {
        var orderId = $(this).attr('order_id');
        $.ajax({
            type: "POST",
            url: "/cert/TrustAsia_order_detail/",
            data: { 'order_id': orderId },
            success: function (result) {
                var data = JSON.parse(result);
                $('#checkDomain').html(data['auth_key']);
                $('#txtRecord').html(data['auth_path']);
                $('#recordValue').html(data['auth_value']);
            }
        })
        $('#myModal').show();
    });

    // 关闭模态框
    $('#closeBtn').click(function () {
        $('#myModal').hide();
        $('.modal-backdrop').hide();
    });

    // 模态框--删除界面
    $('.btn-danger').click(function () {
        var orderId = $(this).attr('order_id');
        var status = $(this).attr('status');
        var _this = $(this);
        swal({
                title: "确定删除吗？",
                // text: "你将无法恢复该虚拟文件！",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "确定删除！",
                cancelButtonText: "取消删除！",
                closeOnConfirm: false,
                closeOnCancel: false
            },
            function(isConfirm){
                if (isConfirm) {

                    swal("删除！", "文件已经被删除。",
                        "success");
                    $.ajax({
                        type: "POST",
                        url: "/cert/TrustAsia_order_delete/",
                        data: {
                            "order_id": orderId,
                            "status": status
                        },
                        success: function (result) {
                            var data = JSON.parse(result);
                            console.log(data)
                            if (data.code == 0) {
                                _this.parent().parent().parent().parent().remove();
                            }
                        }
                    })
                } else {
                    swal("取消！", "取消删除成功。",
                        "error");
                }
            });
    });

    // 模态框--验证界面
    function checkResult() {
        $('.checkBtn').click(function () {
            var orderId = $(this).attr('order_id');
            var commonName = $(this).attr('common_name');
            $('#wave').show();
            $('#wave>h3').text('正在验证，请稍后···');
            $.ajax({
                type: 'POST',
                url: '/cert/TrustAsia_apply/Order_Authz/',
                data: {
                    'order': orderId,
                    'domain': commonName
                },
                success: function (msg) {
                    var data = JSON.parse(msg);
                        $('#wave').hide();
                        $('.checkMsg').html(data.msg);
                        console.log(data);
                        if (data.code == 0) {
                            $('.checkMsg').html('验证成功!');
                            setTimeout(function () {
                                $('#myModalCheck').hide();
                                $('.modal-backdrop').hide();
                                window.location.reload();
                            },2000);
                        } else {
                            $('.checkMsg').html(data.msg);
                            setTimeout(function () {
                                $('#myModalCheck').hide();
                                $('.modal-backdrop').hide();
                            },2000);
                        }
                }
            })
        })
    }
    checkResult();

    // 证书
    // function certification() {
    //     $('.btnCert').click(function () {
    //         var orderId = $(this).attr('order_id');
    //         $(this).attr('href', '/cert/TrustAsia_cert_select/' + orderId +'/');
    //     })
    // }
    // certification();

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
                $(this).css({ "backgroundColor": "#C6C6C7", "color": "#000" });
            }
        })
    }
    pagenation();

    // 域名搜索
    function searchDomain() {
        $('#btn_confirm').click(function () {
            var searchUrl = $('#search_domain').val()
            if ( searchUrl == '' ){
                $('#search_tip').text('此处不能为空!')
                $('.alert-danger').css("display", "block")
                setTimeout(function () {
                    $('.alert-danger').fadeOut()
                }, 1000)
            }else {
                $.ajax({
                    type: "POST",
                    url: "",
                    data: {
                        'url': searchUrl,
                    },
                    success: function () {

                    }
                })
            }
            $('#search_domain').val('')
        });

        $('#search_domain').keyup(function (e) {
            if(e.keyCode == '13') {
                $('#btn_confirm').click()
            }
        });
    }
    searchDomain();
})