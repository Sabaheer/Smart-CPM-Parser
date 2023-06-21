$(document).ready(function(){

    $("#re-parse").click(function(){
      $('#editor').find('p').remove();
      var divContent = $('#editor').text();
      $('#parse-request').html(divContent);
      $("#re-parse-form").submit();
      //#alert(divContent);
    });
  });
