
function show_nav(){
	let nav_option=document.getElementById('side_option');
	let elms=document.querySelectorAll("[id='side_option']");
	if(elms[0].style.width=="0px"){	
		for(let i=0; i<elms.length;i++){
			elms[i].style.width="100%";
			elms[i].style.marginLeft="10px";	
			elms[i].style.padding="0px 30px";	
		}
	}
	else{ 	
		for(let i=0; i<elms.length;i++){
			elms[i].style.width="0px";
			elms[i].style.marginLeft="0px";	
			elms[i].style.padding="0px 0px";	
		}


	}


}