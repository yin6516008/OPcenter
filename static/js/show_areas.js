$(function () {
    $('#side-menu>li:nth-of-type(2)').addClass('active')
    $('#side-menu>li:nth-of-type(2)>ul').removeClass('ulhide')
    $('#side-menu>li:nth-of-type(2)>ul').addClass('collapse')
    $('#side-menu>li:nth-of-type(2)>ul').addClass('in')

    $('.third-menu').hide()
    $('.dropdown-menu>li').mouseover(function () {
        $(this).find('.third-menu').show();
    })
    $('.dropdown-menu>li').mouseout(function () {
        $(this).find('.third-menu').hide();
    })
    $('#itemAdd,#itemAdd_edit').parent().css("backgroundColor", "#18a689")

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
    // 点击下拉列表的选项
    $('.dropdown-item-add').click(function () {
        // $(this).hide()
        $('#itemChoice').text($(this).text());
        $('#add_edit_form').find('[type="hidden"]').val($(this).val())
    })


    // 点击关闭按钮或者× 清除表单内的四个val值 复选框勾选清除
    $('#btn_close_bottom,#btn_close_top').click(function () {
        $('#project,#itemInput,#itemDetail,#domains').val('')
        $('#add_notadd,#add_notwarn').attr('checked', false)
    })

    // 表单提交验证
    $('#btn_save').attr('disabled', 'true')
    $(document).mousemove(function () {
        if ($('#project').val() != '') {
            if ($('#itemDetail').val() != '') {
                $('#btn_save').removeAttr("disabled")
            } else if ($('#domains').val() != '') {
                $('#btn_save').removeAttr("disabled")
            } else {
                $('#btn_save').attr('disabled', 'true')
            }
        }

        if ($('#itemInput').val() != '') {
            if ($('#itemDetail').val() != '') {
                $('#btn_save').removeAttr("disabled")
            } else if ($('#domains').val() != '') {
                $('#btn_save').removeAttr("disabled")
            } else {
                $('#btn_save').attr('disabled', 'true')
            }
        }
    })

  // =================删除模态框====================
  $('[data-target="#delModal"]').click(function () {
    var name_title = $('#domainName').text()
    $('#delModalLabel').text('确认删除'+ name_title + '吗?')
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
  $('#add_edit_editForm').find('.dropdown-item-edit').click(function () {
    $('#itemChoice_edit').text($(this).text())
    $('#add_edit_editForm').find('[type="hidden"]').val($(this).val())
  })

  // 默认渲染到button按钮的值和列表中的值一样的时候 隐藏列表中的
  $('#add_edit_editForm').find('.dropdown-item-edit').children('a')
  .each(function(index, item) {
    var btnText = $('#itemChoice_edit').text()
    if($(item).text() == btnText) {
      $(item).parent().hide()
    }
  })
  
  
  // 点击关闭按钮或者× 清除表单内的三个val值
  $('#btn_close_bottom_edit,#btn_close_top_edit').click(function () {
    $('#edit_notadd,#edit_notwarn').attr('checked',false)
  })

  // ================消息提示框================
  $('#tip_close').click(function () {
    $(this).parent().hide()
  })

  $('#domainsUl>li').mouseover(function () {
    $(this).children('a').css('backgroundColor','#ccc')
  }).mouseleave(function () {
    $(this).children('a').css('backgroundColor','')
  })
  // 下拉菜单过长改变子选项显示位置
  function getMousePos(event) {
    var e = event || window.event;
    return {'x':e.clientX,'y':e.clientY}
  }
})

function update_graph(option,graph_data) {
    option['xAxis'][0]['data'] = graph_data['time_list']
        var color = [
            '255, 0, 0',
            '255, 150, 0',
            '150, 255, 0',
            '0, 255, 150',
            '0, 200, 255',
            '0, 100, 255',
            '0, 0, 255',
            '150, 0, 255',
            '255, 0, 255'
           ]
        for ( var i in graph_data['data']){
            var curve =   {
            name: '',
            type: 'line',
            smooth: true,
            symbol: 'circle',
            symbolSize: 5,
            showSymbol: false,
            lineStyle: {
                normal: {
                    width: 1
                }
            },
            areaStyle: {
                normal: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: ''
                    }, {
                        offset: 0.8,
                        color: ''
                    }], false),
                    shadowColor: 'rgba(0, 0, 0, 0.1)',
                    shadowBlur: 10
                }
            },
            itemStyle: {
                normal: {
                    color: '',
                    borderColor: '',
                    borderWidth: 12

                }
            },
            data: []
        }
            option['legend']['data'][i] = graph_data['data'][i]['node']
            curve['name'] = graph_data['data'][i]['node']
            curve['areaStyle']['normal']['color'].colorStops[0]['color'] = 'rgba(' + color[i] + ', 0.1)'
            curve['areaStyle']['normal']['color'].colorStops[1]['color'] = 'rgba(' + color[i] + ', 0)'
            curve['itemStyle']['normal']['color'] = 'rgba(' + color[i] + ')'
            curve['itemStyle']['normal']['borderColor'] = 'rgba(' + color[i] + ', 0.2)'
            curve['data'] = graph_data['data'][i]['values']
            option['series'][i] = curve

        }
        return option
 }



// ================消息提示框================
$('#btn_confirm').click(function (e) {
  var search_url = $('#inputSearch').val()
  if ( search_url == '' ){
      $('#search_tip').text('请输入域名')
      $('.alert-danger').css("display", "block")
      setTimeout(function () {
        $('.alert-danger').fadeOut()
      }, 2000)
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
                  }, 2000)
              } else {
                  window.location.href = "/webmoni/areas-" + url_id;
              }
          }
      })
  }
  $('#inputSearch').val('')
})
// 监听回车事件
$('#inputSearch').keyup(function (e) {
  if(e.keyCode == '13') {
    $('#btn_confirm').click()
  }
})

function timing_update(option,url_id) {
  $.ajax({
     type: "POST",
     url: "/webmoni/update_graph/",
     data: {
        'url_id': url_id,
      },
     success: function(graph_data) {
      //  console.log(JSON.parse(graph_data))
        var new_option = update_graph(option,JSON.parse(graph_data))
        myChart.setOption(new_option, true);
     }
})
}
