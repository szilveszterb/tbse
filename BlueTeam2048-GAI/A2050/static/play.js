window.addEventListener("keydown",function(event){
  var key=event.keyCode;
  //if(key>=37 && key<=40)
    socket.emit("input",{key:event.keyCode});
});
