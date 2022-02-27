
function showMore(){
    var moreContent = document.getElementById('more-content');
    var more = document.getElementById('more');
    var btnToggle = document.getElementById('btn-1');
    
    if (moreContent.style.display == "none"){
      moreContent.style.display = "inline";
      btnToggle.innerHTML = "Learn More";
      more.style.display = "none";
    }
    else{
      moreContent.style.display = "none";
      more.style.display = "block";
      btnToggle.innerHTML = "Show Less";
    }
  }

let btn = document.getElementById('btn-1');
btn.onclick = showMore;