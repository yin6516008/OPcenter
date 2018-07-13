$(function () {
    // -------------主机列表选择按钮---------
    // 页面初始化选择按钮和移除按钮默认处于禁止点击状态
    $('.choose').attr('disabled', true);
    $('.remove').attr('disabled', true);

    $("#chooseAll").click(function () {
        var th_ckd = $(this).prop("checked");
        if (th_ckd) {
            $('.choose').attr('disabled', false);
        } else {
            $('.choose').attr('disabled', true);
        }
        $("#chooseTbody").find(":checkbox").prop("checked",th_ckd);
    });

    $("#chooseTbody").find(":checkbox").click(function () {
        $('.choose').attr('disabled', false);
        var length1=$("#chooseTbody").find(":checkbox").length;
        var length2=$("#chooseTbody").find(":checked").length;
        if(length1==length2){
            $("#chooseAll").prop("checked",true);
        }else{
            $("#chooseAll").prop("checked",false);
        }
    });

    var tbody_checkbox = $('#chooseTbody').find(':checkbox').length;
    console.log(tbody_checkbox);
})