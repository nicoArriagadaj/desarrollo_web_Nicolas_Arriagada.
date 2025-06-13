document.getElementById('formComentario').onsubmit = function(e) {
  e.preventDefault();

  const nombre = document.getElementById('nombre').value.trim();
  const comentario = document.getElementById('comentario').value.trim();
  const actividad_id = document.querySelector('input[name="actividad_id"]').value;

  fetch('/api/comentario', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ nombre, comentario, actividad_id })
  })
  .then(response => response.json())
  .then(result => {
    if (result.success) {
      document.getElementById('errores').innerHTML = '<span style="color:green">¡Su Comentario ha sido agregado!</span>';
      document.getElementById('formComentario').reset();
      cargarComentarios();
    } else {
      document.getElementById('errores').innerHTML = (result.errors || []).map(e => `<div style="color:red">${e}</div>`).join('');
    }
  })
  .catch(error => {
    document.getElementById('errores').innerHTML = `<div style="color:red">Error de red: ${error}</div>`;
  });
};

function cargarComentarios() {
  const actividad_id = document.querySelector('input[name="actividad_id"]').value;
  fetch(`/api/comentarios/${actividad_id}`)
    .then(response => response.json())
    .then(data => {
      if (data.comentarios && data.comentarios.length > 0) {
        document.getElementById('comentarios').innerHTML =
          data.comentarios.map(c =>
            `<div style="border-bottom:1px solid #ccc;margin-bottom:8px;">
              <b>${c.nombre}</b> <i>${c.fecha}</i><br>
              ${c.texto}
            </div>`
          ).join('');
      } else {
        document.getElementById('comentarios').innerHTML = "<i>No hay comentarios aún.</i>";
      }
    })
    .catch(error => {
      document.getElementById('comentarios').innerHTML = `<div style="color:red">Error al cargar comentarios: ${error}</div>`;
    });
}

window.onload = cargarComentarios;