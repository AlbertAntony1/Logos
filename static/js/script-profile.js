let userProfilePicture = document.querySelector('.userProfilePicture');
let userName = document.querySelector('.userName');
let userId = document.querySelector('.userId');
let ImageSelector = document.querySelector('input')

async function userProfilePictureChange(e){
    const filesData = new FormData()
    filesData.append('file', e.target.files[0]);
    let userProfilePictureChangeFetch = await fetch('/userProfilePictureChange', {
        method: 'POST',
        body: filesData
    })
    userProfilePicture = e.target.files[0];
}
async function userNameChange(e){
    const NewUserName = e.target.value;
    let userNameChangeFetch = await fetch('/userNameChange', {
        method: 'POST',
        headers: {'Content-type': 'application/json'},
        body: JSON.stringify({'data': NewUserName})
    })
}

async function userIdChange(e){
    const NewUserId = e.target.value;
    let userIdChangeFetch = await fetch('/userIdChange', {
        method: 'POST',
        headers: {'Content-type': 'application/json'},
        body: JSON.stringify({'data': NewUserId})
    })
}



userProfilePicture.addEventListener('dblclick', ()=>{ImageSelector.click();});
ImageSelector.onchange = userProfilePictureChange;
userName.onchange = userNameChange;
userId.onchange = userIdChange;
