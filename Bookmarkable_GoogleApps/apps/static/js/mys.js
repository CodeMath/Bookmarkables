function deletes(passwords, del_id){
    $.ajax({
        url:"/delete",
        dataType: 'JSON',
        type:'POST',
        data: {
           passwords : passwords,
           del_id : del_id
       },
       success:function(data){
        if( data.dels == "yes" ){
            alert("삭제 완료!");
            history.go(0);    
        }
        else{
            alert("비밀번호를 다시 확인해주세요!")
        }
    }
})
};

function comments(comment, re_ids){
    $.ajax({
        url:"/comment",
        dataType: 'JSON',
        type:'POST',
        data: {
            comment : comment,
            re_id : re_ids 
        },
        success:function(data){
            alert("코멘트 수정 완료!");
            history.go(0);
        }
    })
};

function pass_settings(check){
    $.ajax({
        url:"/pass_setting",
        dataType: 'JSON',
        type:'POST',
        data: {
            set_pass : document.getElementById("set_pass").value,
            set_id : document.getElementById("set_id").value
        },
        success:function(data){
            alert("수정 완료! - 잊어버리셨다면 다시 설정해주세요! :) ");
            history.go(0);
        }
    })
};

function nic_set(update){
    $.ajax({
        url:"/nic_set",
        dataType:'JSON',
        type:'POST',
        data:{
            set_nic : document.getElementById("set_nic").value,
            set_id : document.getElementById("set_ids").value
        },
        success:function(data){
            alert("수정완료되었습니다.");
            history.go(0);
        }
    })
};

$('.fix_btn').on('click',function(){
    var $parent_fix = $(this).parent();
    var comment = $parent_fix.find('.commented').val();
    var re_ids = $parent_fix.find('.ids').val();
    comments(comment, re_ids);
});

$('#pass_btn').on('click',function(){
    var checke = true;
    pass_settings(checke);
});

$('.del_btn').on('click',function(){
    var $parent_del = $(this).parent();
    var del_id = $parent_del.find('.dels_id').val();
    var passwords = $parent_del.find('.pass_words').val();
    deletes(passwords, del_id);
});

$('#nic_btn').on('click',function(){
    var update = true;
    nic_set(update);
});