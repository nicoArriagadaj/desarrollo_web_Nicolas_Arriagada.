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

document.addEventListener("DOMContentLoaded", function () {
    // objeto region :comunas 
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
  
    selectRegion.addEventListener("change", function () {
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
  });


