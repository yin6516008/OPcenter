// 启用、隐藏模态框
$('#myModal').modal("hide")

$(function() {
  // $('.add_btn').on('click', function() {
  //     $('.domain_name').val() = '';
  // })

  $('.add_content').on('click', function() {
      var inputValue = [];
      var inputValue = $('.input-group').find('input').val();
      if (inputValue.length == 0) {
          $('.add_content').attr('disabled',true);
      }
      var tr = document.createElement('tr');
      $('tbody').prepend(tr);
      tr.innerHTML = `<td><a>${$('.domain_name').val()}<a></td>
                      <td>${$('.lisence_expire').val()}</td>
                      <td>${$('.rest_days').val()}</td>
                      <td>${$('.update_time').val()}</td>
                      <td>${$('.status').val()}</td>
                      <td>
                        <div class="btn-group">
                          <button type="button" class="btn btn-primary dropdown-toggle" data-toggle="dropdown">
                            操作 <span class="caret"></span>
                          </button>
                          <ul class="dropdown-menu" role="menu">
                            <li><a href="#">修改</a></li>
                            <li><a href="#">删除</a></li>
                          </ul>
                        </div>
                      </td>`;
      $('#myModal').modal("hide");
  })

  
})