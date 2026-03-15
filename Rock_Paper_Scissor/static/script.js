function play(choice){

fetch("/play", {

method: "POST",
headers: {
"Content-Type": "application/json"
},

body: JSON.stringify({
choice: choice
})

})

.then(response => response.json())

.then(data => {

document.getElementById("userChoice").innerText =
"Your Choice: " + data.user;

document.getElementById("computerChoice").innerText =
"Computer Choice: " + data.computer;

document.getElementById("gameResult").innerText =
data.result;

});

}

function resetGame(){

document.getElementById("userChoice").innerText = "";
document.getElementById("computerChoice").innerText = "";
document.getElementById("gameResult").innerText = "";

}