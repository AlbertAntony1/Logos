let sendBtn = document.querySelector('.sendBtn');
let messageListUl = document.querySelector('ul');
let messageBox = document.querySelector('.messageBox');






async function sendMessageToServer() {
    let timeAndDate = new Date();
    let messageValue = messageBox.value;
    let messageId = Number(`${Date.now()}`);

    let messageSend = await fetch('/messageSend', {
        method: 'POST',
        headers: {'Content-type': 'application/json'},
        body: JSON.stringify({
            'message' : messageValue,
            'messageId' : messageId,
            'date' : timeAndDate
        })
    })
    messageBox.value = '';
    loadMessages();

}

async function loadMessages(){

    let Response = await fetch('/messageReceive', {
        method: 'POST',
        headers: {'Content-type': 'application/json'},
        body: JSON.stringify({})
    })

    let messageList = await Response.json();

    messageListUl.innerHTML =   '';
    messageList.forEach(message => {
        messageListUl.innerHTML =   `<li>
        <div>
                    <img src="${message.userProfilePicture}" alt="">
        </div>
        <div>
            <h4 class="headline">${message.userName}</h4>
            <h5>${message.userId}</h5>
            <p>${message.message}</p></div></li>
            ${messageListUl.innerHTML}
        `;
    });


    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth'});

    
}



loadMessages()
sendBtn.addEventListener('click', sendMessageToServer);
messageBox.addEventListener('keydown', (event)=>{if (event.key == 'Enter'){sendMessageToServer()}})
