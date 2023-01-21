$(document).ready(function () {
    var socket = io.connect("http://localhost:5000")
    socket.on('connect', function() {
        socket.send("User connected");
    });

    socket.on('message', function(data) {
        $('#messages').append($('<p>').text(data));
    });

    $('#sendBtn').on('click', function() {
        socket.send($('#username').val() + ': ' + $('#message').val());
        $('#message').val('');
    });
})