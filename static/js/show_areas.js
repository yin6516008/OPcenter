$(function () {
  $('.third-menu').hide()
  $('.dropdown-menu>li').mouseover(function () {
    $(this).find('.third-menu').show();
  })
  $('.dropdown-menu>li').mouseout(function () {
    $(this).find('.third-menu').hide();
  })

  // 点击"新增项目名称" 选择项目按钮变为input输入框
  $('#itemInput').hide()
  var projectId = null
  $('#itemAdd').click(function () {
    $('#itemChoice').hide()
    $('#itemInput').show()
    // 点击"新增项目名称" 清空隐藏域里input的value值 方便验证
    projectId = $('#project').val()
    $('#project').val('')
  })
  $('#itemInput').dblclick(function () {
    // 双击新增项目输入框 变回下拉选项框之前清空已经输入的值
    $(this).hide().val('')
    $('#itemChoice').show()
    $('#project').val(projectId)
  })

  // 双击 添加域名input框 将input改变为textarea框 再双击 切换
  $('textarea').hide()
  $('#itemDetail').dblclick(function () {
    $(this).hide().val('')
    $('textarea').show()
  })
  $('textarea').dblclick(function () {
    $(this).hide().val('')
    $('#itemDetail').show()
  })

  $('.dropdown-item').click(function () {
    $('#itemChoice').text($(this).text());
    $('[type="hidden"]').val($(this).val())
  })
  
  // 点击关闭按钮或者× 清除表单内的四个val值
  $('#btn_close_bottom').click(function () {
    $('#project').val('')
    $('#itemInput').val('')
    $('#itemDetail').val('')
    $('#domains').val('')
  })
  $('#btn_close_top').click(function () {
    $('#project').val('')
    $('#itemInput').val('')
    $('#itemDetail').val('')
    $('#domains').val('')
  })

  // 表单提交验证
  $('#btn_save').attr('disabled','true')  
  $(document).mousemove(function () {
    if($('#project').val() != '') {
      if($('#itemDetail').val() != '') {
        $('#btn_save').removeAttr("disabled")
      }else if($('#domains').val() != '') {
        $('#btn_save').removeAttr("disabled")
      }else {
        $('#btn_save').attr('disabled','true')
      }
    }

    if($('#itemInput').val() != '') {
      if($('#itemDetail').val() != '') {
        $('#btn_save').removeAttr("disabled")
      }else if($('#domains').val() != '') {
        $('#btn_save').removeAttr("disabled")
      }else {
        $('#btn_save').attr('disabled','true')
      }
    }
  })
})

