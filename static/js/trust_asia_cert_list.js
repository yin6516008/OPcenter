$(function () {

    // 模态框--详情界面
    $('.btnDetail').click(function () {
        var sha1Value = $(this).attr('sha1');
        var restDay = $(this).attr('restDay');
        $.ajax({
            type: "POST",
            url: "/cert/TrustAsia_cert_detail/",
            data: {'sha1': sha1Value,},
            success: function (msg) {
                var data = JSON.parse(msg);
                console.log(data);
                if (data.code == 0) {
                    $('#generalName').html(data['msg']['common_name']);
                    $('#brand').html(data['msg']['brand']);
                    $('#backupName').html(data['msg']['dns_names']);
                    $('#issuerSha1').html(data['msg']['issuer_sha1']);
                    $('#keyAlgo').html(data['msg']['key_algo']);
                    $('#signAlgo').html(data['msg']['sign_algo']);
                    $('#sha1Val').html(data['msg']['sha1']);
                    $('#sha2Val').html(data['msg']['sha2']);
                    $('#snVal').html(data['msg']['sn']);
                    $('#beginDate').html(data['msg']['begin_date']);
                    $('#endDate').html(data['msg']['end_date']);
                    $('#restDay').html(restDay + '天');
                    $('#addDate').html(data['msg']['created_at']);
                }
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
        var sha1Value = $(this).attr('sha1');
        var $this = $(this);
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
                        url: "/cert/TrustAsia_cert_delete/",
                        data: {'sha1': sha1Value},
                        success: function (msg) {
                            var data = JSON.parse(msg);
                            if (data.code == 0) {
                                $this.parent().parent().parent().parent().remove();
                            }
                        }
                    })
                } else {
                    swal("取消！", "取消删除成功。",
                        "error");
                }
        });
    });

    // 证书下载
        // Nginx证书下载
    // function downloadNginx() {
        $('.cert_download').click(function () {
            var domain = $(this).attr('domain');
            $('#cert_for_nginx').attr('href', '/cert/download/nginx/' + domain +"/")
            $('#cert_for_iis').attr('href', '/cert/download/iis/' + domain +"/")

        })
    // }
    // downloadNginx();

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