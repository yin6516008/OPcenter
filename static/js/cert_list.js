$(function () {
    $('#side-menu>li:nth-of-type(5)').addClass('active')
    $('#side-menu>li:nth-of-type(5)>ul').removeClass('ulhide')
    $('#side-menu>li:nth-of-type(5)>ul').addClass('collapse')
    $('#side-menu>li:nth-of-type(5)>ul').addClass('in')

    $("#filterName").keyup(function(e) {
        $(".file-manager>ul>li")
          .hide()
          .filter(":contains('" + ($(this).val()).trim() + "')")
          .show();
        if($(this).val().trim() == "") {
          $(".file-manager>ul>li")
          .show()
        }
    });

    $('.folder-list>li>a').click(function () {
        var domain = $(this).parent().attr('data-name')
        $.ajax({
            url:'/cert/getfile/',
            type:'post',
            data:{'domain':domain},
            success:function (msg) {
                var files = JSON.parse(msg)
                $('#file_table').html('')
                for (i in files){
                    var file = `<div class='file-box'>
                                  <div class='file'>
                                     <a href='/cert/download/${domain}/${files[i]}'>
                                        <span class='corner'></span>
                                        <div class='icon'>
                                            <i class='fa fa-file'></i>
                                        </div>
                                        <div class='file-name'>${files[i]}
                                            <br/>
                                        </div>
                                     </a>
                                 </div>`

                    var postname = files[i].split('.')[files[i].split('.').length - 1]
                    var file_table = $('#file_table')
                    var file_fa = $(file).find('.fa')
                    if(postname == 'conf') {
                        file_table.append(file_fa.removeClass('fa-file').addClass('fa-cog').parents('.file-box')[0])
                    }else if(postname == 'key') {
                        file_table.append(file_fa.removeClass('fa-file').addClass('fa-key').parents('.file-box')[0])
                    }else if(postname == 'cer') {
                        file_table.append(file_fa.removeClass('fa-file fa').addClass('iconfont icon-zhengshu-copy').parents('.file-box')[0])
                    }

                }
            }
        })
    })

    var $that = null
    $('.folder-list>li>a:nth-of-type(2)').click(function () {
        var domainName = $(this).parent().attr('data-name')
        $('#myModalLabel').text('确认删除域名"'+domainName+'"吗？')
        $('#hiddenIput').val(domainName)
        $that = $(this)
    })

    // 模态框确认删除按钮
    $('#btnConfirm').click(function () {
        var domain = $('#hiddenIput').val()
        $.ajax({
            url:'/cert/delete/',
            type:'post',
            data:{'domain':domain},
            success:function (msg) {
                if ( msg == 'OK'){
                    $that.parent().remove()
                    $('#file_table').empty()
                    $('#btnClose').click()
                }else{
                    window.location.reload()
                }
            }
        })
    })

    // 模态框关闭按钮
    $('#btnClose, #cross').click(function () {
        $('#hiddenIput').val('')
    })
})