$(function () {
  $('#side-menu>li:nth-of-type(5)').addClass('active')
  $('#side-menu>li:nth-of-type(5)>ul').removeClass('ulhide')
  $('#side-menu>li:nth-of-type(5)>ul').addClass('collapse')
  $('#side-menu>li:nth-of-type(5)>ul').addClass('in')

  $('#getTXT').click(function () {
      $('#wave').show() // 点击按钮 显示动画
      $('#TXT_info').hide()
      $('#err').hide()
      $('#certList').hide().html('')
      $('#record').text('系统操作信息：')
      var domain = $('#inputBox').val()
      $.ajax({
          url:'/cert/apply/postdomain/',
          data:{'domain':domain},
          type:'post',
          success:function (msg) {
              $('#wave').hide()
              var result = JSON.parse(msg)
              var TXT = result.TXT
              var excode = result.excode //后台记录
              $('#record').append('<hr/>').append(excode) //后台记录添加到右侧
              if(result.status == 'OK') {
                $('#TXT_info').show()
                var host = result.host
                $('#hostname').text(host)
                $('#TXTval').text(TXT)
              }else if ( result.status == 'SUCCESS'){
                $('#certList').show()
                var files = res.files
                for(var i=0; i<files.length; i++) {
                var fileName = files[i]
                $('#certList>ul').prepend("<li><a href='/cert/download/"+domain+"/"+fileName+"/'>"+fileName+"</a></li>")
                }
              }else {
                $('#err').show()
              }
          }
      })


  })
      

  $('#generateCert').click(function () {
      var domain = $('#inputBox').val()
      $('#err').hide()
      $('#wave').show()
      $('#wave>h3').text('证书生成中，请稍后···')
      $.ajax({
          url: '/cert/apply/genercert/',
          data: {'domain':domain},
          type: 'post',
          success: function (msg) {
              $('#wave').hide()
              var res = JSON.parse(msg)
              var excode = res.excode
              $('#record').append('<hr/>').append(excode)
              if(res.status == 'OK') {
                  // 正确返回的处理
                  $('#certList').show()
                  var files = res.files
                  for(var i=0; i<files.length; i++) {
                      var fileName = files[i]
                      $('#certList>ul').prepend("<li><a href='/cert/download/"+domain+"/"+fileName+"/'>"+fileName+"</a></li>")
                  }
              }else {
                  $('#err').show() //出错提示
              }
          }
      })
  })

  // 监听输入框回车事件
  $('#inputBox').keyup(function (e) {
    if(e.keyCode == 13) {
      $('#getTXT').click()
    }
  })
  // 点击复制
  $('#copyHostname').click(function () {
      copyContent('hostname')
      $(this).after($('<span>复制成功！</span>'))
      $(this).next().css({'padding-bottom':'0', 'color':'#f10b0b', 'font-size':'15px'})
      setTimeout(function () {
          $('#copyHostname').next().hide()
      }, 1500)
  })
  $('#copyTxtval').click(function () {
      copyContent('TXTval')
      $(this).after($('<span>复制成功！</span>'))  
      $(this).next().css({'padding-bottom':'0', 'color':'#f10b0b', 'font-size':'15px'})
      setTimeout(function () {
          $('#copyTxtval').next().hide()
      }, 1500)
  })
  function copyContent(sourceId) {
      var Url2=document.getElementById(sourceId).innerText;
      var oInput = document.createElement('input')
      oInput.value = Url2
      document.body.appendChild(oInput)
      oInput.select()
      document.execCommand("Copy")
      oInput.className = 'oInput'
      oInput.style.display='none'
  }
})