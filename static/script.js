function openPopup(){
    popupp.classList.remove("openpopup");
    popup.classList.toggle("openpopup");
}

function openPopupp(){
    popup.classList.remove("openpopup");
    popupp.classList.toggle("openpopup");
}

function btn(n){
    for(let i=1;i<11;i++){
        var col = document.getElementById("color"+i).style.borderColor;
        document.getElementById("color"+i).style.backgroundColor = col;
    }
    var col = document.getElementById("color"+n).style.backgroundColor;
    document.getElementById("username").value = n;
    document.getElementById("color"+n).style.color = col;
    document.getElementById("color"+n).style.backgroundColor = "#222";
}

function noChange(){
    document.getElementById("username").value = 0;
}

var colors = ['#222222','#b3595e','#83b2c9','#b3725f','#608aa0','#b58961','#5c589b','#609358','#8a5b9f','#69afa5','#9d526c'];

function whereBox(){
  if (msg.user_name == document.getElementById("username").value){
    box.classList.remove("boxright")
    box.classList.add("boxleft")
  } else {
    box.classList.remove("boxleft")
    box.classList.add("boxright")
  }
  document.getElementById("box").style.borderColor = colors[msg.user_name];
}

// var socket = io.connect('http://' + document.domain + ':' + location.port);

// socket.on( 'connect', function() {
//   socket.emit( 'my event', {
//     data: 'User Connected'
//   } )
//   var form = $( 'form' ).on( 'submit', function( e ) {
//     e.preventDefault()
//     let user_name = $( 'input.username' ).val()
//     let user_input = $( 'input.message' ).val()
//     socket.emit( 'my event', {
//       user_name : user_name,
//       message : user_input
//     } )
//     $( 'input.message' ).val( '' ).focus()
//   } )
// } )

// socket.on( 'my response', function( msg ) {
//   alert(msg.message);
//   console.log( msg );
//   if( typeof msg.user_name !== 'undefined' ) {
//     $( 'h3' ).remove()
//     if (msg.message=='Toxic') {
//       alert( "error" );
//     } else {
//       alert("pass");
//     }
//     $( 'div.right' ).append( '<div class="box" id="box">'+msg.message+'</div>' )
//   }
// })