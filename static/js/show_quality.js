$(function () {
  // 左侧边栏
  $('#side-menu>li:nth-of-type(2)').addClass('active')
  $('#side-menu>li:nth-of-type(2)>ul').removeClass('ulhide')
  $('#side-menu>li:nth-of-type(2)>ul').addClass('collapse')
  $('#side-menu>li:nth-of-type(2)>ul').addClass('in')
  
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
  $('[data-target="#editDomain"]').click(function () {
    var node = $(this).parent().parent().parent()
    .parent().parent()
    // 隐藏域value值
    var nodeNum = node.attr('data-id')
    $('#edit').val(nodeNum)
    $('#itemDetail_cate').val(node.find('td:nth-of-type(2)').text())
    $('#itemDetail_edit').val(node.find('td:nth-of-type(3)').text())
    // 拿到是否检测和是否警告的状态
    $checkStatus = node.find('td:nth-of-type(7)').text()
    $warningStatus = node.find('td:nth-of-type(8)').text()
    if($checkStatus == '否') {
      $('#edit_notadd').prop('checked','true')
    }
    if($warningStatus == '否') {
      $('#edit_notwarn').prop('checked','true')
    }
    
    // =========编辑的模态框==========
    $('#btn_save_edit').click(function () {
      var $check_id = $(this).parent().prev().find('[name="check_id"]').is(':checked')
      var $warning = $(this).parent().prev().find('[name="warning"]').is(':checked')
      $check_id == true ? $check_id = "1" : $check_id = "0";
      $warning == true ? $warning = "1" : $warning = "0";
      $.ajax({
        type: "POST",
        url: "/webmoni/tables/edit/",
        data: {
          'url_id': nodeNum,
          'check_id': $check_id,
          'warning': $warning
        },
        success: function (result) {
          if (result == 'true') {
            window.location.reload()
          }else {
            alert('修改失败！')
          }
        }
      })
    })

  })

  // 关闭编辑模态框 清除选中的值
  $('#btn_close_bottom_edit,#btn_close_top_edit').click(function () {
    $('#edit_notadd,#edit_notwarn').attr('checked',false)
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
