
var form = document.querySelector("form");
var dialogInput = document.getElementById("dialogInput");
var dialogDisplay = document.getElementById("log");

function dialSend(data){
    console.log("envoi en cours");
    console.log(data);
    var data = {
        dialContent: data
    }
    console.log(JSON.stringify(data));
    ajaxPost("http://localhost/dialog", data, display(), true);

}

function createEltDisplay (text) {
    var inputElt = document.createElement("p");
    inputElt.textContent = text;
    return inputElt;
}

function display() {
    //takes the response and appends it in the dialogDisplay
    paragraphe = createEltDisplay("It's britney bitch");
    dialogDisplay.appendChild(paragraphe);
}


form.addEventListener("submit", function (e) {
    e.preventDefault();
    data = dialogInput.value;
    dialogInput.value = null;
    dialSend(data);
});

dialogInput.addEventListener('keypress', function(e) {
    if (e.keyCode === 13) { 
        e.preventDefault();
        console.log("enter")
        data = dialogInput.value;
        dialogInput.value = null;
        dialSend(data);
    }
});
