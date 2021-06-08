//luisteren naar button
document.getElementById("summarize").addEventListener("click", function(){

    // kader met loading scherm tonen
    document.getElementById("sumDiv").style.display = "block";
    document.getElementById("loaderDiv").style.display = "block";
    document.getElementById("headingField").textContent="";
    document.getElementById("summarizationField").textContent="";
    document.getElementById("validation").textContent="";

    // post request maken en opgehaalde article link megeven 
    var articleLink = document.getElementById("link").value;
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            //loader niet meer tonen en summary binnenhalen
            document.getElementById("loaderDiv").style.display = "none";
            var response = JSON.parse(this.responseText)
            document.getElementById("link").value="";
            if(response['status'] == true){
                //wanneer successvol de summary nonen
                console.log(response["message"]);
                document.getElementById("headingField").textContent=response["heading"];
                document.getElementById("summarizationField").textContent=response["summary"];
            } else {
                //wanneer niet succesvol dit laten weten
                console.log(response["message"]);
                document.getElementById("sumDiv").style.display = "none";
                document.getElementById("validation").textContent=response["message"];
            }
            
        }
    };

    //post request doen
    xmlhttp.open("POST", "/getSummary", true);
    xmlhttp.send(articleLink);
});


