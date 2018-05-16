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

  // 若tr的id大于20 则隐藏
  $('tbody>tr').each(function () {
    var id = ($(this).attr('id'))
    if(id > 20) {
      $(this).hide()
    }
  })
  // 设置页码的点击事件
  $('.pageClick').click(function () {
    var pageNum = $(this).find('a').text()
    var idMax = pageNum * 20
    var idMin = idMax - 19
    $('tbody>tr').each(function () {
      var id = Number(($(this).attr('id')))
      console.log(id)
      if(id>=idMin & idMax>=id) {
        $(this).show()
      }else {
        $(this).hide()
      }
    })
  })

})