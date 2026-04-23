let googleLoginBtn = document.querySelector('#GoogleLoginBtn');
let OTPSendBtn = document.querySelector('#OTPSendBtn');
let OTPLoginBtn = document.querySelector('#OTPLoginBtn');
let LoginOptionsSection = document.querySelector('.LoginOptions');
let OTPVerificationsSection = document.querySelector('.OTPVerification');



async function googleLogin(){
    let googleLoginFetch = await fetch('/login/google');
    let googleLoginRequestURL = await googleLoginFetch.json();
    location.href = googleLoginRequestURL['data'];
}

async function googleLoginCallback(){
    let googleLoginFetchData = await fetch('/callback');
    let googleLoginData = await googleLoginFetchData.json();
    
}
async function OTPSend(){
    LoginOptionsSection.style.display = 'none';
    OTPVerificationsSection.style.display = 'flex';
    let email = document.querySelector('#EmailInput').value;
    let OTPSendRequest = await fetch('/login/otp', {
        method: 'POST',
        headers: {'Content-type': 'application/json'},
        body: JSON.stringify({'data': email})
    })

    let OTPVerification = await OTPSendRequest.json();
    alert(OTPVerification['data']);
    
}

async function OTPLogin(){
    let name = document.querySelector('#NameInput').value;
    let otp = document.querySelector('#OTPInput').value;
    let OTPLoginRequest = await fetch('/login/otp/validate', {
        method: 'POST',
        headers: {'Content-type': 'application/json'},
        body: JSON.stringify({'otp': otp, 'name': name})
    })

    let OTPValidate = await OTPLoginRequest.json();
    if (OTPValidate['data'] == true){
        location.href ='/chat';
    }else{
        alert('Try Again')
    }
    
}

googleLoginBtn.addEventListener('click', googleLogin);
OTPSendBtn.addEventListener('click', OTPSend)
OTPLoginBtn.addEventListener('click', OTPLogin)
