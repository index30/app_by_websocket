var socket = new WebSocket('ws://' + location.host + '/websocket');

socket.onmessage = function (message) {
    result = document.getElementById('result');
    li = document.createElement('li');
    li.innerHTML = message.data;
    result.appendChild(li);
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
