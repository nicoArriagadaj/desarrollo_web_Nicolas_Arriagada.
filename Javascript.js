// variables
const RegionSeleccionada = document.getElementById("region");
const ComunaSeleccionada = document.getElementById("comuna");

const NumeroIngresado = document.getElementById("")

const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;


// funcion verificadora de correo
const correoValido = () =>{
    const CorreoIngresado = document.getElementById("email").value;
    const CorreoError = document.getElementById("errorEmail");
    if(!regexEmail.test(CorreoIngresado)){
        CorreoError.textContent = "ERROR: Correo electrónico no válido.";
        CorreoError.style.color = "red";
        return false;
    }
    else {
        CorreoError.textContent = "Correo válido.";
        CorreoError.style.color = "green";
    }
};

const NumeroValido = (numero) =>{
    if (numero.find("+")){

    }
    
};
// aqui,debemos dar un mensaje, que diga si esta seguro o no de enviar el formulario
const MensajeRecibido = () =>{
    
}
