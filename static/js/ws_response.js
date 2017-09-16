var socket = new WebSocket('ws://' + location.host + '/websocket');

socket.onmessage = function (message) {
    //message = JSON.parse(message.data);
    result = document.getElementById('result');
    result.innerHTML = message.data;
}


function send_mes () {
    text_box = document.getElementById('text_box');
    former_text = text_box.value;
    message = JSON.stringify({
        text: former_text
    });
    socket.send(message);
    text_box.value = "";

}
