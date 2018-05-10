$(function () {
  $('.third-menu').hide()
  $('.dropdown-menu>li').mouseover(function () {
    $(this).find('.third-menu').show();
  })
  $('.dropdown-menu>li').mouseout(function () {
    $(this).find('.third-menu').hide();
  })

  // ================新增模态框================
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
    $('#add_edit_form').find('[type="hidden"]').val($(this).val())
  })
  
  // 点击关闭按钮或者× 清除表单内的四个val值
  $('#btn_close_bottom,#btn_close_top').click(function () {
    $('#project,#itemInput,#itemDetail,#domains').val('')
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

  // ================修改模态框================
  // 点击"新增项目名称" 选择项目按钮变为input输入框
  $('#itemInput_edit').hide()
  // var projectId = null
  $('#itemAdd_edit').click(function () {
    $('#itemChoice_edit').hide()
    $('#itemInput_edit').show()
    // 点击"新增项目名称" 清空隐藏域里input的value值 方便验证
    // projectId = $('#project').val()
    $('#project_edit').val('')
  })
  $('#itemInput_edit').dblclick(function () {
    $(this).hide().val('')
    $('#itemChoice_edit').show()
    // $('#project').val(projectId)
  })
  $('#add_edit_editForm').find('.dropdown-item').click(function () {
    $('#itemChoice_edit').text($(this).text())
    $('#add_edit_editForm').find('[type="hidden"]').val($(this).val())
  })

  // 点击关闭按钮或者× 清除表单内的三个val值
  $('#btn_close_bottom_edit,#btn_close_top_edit').click(function () {
    $('#project_edit,#itemInput_edit,#itemDetail_edit').val('')
  })
  
})

