document.addEventListener("DOMContentLoaded", () => {
    const formulario = document.getElementById("formulario-cita");
    const mensaje = document.getElementById("mensaje");
  
    formulario.addEventListener("submit", function (e) {
      e.preventDefault();
  
      const medico = document.getElementById("medico").value;
      const paciente = document.getElementById("paciente").value;
      const fecha = document.getElementById("fecha").value;
      const hora = document.getElementById("hora").value;
      const consulta = document.getElementById("consulta").value;
  
      if (!medico || !paciente || !fecha || !hora || !consulta) {
        mostrarMensaje("Por favor complete todos los campos.", "#cf2537");
        return;
      }
  
      const hoy = new Date().toISOString().split("T")[0];
      if (fecha < hoy) {
        mostrarMensaje("La fecha no puede ser pasada.", "#cf2537");
        return;
      }
  
      if (hora < "08:00" || hora > "17:00") {
        mostrarMensaje("La hora debe estar entre 08:00 y 17:00.", "#cf2537");
        return;
      }
  
      mostrarMensaje("¡Cita guardada correctamente!", "#24d251");
      // formulario.reset(); // si deseas limpiar
    });
  
    function mostrarMensaje(texto, color) {
      mensaje.textContent = texto;
      mensaje.style.color = color;
    }
  });
  