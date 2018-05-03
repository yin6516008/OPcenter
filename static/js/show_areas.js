$(function () {
  $('.third-menu').hide()
  $('.dropdown-menu>li').mouseover(function () {
    $(this).find('.third-menu').show();
  })
  $('.dropdown-menu>li').mouseout(function () {
    $(this).find('.third-menu').hide();
  })

  // 点击"点此新增项目名称"按钮将 选择项目按钮变为input输入框
  $('#itemInput').hide()
  // $('#itemChoice').dblclick(function () {
  //   $('#itemChoice').hide()
  //   $('#itemInput').show()
  // })
  $('#itemAdd').click(function () {
    console.log(8888)
    $('#itemChoice').hide()
    $('#itemInput').show()
  })
  $('#itemInput').dblclick(function () {
    $(this).hide()
    $('#itemChoice').show()
  })

  // 双击 添加域名input框 将input改变为textarea框 再双击 切换
  $('textarea').hide()
  $('#itemDetail').dblclick(function () {
    $(this).hide()
    $('textarea').show()
  })
  $('textarea').dblclick(function () {
    $(this).hide()
    $('#itemDetail').show()
  })
})

