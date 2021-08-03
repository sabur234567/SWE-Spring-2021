var form = document.getElementById('RegisterFleet')
form.addEventListener('submit',(e) => {e.preventDefault();})
function validateFleetRegistration() 
{
    var serviceName = document.forms["RegisterFleet"]["serviceName"].value;
    var Manufacturer = document.forms["RegisterFleet"]["Manufacturer"].value;
    var Model = document.forms["RegisterFleet"]["Model"].value;




    if (serviceName == "" || Manufacturer =="" || Model =="" )
    {
      alert("Please fill out the form completely.");
    }
    else
    {
      sendForm();
    }
    
}
function sendForm()
{
  //create form variable
  var form = document.getElementById('RegisterFleet');

  //capture form data
  var user = {};
  
  var i;
  for (i = 0; i <form.length; i++)
  {
    if (form.elements[i].name != ""){ 
      user[form.elements[i].name] =  form.elements[i].value;
    }
  }
  //POST the form data
  var formAction = 'https://demand.team11.sweispring21.tk/supply-front-end/RegisterFleet';
  var xmlreq = new XMLHttpRequest();
  xmlreq.open('POST', formAction, true );
  xmlreq.send(JSON.stringify(user));
}
  



