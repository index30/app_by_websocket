var socket = new WebSocket('ws://' + location.host + '/websocket');

socket.onmessage = function (message) {
    result = document.getElementById('result');
    li = document.createElement('li');
    var data = JSON.parse(message.data);
    return_mes(data.response);
    li.innerHTML = data.kakasi_mes;
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

function return_mes (message){
    bot_result = document.getElementById('botmes');
    bot_result.innerHTML = message;
}
