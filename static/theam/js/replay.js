/**
 * Created by amr on 27/06/17.
 */
$(document).ready(function () {
      $(".comment-reply-btn").click(function (event) {
          event.preventDefault();
          $(this).parent().next(".comment-reply").fadeToggle();
      });
      // $("#following").hover(function(){
      //
      //       // $(".unfollow").show();
      //   },
      //   function(){
      //     $(this).show();
      //       // $(".unfollow").hide();
      //   });

});



$(document).ready(function() {
	$('#tallModal').modal('show');
});


// script for like button 

// $('.likebutton').click(function(){ 
// var id; 
// id = $(this).attr("data-catid"); 
// $.ajax( 
// { 
// type:"GET", 
// url: "Answer/answer_id/likes/", 
// data:{ 
// 	 answer_id: id 
// }, 
// success: function( data ) 
// { 
// $( '#like'+ id ).removeClass('btn btn-primary btn-lg'); 
// $( '#like'+ id ).addClass('btn btn-success btn-lg'); } }) });
    
// end script