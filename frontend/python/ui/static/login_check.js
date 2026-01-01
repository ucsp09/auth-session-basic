run();

async function callBackendLoginStatusAPI(){
    const loginStatusUrl = "http://localhost:8000/api/v1/login/status";
    const response = await fetch(loginStatusUrl, {
        method: "GET",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        }
    });
    return response;
}

async function getLoginStatus(){
    const response = await callBackendLoginStatusAPI();
    if (response.status === 200){
        data = await response.json();
        session_id = data["session_id"];
        if (session_id !== null && session_id !== ""){
            return true;
        }else{
            return false;
        }
    }else{
        return false;
    }
}

async function run(){
    console.log("Getting login status");
    const loginStatus = await getLoginStatus();
    if (loginStatus === false){
        if(window.location.pathname !== "/"){
            console.log("Redirecting to login page");
            window.location.replace("/");
        }else{
            console.log("Already redirected to login page");
        }
    }else{
        console.log("Already Logged in");
        if(window.location.pathname === "/"){
            console.log("Redirecting to home page");
            window.location.replace("/ui/home");
        }else{
            console.log("Already redirected");
        }
    }
}