$(function () {
  // 当消息提示的信息为0时 隐藏消息数提示的圆点
 $('.badge.badge-danger.pull-right').each(function () {
   if($(this).text() == 0) {
     $(this).hide()
   }
 })
  //  点击确定按钮弹出提示框
  $('#btn_confirm').click(function (e) {
    var search_url = $('#inputSearch').val()
    if(search_url == '') {
      e.preventDefault()
      $('#search_tip').text('请输入域名！')
      $('.alert-danger').css("display", "block").addClass('fadeInRight')
      setTimeout(function () {
        $('.alert-danger').fadeOut()
      }, 1500)
    }else {
      $.ajax({
        type: "POST",
        url: "/webmoni/search/",
        data: {
            'url': search_url,
        },
        success: function (url_id) {
            if (url_id == 'no') {
                $('#search_tip').text('没有这个域名！')
                $('.alert-danger').css("display", "block").addClass('fadeInRight')
                setTimeout(function () {
                    $('.alert-danger').fadeOut()
                }, 1500)
            } else {
                window.location.href = "/webmoni/tables-" + url_id;
            }
        }
      })
    }
    
  })

  // ==========页码区域==========
  var id = null
  var idMax = null
  var idMin = null
  var pageNum = null
  var totalPages = Math.ceil(id / 20)  //总页数

  // 页面一加载 若tr的id大于20 则隐藏
  $('tbody>tr').each(function () {
    id = Number($(this).attr('id'))
    // console.log(id)
    if(id > 20) {
      $(this).hide()
    }
  })

  // 设置页码的点击事件
  $('.pageClick').click(function () {
    pageNum = Number($(this).text())
    idMax = pageNum * 20
    idMin = idMax - 19
    $('tbody>tr').each(function () {
      id = Number(($(this).attr('id')))
      if(idMin<=id & idMax>=id) {
        $(this).show()
      }else {
        $(this).hide()
      }
    })
    // 被点击的样式
    $('.pageClick').css({ "backgroundColor": "", "color": "" })    
    $(this).css({ "backgroundColor": "#999", "color": "#0d71c7" })
  })

  // 下一页的点击事件
  $('#next').click(function () {
    // 不点击页码 直接点击下一页的情况
    if(idMax === null) {
      idMax = 20
      idMin = 1
      pageNum++
    }
    // 获取到当前页展示的id 然后根据这个id往后加上20项显示
    if(idMax > id) {
      return false
    }
    idMax += 20
    idMin += 20
    $('tbody>tr').each(function () {
      id = Number(($(this).attr('id')))
      if(idMin<=id & idMax>=id) {
        $(this).show()
      }else {
        $(this).hide()
      }
    })
    // 下一页按钮被点击的样式
    pageNum++
    $('.pageClick').each(function () {
      if(pageNum === Number($(this).text())){
        $(this).css({ "backgroundColor": "#999", "color": "#0d71c7" })
      }else {
        $(this).css({ "backgroundColor": "", "color": "" })
      }
    })
  })

  // 上一页的点击事件
  $('#previous').click(function () {
    // 不点击页码 直接点击上一页的情况
    if(idMax === null) {
      idMax = 20
      idMin = 1
      pageNum--
    }
    if(idMin == 1) {
      return false
    }
    idMax -= 20
    idMin -= 20
    $('tbody>tr').each(function () {
      id = Number(($(this).attr('id')))
      if(idMin<=id & idMax>=id) {
        $(this).show()
      }else {
        $(this).hide()
      }
    })
    // 上一页按钮被点击后的样式
    pageNum--
    $('.pageClick').each(function () {
      if(pageNum === Number($(this).text())){
        $(this).css({ "backgroundColor": "#999", "color": "#0d71c7" })
      }else {
        $(this).css({ "backgroundColor": "", "color": "" })
      }
    })
  })

})