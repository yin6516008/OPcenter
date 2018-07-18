$(function () {
    // 上传剧本
    $('.btn-upload-playbook').click(function () {
        $('.show-file-name > span').text('未上传任何文件');
        $('#uploadPlayBook').attr('disabled', true);
    })
    // 上传文件
    $('#uploadFile').change(function () {
        $('#uploadPlayBook').attr('disabled', false);
        $('.show-file-name > span').text($(this).val());
        var size = $('#uploadFile')[0].files[0].size / 1024;
        if (size > 100) {
            $('.modal-tips').show();
            $('.modal-tips').find('span').text('请上传小于100kb的文件!');
            $('#uploadPlayBook').attr('disabled', true);
            setTimeout(function () {
                $('.modal-tips').hide();
            },1000)
        }
        if ($(this).val() == '') {
            $('.show-file-name > span').text('未上传任何文件');
        }
    })
    // 上传剧本
    $('#uploadPlayBook').click(function () {
        var form = new FormData(document.getElementById("uploadform"));
        $.ajax({
            url:'/saltstack/playbook_upload/',
            type: 'POST',
            data: form,
            contentType: false,
            processData: false,
            success: function (msg) {
                data = JSON.parse(msg)
                console.log(data);
                if (data.code == 0) {
                    $('.modal-tips').show();
                    $('.modal-tips').find('span').text(data.data);
                    setTimeout(function () {
                        $('.modal-tips').hide();
                        $('.modal').hide();
                        $('.modal-backdrop').hide();
                    },1000)
                }
                if (data.code == 9527) {
                    $('.modal-tips').show();
                    $('.modal-tips').find('span').text(data.data);
                    setTimeout(function () {
                        $('.modal-tips').hide();
                    },2000)
                }
            }
        })
    })

    // 选择分组
    $('.btn-group > button').click(function () {
        console.log(123);
        var lis = $('.btn-group > ul').children();
        for (var i = 0; i < lis.length; i++) {
            var li = lis[i];
            $(li).click(function () {
                $('.btn-group > button').text($(this).find('a').text());
                $('.btn-group > button > span').removeClass('caret');
            })
        }
    })

    //----------右侧编辑，删除，保存，取消操作-----------------------

    // 初始化页面禁止点击
    $('#edit_btn').attr('disabled', true);
    $('#del_btn').attr('disabled', true);
    $("tr[name='playbook_row']").click(function () {

        // 点击tr后允许按钮执行点击操作
        $('#del_btn').attr('disabled', false);
        $('#edit_btn').attr('disabled', false);

        // 获取路径
        var playbook_path = $(this).find('td:eq(3)').text();

        // 右侧显示对应内容
        if ( $(this).attr('show_status') == 1 ){
            return
        }else{
            $(this).attr('show_status',1).siblings('tr').removeAttr('show_status')
            var playbook_id = $(this).attr('playbook_id')
            $.ajax({
                url:'/saltstack/playbook_edit/',
                type:'POST',
                data:{'playbook_id':playbook_id},
                success:function (msg) {
                    var data = JSON.parse(msg)
                    $('#playbook_path').empty().append(data.data.playbook_path)
                    $('#playbook_show').empty().append(data.data.playbook_content)
                    var editor = ace.edit("playbook_editor")
                    editor.setValue(data.data.playbook_content)
                }
            })
        }

        // 编辑
        $('#edit_btn').click(function () {
            $('#playbook_show').hide();
            $('#playbook_editor').show();
            $('.save_and_cancel').show();
        });


        // 取消
        $('#cancel_btn').click(function () {
            $('#playbook_show').show();
            $('#playbook_editor').hide();
            $('.save_and_cancel').hide();
        })
    })
    // 删除
    $('#del_btn').click(function () {
        if ($("tr[name='playbook_row']")[0].hasAttribute('show_status')) {
            var playbook_path = $("tr[show_status='1']").find('td:eq(3)').text();
            $('#confirmDel').click(function () {
                $('#playbook_show').empty();
                // $('#playbook_editor').empty();
                $('#playbook_path').empty();
                $.ajax({
                    type: 'POST',
                    url: ' /saltstack/playbook_del/',
                    data: {
                        'playbook_path': playbook_path
                    },
                    success: function (msg) {
                        var data = JSON.parse(msg);
                        if (data.code == 0) {
                            $('tr').each(function (item, el) {
                                if (el.hasAttribute('show_status')) {
                                    el.remove();
                                }
                            })
                            $('.confirm-del').hide();
                            $('.modal-backdrop').hide();
                        }
                    }
                })
            })
        }
    });
    // 保存
    $('#save_btn').click(function () {
        var playbook_path;
        var trs = $("tr[name='playbook_row']");
        for (var i = 0; i < trs.length; i++) {
            var tr = trs[i];
            if (tr.hasAttribute('show_status')) {
                playbook_path = $(tr).find('td:eq(3)').text();
            }
        }
        var editor = ace.edit("playbook_editor");
        var playbook_context = editor.getValue();
        console.log(playbook_path);

        $('#confirmSave').click(function () {
            $.ajax({
                type: 'POST',
                url: '/saltstack/playbook_save/',
                data: {
                    'playbook_path': playbook_path,
                    'playbook_context': playbook_context
                },
                success: function (msg) {
                    var data = JSON.parse(msg);
                    if (data.code == 0) {
                        $('.confirm-save').hide();
                        $('.modal-backdrop').hide();

                        $('#playbook_show').show();
                        $('#playbook_editor').hide();
                        $('.save_and_cancel').hide();
                        $('#playbook_path').empty().append(data.data.playbook_path);
                        $('#playbook_show').empty().append(data.data.playbook_content);
                        editor.setValue(data.data.playbook_content);
                    }
                }
            })
        })
    });

})