$(function () {
  $('#side-menu>li:nth-of-type(5)').addClass('active')
  $('#side-menu>li:nth-of-type(5)>ul').removeClass('ulhide')
  $('#side-menu>li:nth-of-type(5)>ul').addClass('collapse')
  $('#side-menu>li:nth-of-type(5)>ul').addClass('in')

  $('#getTXT').click(function () {
      $('#wave').show() // 点击按钮 显示动画
      var domain = $('.input-lg').val()
      $.ajax({
          url:'/cert/apply/postdomain/',
          data:{'domain':domain},
          type:'post',
          success:function (result) {
              $('#wave').hide()
              JSON.parse(result)
              if(result.status == 'OK') {
                $('#TXT_info').show()
                var host = result.host
                var TXT = result.TXT
                $('#hostname').text(host)
                $('#TXTval').text(TXT)
              }else {
                $('#err').show()
                var errInfo = result.data
                $('#err>pre').text(errInfo)
              }
          }
      })
  })


})