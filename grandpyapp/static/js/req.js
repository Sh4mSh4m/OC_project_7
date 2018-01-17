////////////////////////////////////////////////////////////////
// DOM selecotrs declaration                                  //
////////////////////////////////////////////////////////////////
var form = document.querySelector("form");
var dialogInput = document.getElementById("dialogInput");
var dialogDisplay = document.getElementById("dialogDisplay");

////////////////////////////////////////////////////////////////
// Post function sending user input and recovering server     //
// Calling back function to handle response                   //
////////////////////////////////////////////////////////////////
function dialogSend(data){
    var data = {
        dialogContent : data
    }
    ajaxPost("http://localhost:5000/dialog", data, function (text) {
      var listData= JSON.parse(text)

//      if (text === "tg") {
//        botMsg = displayLogMessage("bot", "toi ftg vp");
//        dialogDisplay.insertAdjacentElement("afterbegin", botMsg);
//      }
//      if (true) {
//        botMsg = displayLogMessage("bot", "je dis ce que je veux"+text);
//        dialogDisplay.insertAdjacentElement("afterbegin", botMsg);
//      }
      msg = listData.interaction
      msg += listData.response
      msg += listData.complement
      console.log(msg)
      botMsg = displayLogMessage("bot", msg);
      dialogDisplay.insertAdjacentElement("afterbegin", botMsg);
      //              var listeData = JSON.parse(text);
//        listeData.forEach( function(data) {
//            var lienElt = creerElementLien(data);
//            contenuElt.appendChild(lienElt);
// if JSON.error not empty
// if JSON.reponse not empty
// if JSON.nose not empty
// if JSON.confirm not empty
//     replace inputarea
// if JSON.resultat not empty
    }, true);
};

////////////////////////////////////////////////////////////////
// Functions that creates HTML elements to display in the log //
////////////////////////////////////////////////////////////////
function createTimeStampElt () {
    var date = new Date ()
    var hour = date.getHours()
    var min = date.getMinutes()
    var spanElt = document.createElement("span")
    spanElt.setAttribute("class", "time");
    spanElt.textContent = hour + ":" + min
    return spanElt
};

function createParagraphElt (text) {
    var paragrapheElt = document.createElement("p");
    paragrapheElt.setAttribute("class", "wordwrap");
    paragrapheElt.textContent = text;
    return paragrapheElt
};

function createAvatarElt (source) {
    var avatarElt = document.createElement("div");
    avatarElt.setAttribute("class", "avatar");
    avatarElt.setAttribute("id", source);
    return avatarElt
};

function createDivElt (source) {
    var divElt = document.createElement("div");
    divElt.setAttribute("class", source);
    return divElt
};

function displayLogMessage (source, text) {
    var msgElt = createDivElt(source);
    var msgAvatarElt = createAvatarElt(source)
    var msgInputElt = createParagraphElt(text)
    var msgInputTimeElt = createTimeStampElt()
    msgElt.appendChild(msgAvatarElt);
    msgElt.appendChild(msgInputElt);
    msgInputElt.appendChild(msgInputTimeElt)
    return msgElt;
};

function checkInput (data) {
    if (typeof data === 'string') {
        return true;
    }
    else {
        return false;
    }
};

function sendUsrInput (data) {
    dialogInput.value = null;
    userMsg = displayLogMessage("user", data);
    dialogDisplay.insertAdjacentElement("afterbegin", userMsg);
    dialogSend(data);
}

////////////////////////////////////////////////////////////////
// Event listeners to submit user input upon clicking submit  //
// button                                                     //
////////////////////////////////////////////////////////////////
form.addEventListener("submit", function (e) {
    e.preventDefault();
    data = dialogInput.value;
    if (checkInput(data)) {
        sendUsrInput(data);
    }
    else {
        botMsg = displayLogMessage("bot", "HHooouuu eeee, wrong input mate");
        dialogDisplay.insertAdjacentElement("afterbegin", botMsg);
    }
});

dialogInput.addEventListener('keypress', function(e) {
    if (e.keyCode === 13) { 
        data = dialogInput.value;
        if (checkInput(data)) {
            sendUsrInput(data);
        }
        else {
            botMsg = displayLogMessage("bot", "HHooouuu eeee, wrong input mate");
            dialogDisplay.insertAdjacentElement("afterbegin", botMsg);
        }        e.preventDefault();
    }
});


// eventlistener for confirmation window