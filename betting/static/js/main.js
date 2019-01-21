const date = new Date();
document.querySelector('.year').innerHTML = date.getFullYear();

setTimeout(function() {
     $('#message').fadeOut('slow');
}, 3000);

window.onload=function() { 
     document.getElementById("over_under").onchange=function() {
               // Get all options within <select id='foo'>...</select>
          if (document.getElementById("over_under").value == 'na'){
               document.getElementById("number_goals").disabled=true;
               document.getElementById("goals").disabled=true; 
               document.getElementById("number_goals").value=this.options[this.selectedIndex].getAttribute("data-sync");
          }
          else {
               document.getElementById("number_goals").disabled=false;
               document.getElementById("goals").disabled=false;  
          }
     }

     document.getElementById("home").onchange=function() {
          if (document.getElementById("home").value =='none'){
               document.getElementById('btts_home').style.display ='none';
               document.getElementById('btts_home_f').style.display ='none';
          } else {
               document.getElementById('btts_home').style.display ='block';
               document.getElementById('btts_home_f').style.display ='block';
          }
          
     }

     document.getElementById("away").onchange=function() {
          if (document.getElementById("away").value =='none'){
               document.getElementById('btts_away').style.display ='none';
               document.getElementById('btts_away_f').style.display ='none';
          } else {
               document.getElementById('btts_away').style.display ='block';
               document.getElementById('btts_away_f').style.display ='block';
          }
          
     }

     document.getElementById("home").onchange();
     document.getElementById("away").onchange();
     document.getElementById("over_under").onchange(); // trigger when loading
}

