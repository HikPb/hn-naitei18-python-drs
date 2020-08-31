// if ($(window).width() > 992) {
    $(window).scroll(function(){  
       if ($(this).scrollTop() > 0) {
          $('#navbar_top').addClass("fixed-top");
          // add padding top to show content behind navbar
          $('body').css('padding-top', $('.navbar').outerHeight() + 'px');
          $('#sidebar-container').css('position','sticky');
          $('#sidebar-container').css('top',$('.navbar').outerHeight() + 'px');
        }else{
          $('#navbar_top').removeClass("fixed-top");
           // remove padding top from body
          $('body').css('padding-top', '0');        }   
    });
// }

setTimeout(function(){
  if($('#msg').length >0) {
    $('#msg').remove()
  }
}, 2000)
