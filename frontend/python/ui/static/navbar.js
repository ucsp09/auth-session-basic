navbar = document.getElementById("navbar");
navbar.innerHTML = `
    <a href="/ui/home">Home</a>
    <a href="/ui/about">About</a>
    <button id="logoutButton">Logout</button>
`;
logoutButton = document.getElementById("logoutButton");
logoutButton.addEventListener("click", logoutButtonClickEventHandler);

async function logoutButtonClickEventHandler(event){
    event.preventDefault();
    const logoutSuccess = await logoutUser();
    if (logoutSuccess === true){
        alert("Logout Sucess.");
        window.location.replace("/");
    }else{
        alert("Logout failed.");
        window.location.replace(window.location.pathname);
    }
}

async function callBackendLogoutAPI(){
    const loginUrl = "http://localhost:8000/api/v1/logout";
    const response = await fetch(loginUrl, {
        method: "GET",
        credentials: "include"
    });
    return response;
}

async function logoutUser(){
    const response = await callBackendLogoutAPI();
    if (response.status === 200){
        return true;
    }else{
        return false;
    }
}