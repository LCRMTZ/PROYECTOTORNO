function guardarMensaje(mensaje_usuario, mensaje_bot) {
    fetch('http://127.0.0.1:5000/guardar-mensaje', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            mensaje_usuario: mensaje_usuario,
            respuesta_chatbot: mensaje_bot
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Conversación guardada:', data);
    })
    .catch(error => {
        console.error('Error al guardar conversación:', error);
    });
}


function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();

    if (message === "") return;

    addMessage(message, 'user');
    userInput.value = "";

  // Intención: Agendar cita
  if (message.toLowerCase().includes("agendar cita")) {
    const fechaMatch = message.match(/\d{4}-\d{2}-\d{2}/);
    const horaMatch = message.match(/\d{2}:\d{2}/);
    const nombreMatch = message.match(/para\s(.+)$/i);
    const correoMatch = message.match(/correo[:\s]+([^\s]+)/i);
    const motivoMatch = message.match(/motivo[:\s]+(.+)/i);

    if (fechaMatch && horaMatch && nombreMatch && correoMatch && motivoMatch) {
        const nombrePaciente = nombreMatch[1].trim();
        const correoPaciente = correoMatch[1].trim();
        const motivo = motivoMatch[1].trim();
        scheduleAppointment(fechaMatch[0], horaMatch[0], nombrePaciente, correoPaciente, motivo);
        return;
    } {
        addMessage("Por favor proporciona la fecha, hora, nombre del paciente, correo asociado y el motivo de la consulta. Ejemplo: Agendar cita 2025-05-01 10:00 para Juan Pérez correo juan@example.com motivo: Revisión de alergias", 'bot');
        return;
    }
}

// Intención: Editar cita
// Intención: Editar cita
if (message.toLowerCase().includes("editar cita")) {
    const id = message.match(/id\s?(\d+)/i);
    const fecha = message.match(/\d{4}-\d{2}-\d{2}/);
    const hora = message.match(/\d{2}:\d{2}/);
    const nombreMatch = message.match(/para\s(.+?)\s+motivo[:]/i);
    const motivoMatch = message.match(/motivo[:\s]+(.+?)\s+correo[:]/i);
    const correoMatch = message.match(/correo[:\s]+([^\s]+)/i);

    if (id && fecha && hora && nombreMatch && motivoMatch && correoMatch) {
        const appointmentId = parseInt(id[1]);
        const newDate = fecha[0];
        const newTime = hora[0];
        const nombrePaciente = nombreMatch[1].trim();
        const motivo = motivoMatch[1].trim();
        const correoPaciente = correoMatch[1].trim();

        editAppointment(appointmentId, newDate, newTime, nombrePaciente, correoPaciente, motivo);
        return;
    } else {
        addMessage("Por favor proporciona el ID, nueva fecha, hora, nombre, motivo y correo. Ejemplo: Editar cita id 14 2025-06-01 13:30 para Axel Yahir motivo: fiebre alta correo: axel@example.com", 'bot');
        return;
    }
}

// Intención: Cancelar cita
// Intención: Cancelar cita
if (message.toLowerCase().includes("cancelar cita")) {
    const id = message.match(/id\s?(\d+)/i);
    if (id) {
        cancelAppointment(parseInt(id[1]));
        return;
    }
}


    fetch('/preguntar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mensaje: message })
    })
    .then(response => response.json())
    .then(data => {
        const respuesta = data.respuesta;
        addMessage(respuesta, 'bot');
        guardarMensaje(message, respuesta);  // si estás guardando la conversación
    })
    .catch(error => {
        console.error('Error al comunicarse con el backend:', error);
        addMessage("Hubo un error al contactar al servidor.", 'bot');
    });

}


function closeChat() {
    window.location.href = "index.html"; // Cambia esto a la URL de tu página principal
}
// Función que devuelve respuestas del chatbot (simulación)
function getBotResponse(userMessage) {
    userMessage = userMessage.toLowerCase();

    if (userMessage.includes("hola")) {
        return "¡Hola! Soy Medibot, tu asistente virtual pediátrico. ¿En qué puedo ayudarte?";
    } else if (userMessage.includes("cita")) {
        return "Puedo ayudarte a agendar, modificar o cancelar una cita médica. ¿Qué deseas hacer?";
    } else if (userMessage.includes("gracias")) {
        return "¡De nada! Estoy aquí para ayudarte.";
    } else {
        return "Lo siento, no entiendo tu consulta. ¿Podrías reformularla?";
    }
}

// Función para mostrar la respuesta del bot
function botResponse(userInput) {
    let response = '';
    
    // Respuestas básicas de ejemplo
    if (userInput.toLowerCase().includes('agendar cita')) {
        response = '¿Cuándo te gustaría agendar la cita? Por favor, dime la fecha y hora.';
    } else if (userInput.toLowerCase().includes('editar cita')) {
        response = '¿Qué detalles te gustaría cambiar de tu cita?';
    } else if (userInput.toLowerCase().includes('cancelar cita')) {
        response = '¿Cuál es la cita que te gustaría cancelar? Por favor, proporciona los detalles.';
    } else if (userInput.toLowerCase().includes('hola')) {
        response = '¡Hola! ¿En qué puedo ayudarte hoy?';
    } else {
        response = 'Lo siento, no entendí tu mensaje. ¿Puedes reformularlo?';
    }

    addMessage(response, 'bot');
}

// Función para mostrar/ocultar el indicador de carga
function showLoading(isLoading) {
    const loading = document.getElementById('loading');
    loading.style.display = isLoading ? 'block' : 'none';
}

// Función para agendar una cita, conectándose al backend (ejemplo)
function scheduleAppointment(date, time, nombrePaciente, correoPaciente, motivo) {
    const appointmentData = {
        date: date,
        time: time,
        nombre_paciente: nombrePaciente,
        correo_paciente: correoPaciente,
        motivo: motivo,
        id_medico: 3
    };

    fetch('http://127.0.0.1:5000/agendar-cita', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(appointmentData),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            addMessage(`❌ No se pudo agendar: ${data.error}`, 'bot');
        } else {
            addMessage(`✅ Cita agendada para el ${data.date} a las ${data.time}. ID: ${data.id_cita}`, 'bot');
        }
    })
    .catch(error => {
        addMessage('❌ Error al conectar con el servidor.', 'bot');
        console.error('Error:', error);
    });
}



// Función para editar una cita, conectándose al backend (ejemplo)
function editAppointment(appointmentId, newDate, newTime, nombrePaciente, correoPaciente, motivo) {
    const updatedData = {
        appointmentId,
        newDate,
        newTime,
        newMotivo: motivo,
        nombre_paciente: nombrePaciente,
        correo_paciente: correoPaciente
    };

    fetch('http://127.0.0.1:5000/editar-cita', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedData),
    })
    .then(response => response.json())
    .then(data => {
        if (data.newDate && data.newTime) {
            addMessage(`✅ Tu cita ha sido actualizada para el ${data.newDate} a las ${data.newTime}.`, 'bot');
        } else if (data.error) {
            addMessage(`❌ Error: ${data.error}`, 'bot');
        } else {
            addMessage('❌ Hubo un error al actualizar tu cita.', 'bot');
        }
    })
    .catch(error => {
        addMessage('❌ Error al conectar con el servidor.', 'bot');
        console.error('Error:', error);
    });
}



// Función para cancelar una cita, conectándose al backend (ejemplo)
function cancelAppointment(appointmentId) {
    fetch(`http://127.0.0.1:5000/cancelar-cita/${appointmentId}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        addMessage('Tu cita ha sido cancelada exitosamente.', 'bot');
    })
    .catch(error => {
        addMessage('Hubo un error al cancelar tu cita. Intenta nuevamente.', 'bot');
        console.error('Error:', error);
    });
}
// Función para agregar mensajes al chat
/**function addMessage(message, sender) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);

    // Crear la burbuja de mensaje
    const bubbleDiv = document.createElement('div');
    bubbleDiv.classList.add('bubble');
    bubbleDiv.textContent = message;

    // Crear la imagen del avatar
    const avatarDiv = document.createElement('img');
    avatarDiv.classList.add('avatar');
    avatarDiv.src = sender === 'user' ? 'imagenes/icono usuario.jpg' : 'imagenes/icono chatbot.jpeg'; // Asegúrate de tener estas imágenes

    // Añadir la imagen y la burbuja al mensaje
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(bubbleDiv);
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Desplazar hacia abajo
}*/
// Función para mostrar la respuesta del bot

document.addEventListener("DOMContentLoaded", () => {
    showCurrentDate();

    // Escuchar clic en el botón Enviar
    document.getElementById("send-button").addEventListener("click", sendMessage);

    // Escuchar tecla Enter en el input
    document.getElementById("user-input").addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            sendMessage();
        }
    });
});


// Función para mostrar la fecha actual al inicio del chat
function showCurrentDate() {
    const chatBox = document.getElementById('chat-box');
    const dateDiv = document.createElement('div');
    dateDiv.classList.add('date');

    const now = new Date();
    const options = { 
        year: 'numeric', 
        month: '2-digit', 
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    };

    dateDiv.textContent = "Chat iniciado el " + now.toLocaleDateString('es-ES', options);
    chatBox.appendChild(dateDiv);
}

function getTimeAgo(time) {
    const now = new Date();
    const seconds = Math.floor((now - time) / 1000);

    if (seconds < 60) {
        return `hace ${seconds} segundo${seconds !== 1 ? 's' : ''}`;
    }

    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) {
        return `hace ${minutes} minuto${minutes !== 1 ? 's' : ''}`;
    }

    const hours = Math.floor(minutes / 60);
    if (hours < 24) {
        return `hace ${hours} hora${hours !== 1 ? 's' : ''}`;
    }

    const days = Math.floor(hours / 24);
    return `hace ${days} día${days !== 1 ? 's' : ''}`;
}


let lastBotMessageTime = null;

function addMessage(message, sender) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);

    // Crear la imagen del avatar
    const avatarDiv = document.createElement('img');
    avatarDiv.classList.add('avatar');
    avatarDiv.src = sender === 'user' ? USER_AVATAR : BOT_AVATAR;

    // Contenedor para la burbuja y el timestamp
    const contentDiv = document.createElement('div');
    contentDiv.classList.add('bubble-container');

    // Crear la burbuja de mensaje
    const bubbleDiv = document.createElement('div');
    bubbleDiv.classList.add('bubble');
    bubbleDiv.textContent = message;

    contentDiv.appendChild(bubbleDiv);

    // Agregar tiempo debajo de la burbuja si es del bot
    if (sender === 'bot') {
        const timeAgoSpan = document.createElement('span');
        timeAgoSpan.classList.add('time-ago');
        const timestamp = new Date();
        timeAgoSpan.setAttribute('data-timestamp', timestamp.getTime());
        timeAgoSpan.textContent = getTimeAgo(timestamp);
        contentDiv.appendChild(timeAgoSpan);

        // Actualizar el tiempo cada 10 segundos
        setInterval(() => {
            timeAgoSpan.textContent = getTimeAgo(new Date(parseInt(timeAgoSpan.getAttribute('data-timestamp'))));
        }, 10000);
    }

    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    chatBox.appendChild(messageDiv);

    // Desplazar hacia abajo después de agregar el mensaje
    setTimeout(() => {
        chatBox.scrollTop = chatBox.scrollHeight;
    }, 0);
}
