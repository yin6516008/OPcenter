$(function () {
  $('#side-menu>li:nth-of-type(5)').addClass('active')
  $('#side-menu>li:nth-of-type(5)>ul').removeClass('ulhide')
  $('#side-menu>li:nth-of-type(5)>ul').addClass('collapse')
  $('#side-menu>li:nth-of-type(5)>ul').addClass('in')

  $('#getTXT').click(function () {
      $('#wave').show() // 点击按钮 显示动画
      if($('#TXT_info').is(':visible')) {
        $('#TXT_info').hide()
      }
      if($('#err').is(':visible')) {
        $('#err').hide()
      }
      var domain = $('.input-lg').val()
      $.ajax({
          url:'/cert/apply/postdomain/',
          data:{'domain':domain},
          type:'post',
          success:function (msg) {
              $('#wave').hide()
              var result = JSON.parse(msg)
              if(result.status == 'OK') {
                $('#TXT_info').show()
                var TXT = result.TXT
                $('#hostname').text('_acme-challenge')
                $('#TXTval').text(TXT)
              }else {
                $('#err').show()
                var errInfo = result.data
                $('#err>pre').text(errInfo)
              }
          }
      })

      $('#generateCert').click(function () {
        $('#wave').show()
        $('#wave>h3').text('证书生成中，请稍后···')
        $.ajax({
          url: '/cert/apply/genercert/',
          data: {'domain':domain},
          type: 'post',
          success: function (msg) {
            $('#wave').hide()
            var res = JSON.parse(msg)
            if(res.status == 'OK') {
              // 正确返回的处理
              $('#certList').show()
              var files = res.files
              for(var i=0; i<files.length; i++) {
                var fileName = files[i]
                $('#certList>ul').prepend("<li><a href='/cert/apply/"+domain+"/"+fileName+"/'>"+fileName+"</a></li>")
              }
            }else {
              // 错误的处理
              $('#err').show()
              $('#err>pre').text(res.data)
            }
          }
        })
      })
      
  })


})