loginButton = document.getElementById("loginButton");
loginButton.addEventListener("click", loginButtonClickEventHandler);

function loginButtonClickEventHandler(event){
    event.preventDefault();
    displayLoginForm();
}

function displayLoginForm(){
    loginForm = document.getElementById("loginForm");
    if(loginForm.style.display === "block"){
        loginForm.style.display = "none";
        return;
    }
    loginForm.style.display = "block";
    loginForm.innerHTML = `
    <form>
    <input type="text" id="username" placeholder="Username" required />
    <input type="password" id="password" placeholder="Password" required />
    <button type="submit" id="loginSubmitButton">Submit</button>
    </form>
    `;
    loginSubmitButton = document.getElementById("loginSubmitButton");
    loginSubmitButton.addEventListener("click", loginSubmitButtonClickEventHandler);
}

async function loginSubmitButtonClickEventHandler(event){
    event.preventDefault();
    console.log("Login submit button is clicked");
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const loginSuccess = await loginUser(username, password);
    if (loginSuccess === true){
        alert("Login Sucess.");
        window.location.replace("/ui/home");
    }else{
        alert("Login failed. Please check your username and password.");
    }
}

async function callBackendLoginAPI(username, password){
    const loginUrl = "http://localhost:8000/api/v1/login";
    const response = await fetch(loginUrl, {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    });
    return response;
}

async function loginUser(username, password){
    const response = await callBackendLoginAPI(username, password);
    if (response.status === 200){
        return true;
    }else{
        return false;
    }
}