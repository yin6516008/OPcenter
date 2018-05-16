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
})