$(function () {
  // 防止收起左侧边栏的时候右上角用户信息隐藏
  $('.navbar-minimalize.minimalize-styl-2.btn.btn-primary ').click(function () {
    $('.dropdown.profile-element').show()
  })

  // 点击左上角logo区 返回首页
  $('.nav-header').click(function () {
    window.location.href = '/index/'
  })

  // 鼠标移入左侧边栏项目 清除类样式ulhide
  $('#side-menu>li').mouseover(function () {
    $(this).find('ul').removeClass('ulhide')
  })
})