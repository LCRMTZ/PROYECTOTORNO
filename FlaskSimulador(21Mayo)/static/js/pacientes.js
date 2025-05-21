document.addEventListener("DOMContentLoaded", () => {
  const tabla = document.getElementById("tabla-pacientes");
  const buscador = document.getElementById("buscar");

  let pacientesData = [];

  function mostrarPacientes(lista) {
    tabla.innerHTML = "";

    lista.forEach((paciente, index) => {
      const fila = document.createElement("tr");

      const fechaHora = `${paciente.fecha_cita} ${paciente.hora_cita}`;

      fila.innerHTML = `
        <td>${paciente.nombre}</td>
        <td>${fechaHora}</td>
        <td>${paciente.nombre_medico}</td>
        <td>${paciente.motivo}</td>
        <td>
          <button class="editar" data-index="${index}">✏️</button>
          <button class="eliminar" data-index="${index}">❌</button>
        </td>
      `;

      tabla.appendChild(fila);
    });

    // Eventos de edición y eliminación (a futuro si los conectas con backend)
    document.querySelectorAll(".editar").forEach(boton => {
      boton.addEventListener("click", (e) => {
        const paciente = pacientesData[e.target.dataset.index];
        alert(`Editar paciente: ${paciente.nombre}`);
        // Aquí podrías abrir un modal con la info del paciente y actualizarla
      });
    });

    document.querySelectorAll(".eliminar").forEach(boton => {
      boton.addEventListener("click", (e) => {
        const paciente = pacientesData[e.target.dataset.index];
        const confirmar = confirm(`¿Eliminar cita de ${paciente.nombre}?`);
        if (confirmar) {
          // Aquí podrías hacer un fetch DELETE con paciente.id o similar
          alert("Función de eliminar aún no implementada.");
        }
      });
    });
  }

  function filtrarPacientes() {
    const texto = buscador.value.toLowerCase();
    const filtrados = pacientesData.filter(p =>
      p.nombre.toLowerCase().includes(texto)
    );
    mostrarPacientes(filtrados);
  }

  // Cargar desde el backend
  fetch("/api/pacientes")
    .then(response => response.json())
    .then(data => {
      pacientesData = data;
      mostrarPacientes(pacientesData);
    })
    .catch(error => {
      console.error("Error cargando pacientes:", error);
      tabla.innerHTML = `<tr><td colspan="5">❌ No se pudieron cargar los datos.</td></tr>`;
    });

  buscador.addEventListener("input", () => {
    filtrarPacientes();
  });
});
