$(function () {
  // 左侧边栏
  $('#side-menu>li:nth-of-type(2)').addClass('active')
  $('#side-menu>li:nth-of-type(2)>ul').removeClass('ulhide')
  $('#side-menu>li:nth-of-type(2)>ul').addClass('collapse')
  $('#side-menu>li:nth-of-type(2)>ul').addClass('in')

    // ================新增模态框================
    // 点击"新增项目名称" 选择项目按钮变为input输入框
    // $('#btn_save').attr('disabled', true);
    var domain = $('#itemDetail').val();
    var project = $('#itemChoice').text();

    $('#itemChoice').click(function () {
        var project = $('#itemChoice').text();
        // if (project != '') {
        //     $('#btn_save').attr('disabled', false);
        // } else {
        //     $('#btn_save').attr('disabled', true);
        // }

        // $('#btn_save').attr('disabled', true);
        // $('#itemInput').bind('input propertychange', function () {
        //     if ($(this).val() != '') {
        //         $('#btn_save').attr('disabled', false);
        //     } else {
        //         $('#btn_save').attr('disabled', true);
        //     }
        // })
    })
    $('#itemDetail').bind('input propertychange', function () {
        var domain = $('#itemDetail').val();
        if (domain != '') {
            $('#btn_save').attr('disabled', false);
        } else {
            $('#btn_save').attr('disabled', true);
        }
    })

    $('#itemInput').hide()
    var projectId = null
    $('#itemAdd').click(function () {
        $('.cdn_value').val('');
        // $('#add_notadd').parent().css('checked', '');
        // $('#add_notwarn').parent().css('checked', '');
        $('#add_notadd').parent().removeClass('checked');
        $('#add_notwarn').parent().removeClass('checked');
        $('.node-position>div').css('checked');
        $('#errMsg').text('');

        $('#itemChoice').hide()
        $('#itemInput').show()
        // 点击"新增项目名称" 清空隐藏域里input的value值 方便验证
        projectId = $('#project').val()
        $('#project').val('')
        // $('#btn_save').attr('disabled', true);
    })
    $('#itemInput').dblclick(function () {
        // 双击新增项目输入框 变回下拉选项框之前清空已经输入的值
        $(this).hide().val('')
        $('#itemChoice').show()
        $('#project').val(projectId)
    })
    // 双击 添加域名input框 将input改变为textarea框 再双击 切换
    $('textarea').hide()
    $('#itemDetail').dblclick(function () {
        $(this).hide().val('')
        $('textarea').show()
    })
    $('textarea').dblclick(function () {
        $(this).hide().val('')
        $('#itemDetail').show()
    })
    // 点击下拉列表的选项
    $('.dropdown-item-add').click(function () {
        $(this).hide()
        $('#itemChoice').text($(this).text());
        $('#add_edit_form').find('[type="hidden"]').val($(this).val())
    })


    // 点击关闭按钮或者× 清除表单内的四个val值 复选框勾选清除
    $('#btn_close_bottom,#btn_close_top').click(function () {
        $('#project,#itemInput,#itemDetail,#domains').val('')
        $('#add_notadd,#add_notwarn').attr('checked', false)
    })

    // 点击操作按钮显示弹窗的位置
    $('tbody > tr').each(function (item, el) {
        if ($(el).attr('id') == 20) {
               $(el).find('td:eq(9)').find('.dropdown-menu').css('top', '-120px');
        }
        // console.log(el)
        // if (item == 19) {
        //     el.click(function () {
        //         console.log(123);
        //         $('.dropdown-menu').css('top', '-120px');
        //     })
        // }
    })
    // var lastTr = $('tbody > tr:last').find('td:eq(9)');
    // $(lastTr).click(function () {
    //     $('.dropdown-menu').css('top', '-120px');
    // })
    // 表单提交验证
    // $('#btn_save').attr('disabled', 'true')
    // $(document).mousemove(function () {
    //     if ($('#project').val() != '') {
    //         if ($('#itemDetail').val() != '') {
    //             $('#btn_save').removeAttr("disabled")
    //         } else if ($('#domains').val() != '') {
    //             $('#btn_save').removeAttr("disabled")
    //         } else {
    //             $('#btn_save').attr('disabled', 'true')
    //         }
    //     }
    //
    //     if ($('#itemInput').val() != '') {
    //         if ($('#itemDetail').val() != '') {
    //             $('#btn_save').removeAttr("disabled")
    //         } else if ($('#domains').val() != '') {
    //             $('#btn_save').removeAttr("disabled")
    //         } else {
    //             $('#btn_save').attr('disabled', 'true')
    //         }
    //     }
    // })
    $('#btn_save').click(function () {
        var arr = [];
        var cdn = $('.cdn_value').val() || '';
        var domain = $('#itemDetail').val();
        var project = $('#itemChoice').text();
        if ($("#itemInput").css('display') == 'block') {
            project = $('#itemInput').val();
        }
        if ($("#domains").css('display') == 'inline-block') {
            domain = $('#domains').val();
        }
        console.log(domain);
        console.log(project);

        var check = $('#add_notadd').parent().prop('checked') ? 1 : 0;
        var warning = $('#add_notwarn').parent().prop('checked') ? 1 : 0;
        var areaIdNum = $('.node-position > .icheckbox_square-green');
        for (var i = 0; i < areaIdNum.length; i++) {
            var areaId = areaIdNum[i];
            if ($(areaId).hasClass('checked')) {
                arr.push($(areaId).find('input').attr('area_id'));
            }
        }
        // console.log(arr);
        $.ajax({
            type: 'POST',
            url: '/webmoni/create/',
            data: {
                'cdn': cdn,
                'domain': domain,
                'project': project,
                'check_id': check,
                'warning': warning,
                'nodes': JSON.stringify(arr)
            },
            success: function (msg) {
                var data = JSON.parse(msg);
                if (data.code == 0) {
                    window.location.reload();
                } else {
                    $('#errMsg').text(data.data);
                }
            }
        })
    })





  // ================消息提示框================
  $('#btn_confirm').click(function (e) {
    var search_url = $('#inputSearch').val()
    if ( search_url == '' ){
        $('#search_tip').text('请输入域名')
        $('.alert-danger').css("display", "block")
        setTimeout(function () {
          $('.alert-danger').fadeOut()
        }, 2000)
    }else {
        $.ajax({
            type: "POST",
            url: "/webmoni/tables/search/",
            data: {
                'url': search_url,
            },
            success: function (url_id) {
                if (url_id == 'no') {
                    $('#search_tip').text('没有这个域名！')
                    $('.alert-danger').css("display", "block").addClass('fadeInRight')
                    setTimeout(function () {
                        $('.alert-danger').fadeOut()
                    }, 2000)
                } else {
                    console.log(url_id)
                    window.location.href = "/webmoni/tables/search-" + url_id + '/';
                }
            }
        })
    }
    $('#inputSearch').val('')
  })
  // 监听回车事件
  $('#inputSearch').keyup(function (e) {
    if(e.keyCode == '13') {
      $('#btn_confirm').click()
    }
  })

  // 改变警告为“否”的背景颜色
  $('tbody>tr>td').each(function () {
    if($(this).text().trim() == '否') {
      $(this).css('backgroundColor','#ffffcc')
    }
    var $that = $(this)
    $(this).parent().mouseenter(function () {
      $that.css('backgroundColor','')
    })
    $(this).parent().mouseleave(function () {
      if($that.text().trim() == '否') {
        $that.css('backgroundColor','#ffffcc')
      }
    })
  })
  // 调整第20行操作选项菜单
  $('tbody>tr>td:nth-of-type(9)').each(function () {
    $(this).click(function () {
      if($(this).siblings(':first').text() == 20) {
        $('.tableArea .dropdown-menu').removeClass('fadeInUp').addClass('fadeInDown')
        .css({ 'box-shadow':'0 -6px 12px rgba(0,0,0,.3)', 'top':'-84px' })
      }else {
        $('.tableArea .dropdown-menu').removeClass('fadeInDown').addClass('fadeInUp')
        .css({ 'box-shadow':'', 'top':'' })
      }
    })
  })
  
  // 删除按钮
  $('[data-target="#delDomain"]').click(function () {
    var node = $(this).parent().parent().parent()
    .parent().parent()
    // 获取到对应的tr的节点号 --> 填充到隐藏域value
    var nodeNum = node.attr("data-id")
    $('#delete').val(nodeNum)

    // 确认删除模态框中添加对应节点名
    var nodeDomain = node.find('td:nth-of-type(3)').text()
    $('#delModalLabel').text('确认删除域名 "'+ nodeDomain + '" 吗?')
  })

  // =========删除的模态框==========
  $('#confirmDel').click(function () { //点击确认按钮
    // $('.modal-backdrop').click(function () { //使点击遮罩失效
    //   $('#waving').show()
    // })
    var $that = $(this).siblings('input').val()
    // $('tbody>tr[data-id='+ $that +']').remove()
    // 请求数据
    $.ajax({
      type: "POST",
      url: "/webmoni/tables/delete/",
      data: {'url_id': $('#delete').val()},
      success: function (result) {
        if (result == 'OK') {
          window.location.reload()
        }
      }
    })
  })

  // 编辑按钮
  // $('[data-target="#editDomain"]').click(function () {
  //   var node = $(this).parent().parent().parent()
  //   .parent().parent()
  //   // 隐藏域value值
  //   var nodeNum = node.attr('data-id')
  //   $('#edit').val(nodeNum)
  //   $('#itemDetail_cate').val(node.find('td:nth-of-type(2)').text())
  //   $('#itemDetail_edit').val(node.find('td:nth-of-type(3)').text())
  //   // 拿到是否检测和是否警告的状态
  //   $checkStatus = node.find('td:nth-of-type(7)').text()
  //   $warningStatus = node.find('td:nth-of-type(8)').text()
  //   if($checkStatus == '否') {
  //     $('#edit_notadd').prop('checked','true')
  //   }
  //   if($warningStatus == '否') {
  //     $('#edit_notwarn').prop('checked','true')
  //   }
  //
  //   // =========编辑的模态框==========
  //   $('#btn_save_edit').click(function () {
  //     var $check_id = $(this).parent().prev().find('[name="check_id"]').is(':checked')
  //     var $warning = $(this).parent().prev().find('[name="warning"]').is(':checked')
  //     $check_id == true ? $check_id = "1" : $check_id = "0";
  //     $warning == true ? $warning = "1" : $warning = "0";
  //     $.ajax({
  //       type: "POST",
  //       url: "/webmoni/tables/edit/",
  //       data: {
  //         'id': nodeNum,
            //'domian',
                //'cdn',
  //         'check_id': $check_id,
  //         'warning': $warning
  //       },
  //       success: function (result) {
  //         if (result == 'true') {
  //           window.location.reload()
  //         }else {
  //           alert('修改失败！')
  //         }
  //       }
  //     })
  //   })
  //
  // })

  // 关闭编辑模态框 清除选中的值
  $('#btn_close_bottom_edit,#btn_close_top_edit').click(function () {
    $('#edit_notadd,#edit_notwarn').attr('checked',false)
  })

    // updated 编辑按钮 + 模态框
    $('[data-target="#editDomain"]').click(function () {

        //
        $('#edit_notadd').parent().iCheck('check');
        $('#edit_notwarn').parent().iCheck('check');


        $('#cdn_domain,#itemDetail_edit').val('');
        console.log($('#edit_notadd').parent());
        $('#edit_notadd').parent().removeClass('checked');
        $('#edit_notwarn').parent().removeClass('checked');
        // $('.edit-position>div').removeClass('checked');
        $('#errMsg').text('');

        // $('.edit-position>div').find('input').iCheck('toggle');

        var dataId = $(this).parent().parent().parent().parent().parent().attr('data-id');
        $.ajax({
            type: 'GET',
            url: '/webmoni/tables/edit/',
            data: {'id': dataId},
            success: function (msg) {
                var data = JSON.parse(msg);
                console.log(data.data);
                if (data.code == 0) {


                    $('#itemDetail_edit').val(data.data.domain_info.url)
                    $('#btn_save_edit').val(data.data.domain_info.id)
                    $('#cdn_domain').val(data.data.domain_info.cdn)
                    $('#edit_notadd').parent().addClass(0 == data.data.domain_info.check_id ? '' : 'checked');
                    $('#edit_notwarn').parent().addClass(0 == data.data.domain_info.warning ? '' : 'checked');

                    $('#edit_notadd').parent().iCheck('check');
                    $('#edit_notwarn').parent().iCheck('check');

                    var arrSelected = data.data.domain_info.nodes;
                    for (var i = 0; i < arrSelected.length; i++ ){
                        var node = arrSelected[i]
                        // $("input[area_id='"+ node +"']").parent().addClass('checked');
                        $("input[area_id='"+ node +"']").parent().iCheck('check');
                    }
                    var liValue = $(".edit_ul > li[value='"+data.data.domain_info.project_name+"']").find('a').text();
                    $('#editBtn').text(liValue);
                }
            }
        })
    })

        // // 同步项目
        // var node = $(this).parent().parent().parent().parent().parent();
        // var nodeNum = node.attr('data-id');
        // var projectId = $(this).attr('project_id');
        // var domain = $(this).attr('domain');
        // var cdn = $('#cdn_domain').val();
        var lis = $('.edit_ul').children();
        for (var i = 0; i < lis.length; i++) {
            if ($(lis[i]).attr('value') == projectId) {
                $('#editBtn').html($(lis[i]).children('a').html());
            }
            var li = lis[i];
            $(li).click(function () {
                $('#editBtn').html(($(this).children('a').html()));

            })
        }
        //
        // // 同步域名
        // $('#itemDetail_edit').attr('value', domain);
        //
        // $('#cdn_domain').attr('value', cdn);
        // $('#edit_notadd').parent().prop('checked',);
        // $('#edit_notwarn').parent().prop('checked',);
        //
        // $('#edit').val(nodeNum)
        // $('#itemDetail_cate').val(node.find('td:nth-of-type(2)').text())
        // $('#itemDetail_edit').val(node.find('td:nth-of-type(3)').text())
        // // 拿到是否检测和是否警告的状态
        // $checkStatus = node.find('td:nth-of-type(7)').text()
        // $warningStatus = node.find('td:nth-of-type(8)').text()
        // if($checkStatus == '否') {
        //     $('#edit_notadd').prop('checked','true')
        //   }
        // if($warningStatus == '否') {
        //     $('#edit_notwarn').prop('checked','true')
        //   }

        // 表单提交验证
        // $('#btn_save_edit').attr('disabled', 'true');
        // $(document).mousemove(function () {
        //         if ($('#itemDetail_edit').val() != '') {
        //             $('#btn_save_edit').removeAttr('disabled');
        //         } else {
        //             $('#btn_save_edit').attr('disabled', 'true');
        //         }
        // })

    $('.addNew').click(function () {
        console.log(1)
        $('.cdn_value').val('');
        $('#add_notadd').parent().removeClass('checked');
        $('#add_notwarn').parent().removeClass('checked');
        $('.node-position>div').removeClass('checked');
        $('#errMsg').text('');
    })


    // 提交表单
    $('#btn_save_edit').click(function () {
        var arr = [];
        var dataId = $('#btn_save_edit').val()
        var $check_id = $('#edit_notadd').parent().hasClass('checked') ? 1 : 0;
        var $warning = $('#edit_notwarn').parent().hasClass('checked') ? 1 : 0;

        var domain = $('#itemDetail_edit').val();
        var cdn = $('#cdn_domain').val();
        var editNum = $('.edit-position > .icheckbox_square-green');
        console.log(editNum.length);
        var project = $('#editBtn').text()
        for (var i = 0; i < editNum.length; i++) {
            var areaId = editNum[i];
            if ($(areaId).hasClass('checked')) {
                arr.push($(areaId).find('input').attr('area_id'));
            }
        }
        console.log(arr);
        $.ajax({
            type: "POST",
            url: "/webmoni/tables/edit/",
            data: {
                'id': dataId,
                'domain': domain,
                'cdn': cdn,
                'project':project,
                'check_id': $check_id,
                'warning': $warning,
                'nodes': JSON.stringify(arr)
            },
            success: function (msg) {
                var data = JSON.parse(msg)
                if (data.code == 0) {
                    $('#myModalCheck').hide();
                    $('.modal-backdrop').hide();
                    window.location.reload();
                }else {
                    alert('修改失败！')
                }
            }
        })

    })

    // 更新证书
    $('.update_cert').click(function () {
        var url = $(this).find('a').attr('url');
        var $this = $(this);
        $.ajax({
            type: 'POST',
            url: '/webmoni/tables/update_cert/',
            data: {
                'url_id': url
            },
            success: function (msg) {
                var data = JSON.parse(msg);
                if (data.code == 0) {
                    $this.parent().parent().parent().siblings('td:eq(4)').text('检测中').css('color', 'salmon');
                    $this.parent().parent().parent().siblings('td:eq(5)').text('检测中').css('color', 'salmon');
                }
            }
        })
    })

    // 更新全部证书
    $('.update_all_cert').click(function () {
        $.ajax({
            type: 'POST',
            url: '/webmoni/tables/update_all_cert/',
            data: {'now': 'yes'},
            success: function (msg) {
                var result = JSON.parse(msg);
                console.log(result);
                if (result.code == 0) {
                    $('#updateAllCert').hide();
                    $('.modal-backdrop').hide();
                    $('.cert_check').text(result.data);
                } else {
                    $('.modal-body').removeClass('modal-display-none').addClass('modal-display');
                    $('.modal-footer').css('marginTop', 0);
                    $('.modal-body').find('span').text(result.data);
                }
            }
        })
    })

  // 改变翻页的样式
  var paramNum = window.location.pathname.replace(/[^0-9]/ig,"") || 1
  $('#pageUl').find('li').children().each(function () {
    if($(this).text() == paramNum) { //页数等于地址栏参数
      $(this).css({ "backgroundColor": "#C6C6C7", "color": "#0d71c7" })
      // 分页过多以···显示
      $(this).parent().prev().prev().prev().prevAll().hide() //当页之前 除邻近3项 全部隐藏
      $(this).parent().next().next().next().nextAll().hide() //当页之后 除邻近3项 全部隐藏
      $(this).parent().prev().prev().prev().children().text('···')
      $(this).parent().next().next().next().children().text('···')
    }
  })
  $('#previous').parent().show().children().html('&laquo;')
  $('#next').parent().show().children().html('&raquo;')


})
