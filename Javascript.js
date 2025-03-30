// VARIABLES Y VALIDADORES 

const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
let contadorFotos = 1;
const maxFotos = 5;


function agregarFoto() {
  if (contadorFotos >= maxFotos) {
    alert("Solo puedes subir hasta 5 fotos.");
    document.getElementById("agregarFoto").remove(); 
    return;
  }
  const contenedor = document.getElementById("zona-fotos");
  const nuevoInput = document.createElement("input");
  nuevoInput.type = "file";
  nuevoInput.name = "Foto";
  nuevoInput.className = "foto-input";
  nuevoInput.style.marginTop = "10px";

  contenedor.appendChild(nuevoInput);

  contadorFotos++;
}



// DOMContentLoaded: cuando cargue todo, aplicamos las funciones
document.addEventListener("DOMContentLoaded", () => {
  // Región y comuna
  const comunasPorRegion = {
    arica: ["Arica", "Camarones", "Putre", "General Lagos"],
    tarapaca: ["Iquique", "Alto Hospicio", "Pozo Almonte", "Pica"],
    antofagasta: ["Antofagasta", "Mejillones", "Calama", "Taltal"],
    atacama: ["Copiapó", "Caldera", "Vallenar", "Chañaral"],
    coquimbo: ["La Serena", "Coquimbo", "Ovalle", "Illapel"],
    valparaiso: ["Valparaíso", "Viña del Mar", "Quilpué", "San Antonio"],
    metropolitana: ["Santiago", "Puente Alto", "Maipú", "La Florida"],
    ohiggins: ["Rancagua", "San Fernando", "Rengo", "Santa Cruz"],
    maule: ["Talca", "Curicó", "Linares", "Cauquenes"],
    nuble: ["Chillán", "San Carlos", "Bulnes", "Quirihue"],
    biobio: ["Concepción", "Los Ángeles", "Talcahuano", "Coronel"],
    araucania: ["Temuco", "Angol", "Villarrica", "Padre Las Casas"],
    losrios: ["Valdivia", "La Unión", "Panguipulli", "Río Bueno"],
    loslagos: ["Puerto Montt", "Osorno", "Castro", "Ancud"],
    aysen: ["Coyhaique", "Aysén", "Chile Chico", "Cochrane"],
    magallanes: ["Punta Arenas", "Puerto Natales", "Porvenir", "Cabo de Hornos"]
  };

  const selectRegion = document.getElementById("regiones");
  const selectComuna = document.getElementById("comuna");

  selectRegion.addEventListener("change", () => {
    const regionSeleccionada = selectRegion.value;
    const comunas = comunasPorRegion[regionSeleccionada] || [];

    selectComuna.innerHTML = '<option value="selector" disabled selected>Seleccione una comuna</option>';
    comunas.forEach(comuna => {
      const option = document.createElement("option");
      option.value = comuna.toLowerCase().replace(/\s+/g, "_");
      option.textContent = comuna;
      selectComuna.appendChild(option);
    });
  });

  // Enlazar funciones a eventos
  document.getElementById("agregarFoto").addEventListener("click", agregarFoto);
  document.getElementById("validarCorreo").addEventListener("click", correoValido);
  document.getElementById("tema").addEventListener("change", otroTema);
  document.getElementById("AgregarActividad").addEventListener("click", MensajeRecibido);
});



function otroContacto() {
  const seleccion = document.getElementById("contactar").value;
  const contenedor = document.getElementById("input-otro-contacto");

  contenedor.innerHTML = "";
  if (seleccion === "otra") {
    const input = document.createElement("input");
    input.id="otroInput"
    input.type = "text";
    input.minLength = 4;
    input.maxLength = 50;
    input.placeholder = "Ingrese ID o URL";
    input.name = "otraRed";
    contenedor.appendChild(input);
  }
}



function otroTema() {
  const inputOtroTema = document.getElementById("input_otro_tema");
  const seleccionTema = document.getElementById("tema").value;

  inputOtroTema.innerHTML = "";

  if (seleccionTema === "otro") {
    const nuevo = document.createElement("input");
    nuevo.type = "text";
    nuevo.minLength = 3;
    nuevo.maxLength = 15;
    nuevo.placeholder = "Ingrese tema";
    nuevo.id = "otroTemaInput"; 
    inputOtroTema.appendChild(nuevo);
  }
}

// la funcion que valida todo
function MensajeRecibido() {
  const formulario = document.getElementById("form");
  const errorGeneral = document.getElementById("errorGeneral");

  if (!validaRegionComuna(errorGeneral)) {
    return;
  }
  if (!validaNombre(errorGeneral)){
    return;
  }
  if(!validaSector(errorGeneral)){
    return ;
  }

  if (!validaFotos(errorGeneral)) return;

  const correoOk = correoValido();
  if (!correoOk) return;
  const seleccionTema = document.getElementById("tema").value;
  if (!seleccionTema) {
    errorGeneral.textContent = "Debe seleccionar un tema.";
    return;
  }

  if (!validaOtroContacto(errorGeneral)) return;
  
  // valida que el otro tenga minimo 3 y maximo 15 caracteres
  if (seleccionTema === "otro") {
    const inputTema = document.getElementById("otroTemaInput");
    const valor = inputTema ? inputTema.value.trim() : "";
    if (valor.length < 3 || valor.length > 15) {
      errorGeneral.textContent = "El tema ingresado debe tener entre 3 y 15 caracteres.";
      return;
    }
  }
  

  if (!formulario.checkValidity()) {
    errorGeneral.textContent = "Por favor completa todos los campos obligatorios.";
    alert("Por favor completa todos los campos obligatorios.")
    return;
  } else {
    errorGeneral.textContent = "";
  }


  const numeroOk = NumeroValido();
  const fechasOk = verificaFecha();


  if (!correoOk || !numeroOk || !fechasOk) {
    return;
  }
/* borrar, ya que esto es con "alert"
  const confirmado = confirm("¿Está seguro que desea agregar esta actividad?");
  if (confirmado) {
    formulario.style.display = "none";
    const mensajeFinal = document.createElement("div");
    mensajeFinal.style.textAlign = "center";
    mensajeFinal.innerHTML = `<h2>Hemos recibido su información, muchas gracias y suerte en su actividad.</h2>`;
    document.body.appendChild(mensajeFinal);
  }
    */
   // ahora, con esto, se muestra 
  document.getElementById("confirmacion").style.display = "block";

}

















// VALIDADORES CON JAVASCRIPT


function validaNombre(errorGeneral) {
  const nombre = document.getElementById("name").value.trim();
  if (nombre.length === 0 || nombre.length > 200) {
    errorGeneral.textContent = "El nombre del organizador es obligatorio y debe tener hasta 200 caracteres.";
    return false;
  }
  return true;
}



function validaRegionComuna(errorGeneral) {
  const region = document.getElementById("regiones").value;
  const comuna = document.getElementById("comuna").value;

  if (!region || !comuna) {
    errorGeneral.textContent = "Debe seleccionar una región y una comuna.";
    return false;
  }
  return true;
}




function validaSector(errorGeneral) {
  const sector = document.getElementById("sector").value.trim();
  if (sector.length > 100) {
    errorGeneral.textContent = "El campo 'Sector' no puede tener más de 100 caracteres.";
    return false;
  }
  return true;
}


function correoValido() {
  const CorreoIngresado = document.getElementById("email").value.trim();
  const CorreoError = document.getElementById("errorEmail");

  if (CorreoIngresado.length === 0) {
    CorreoError.textContent = "El correo electrónico es obligatorio.";
    CorreoError.style.color = "red";
    return false;
  }

  if (CorreoIngresado.length > 100) {
    CorreoError.textContent = "El correo no debe superar los 100 caracteres.";
    CorreoError.style.color = "red";
    return false;
  }

  if (!regexEmail.test(CorreoIngresado)) {
    CorreoError.textContent = "ERROR: Correo electrónico no válido.";
    CorreoError.style.color = "red";
    return false;
  }

  CorreoError.textContent = "Correo válido.";
  CorreoError.style.color = "green";
  return true;
}


function NumeroValido() {
  const numero = document.getElementById("number").value;
  const errorSpan = document.getElementById("errorNumero");
  const formatoNumero = /^\+\d{3}\.\d{8}$/;

  if (numero === "") {
    errorSpan.textContent = "";
    return true;
  }

  if (!formatoNumero.test(numero)) {
    errorSpan.textContent = "Formato inválido. Un ejemplo es +569.12345678";
    return false;
  }

  errorSpan.textContent = "";
  return true;
}

// cuando alguien selecciona otro contacto, esto lo valida.
function validaOtroContacto(errorGeneral) {
  const seleccion = document.getElementById("contactar").value;

  if (seleccion === "otra") {
    const input = document.getElementById("otroInput");
    const valor = input ? input.value.trim() : "";

    if (valor.length < 4 || valor.length > 50) {
      errorGeneral.textContent = "Debe ingresar un ID o URL válido (entre 4 y 50 caracteres).";
      return false;
    }
  }

  return true;
}





function verificaFecha() {
  const inicio = document.getElementById("DiaHoraInicio").value;
  const termino = document.getElementById("DiaHoraTermino").value;
  const errorSpan = document.getElementById("errorFecha");

  if (!inicio) {
    errorSpan.textContent = "Debe ingresar una fecha de inicio.";
    return false;
  }

  if (termino && inicio >= termino) {
    errorSpan.textContent = "La fecha de término debe ser posterior a la de inicio.";
    return false;
  }

  errorSpan.textContent = "";
  return true;
}


function validaFotos(errorGeneral) {
  const fotos = document.querySelectorAll('.foto-input');
  let algunaSeleccionada = false;

  fotos.forEach(input => {
    if (input.files.length > 0) {
      algunaSeleccionada = true;
    }
  });

  if (!algunaSeleccionada) {
    errorGeneral.textContent = "Debe subir al menos una foto.";
    return false;
  }

  return true;
}



function enviarFormulario() {
  document.getElementById("form").style.display = "none";
  document.getElementById("confirmacion").style.display = "none";

  const mensajeFinal = document.createElement("div");
  mensajeFinal.style.textAlign = "center";
  mensajeFinal.innerHTML = `<h2>Hemos recibido su información, muchas gracias y suerte en su actividad.</h2>`;
  document.body.appendChild(mensajeFinal);
}

function cancelarEnvio() {
  document.getElementById("confirmacion").style.display = "none";
}
