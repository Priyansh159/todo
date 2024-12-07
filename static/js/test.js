let value = document.querySelector(".check-js");
let stmnt = true;
value.addEventListener('click', ()=>{
if (stmnt===true){
    value.innerHTML = "<h4>Js is running !!<h4>";
    stmnt=false;
}
else{
    value.innerHTML = "<h4>Yes its Running perfectly !!<h4>";
    stmnt=true;
}
    
});