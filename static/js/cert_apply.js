$(function () {
  $('#side-menu>li:nth-of-type(5)').addClass('active')
  $('#side-menu>li:nth-of-type(5)>ul').removeClass('ulhide')
  $('#side-menu>li:nth-of-type(5)>ul').addClass('collapse')
  $('#side-menu>li:nth-of-type(5)>ul').addClass('in')

  $('#getTXT').click(function () {
      var domain = $('.certInput').val()
      $.ajax({
          url:'/cert/apply/postdomain/',
          data:{'domain':domain},
          type:'post',
          success:function (msg) {
              var result = JSON.parse(msg)
              $('#host').text(result['host'])
              $('#TXT').text(result['TXT'])
          }
      })
  })


})