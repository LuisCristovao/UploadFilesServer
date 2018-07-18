%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<html>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<style>
#items{
  list-style:none;
  margin:0px;
  margin-top:4px;
  padding-left:10px;
  padding-right:10px;
  padding-bottom:5px;
  font-size:17px;
  color: #333333;
  
}
hr { width: 85%; 
  background-color:#E4E4E4;
  border-color:#E4E4E4;
    color:#E4E4E4;
}
#cntnr{
  display:none;
  position:absolute;
  border:1px solid #B2B2B2;
  width:150px;      
  background:#F9F9F9;
  
  border-radius:4px;
}

li{
  
  padding: 3px;
  padding-left:10px;
}
li:hover{
	background:#284570;
	color:rgb(255,255,255);
}

</style>
</head>
<h1>{{User}} Uploaded Files: </h1>
<form action="/upload" method="post" enctype="multipart/form-data">
  Select a file: <input type="file" name="upload" />
  <input type="submit" value="Start upload" />
</form>
<text style="cursor:pointer; color:blue; text-decoration:underline" onclick="logout(this)">Log Out</text>		

<table border="1">
%for row in rows:
  %filename=row.split('        ')[0];unicode=row.split('        ')[1]
   
  <tr     >
    
    <td  title="right-click for more option" onmouseover="on(this,'{{filename}}')" onmouseout="off(this)">{{filename}}</td>
    %if unicode!='{{NotShared}}':
        <td title="right-click for more option" onmouseover="on(this,'{{unicode}}')" onmouseout="off(this)">localhost:2000/{{unicode}}</td>  
    %end
  </tr>
%end
</table>
<div id='cntnr'>
    <ul id='items'>
      <li>Download</li>
      <li>Copy Link</li>
      <li>Delete</li>  
      <hr />  
      <li>Share File</li>
      <li>Don't Share File</li>    
    </ul> 
</div>
<p id="download_text" style="visibility:hidden;"><font color="red">Click on row to download File</font></p>	
<script>
var TableBackgroundNormalColor = "#ffffff";
var TableBackgroundMouseoverColor = "#9999ff";
function on(row,row_str){
	row.style.backgroundColor = TableBackgroundMouseoverColor;
    onobject=row_str;
	//document.getElementById("download_text").style.visibility="visible";
}
function off(row){
	row.style.backgroundColor = TableBackgroundNormalColor;
    onobject="";
	//document.getElementById("download_text").style.visibility="hidden";
}
function download(file){
window.location=file;

}
function httpGetAsync(theUrl, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText,theUrl.split('/')[1]);
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous 
    xmlHttp.send(null);
} 
    
function Delete(file){
window.location="delete/"+file;

}
function Share(file){
    window.location="share/"+file;
    
}   
function StopSharing(file){
    window.location="stopshare/"+file;
}    
function logout(text){
	//document.cookie="{{User}}=;expires=Thu, 01 Jan 1970 00:00:01 GMT;path=/;";
    DeleteAllCookies();
	window.location="/";
}
 function DeleteAllCookies()
{
			Cookie=document.cookie;
            console.log(Cookie.localeCompare('')!=-1);
			//if  not empty
			if(Cookie.localeCompare('')!=-1){
				cookies=Cookie.split(';');
                console.log(cookies);
				var cookies_names=[];
				cookies.forEach(function(cookie){cookies_names.push(cookie.split('=')[0]);}); 
				//deleting cookies
                console.log(cookies_names);
				cookies_names.forEach(function(name){document.cookie=name + '=;expires=Thu, 01 Jan 1970 00:00:01 GMT;path=/;';});
				//cookies_names.forEach(function(name){$.cookie(name, null, { path: '/' });});
			}
}
    
//right click menu
var onobject;
var selected;    
$(document).bind("contextmenu",function(e){
  selected=onobject;    
  e.preventDefault();
  console.log(e.pageX + "," + e.pageY);
  $("#cntnr").css("left",e.pageX);
  $("#cntnr").css("top",e.pageY);
 // $("#cntnr").hide(100);        
  $("#cntnr").fadeIn(200,startFocusOut());      
});

function startFocusOut(){
  $(document).on("click",function(){
  $("#cntnr").hide();        
  $(document).off("click");
  });
}

$("#items > li").click(function(){
    if($(this).text().localeCompare('Download')==0){
        download(selected);
    }
    if($(this).text().localeCompare('Delete')==0){
        var r = confirm("Are you sure you want to Delete?");
        if (r == true) {
            Delete(selected);
        } else {
            //nothing...
        }
    }
    if($(this).text().localeCompare('Share File')==0){
        Share(selected);
    }
    if($(this).text().localeCompare("Don't Share File")==0){
        StopSharing(selected);
    }
    if($(this).text().localeCompare("Copy Link")==0){
        //StopSharing(selected);
        console.log(selected);
        copyToClipboard(window.location.host+'/'+selected);
    }
    //onobject=null;
    selected=null;
});

    
const copyToClipboard = str => {
  const el = document.createElement('textarea');
  el.value = str;
  el.setAttribute('readonly', '');
  el.style.position = 'absolute';
  el.style.left = '-9999px';
  document.body.appendChild(el);
  el.select();
  document.execCommand('copy');
  document.body.removeChild(el);
};
    
</script>
</html>