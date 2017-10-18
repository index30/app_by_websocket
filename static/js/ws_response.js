var socket = new WebSocket('ws://' + location.host + '/websocket');

socket.onmessage = function (message) {
    result = document.getElementById('result');
    li = document.createElement('li');
    return_mes(message.data);
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

function return_mes (message){
    var template = "なんでも";
    if(~message.indexOf(template)){
        bot_result = document.getElementById('botmes');
        bot_result.innerHTML = "そういうのはなしです";
    }else{
        bot_result = document.getElementById('botmes');
        bot_result.innerHTML = "いいですね!!おいしそう...";
    }
}
