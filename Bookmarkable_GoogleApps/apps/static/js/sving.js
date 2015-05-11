function uploads(update){
   $.ajax({
      url:"/saving",
      dataType: 'JSON',
      type: 'POST',
      data: { 
         category : document.getElementById("category").value,
         urls : document.getElementById("urls").value,
         subject : document.getElementById("subject").value,
         explain : document.getElementById("explain").value,
         comment : document.getElementById("comment").value,
         user_name : document.getElementById("user_name").value,
         tag1 : document.getElementById("tag1").value,
         tag2 : document.getElementById("tag2").value
     },
     success:function(data){
        string = "확인"+data.upload+" 저장완료!- 마이페이지에서 확인하세요!";
         alert(string);
         history.go(0); 
     }
 })
};

$('#saving_btn').bind('click',function(){
   var update = true;
   uploads(update);
});