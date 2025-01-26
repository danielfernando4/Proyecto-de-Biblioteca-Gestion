function sendSearchQuery() {
    const query = document.getElementById('search-input').value;
  
    // Enviar la búsqueda a la ruta "/actualizar" usando POST
    fetch('/actualizar', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
      console.log('Respuesta de Flask:', data);

      // Ahora actualizamos solo las celdas de la segunda columna
      const rows = data.rows;  // Extraemos las filas del JSON

      // Seleccionar todas las celdas de la segunda columna
      const cells = document.querySelectorAll('table tbody td:nth-child(2)');

      // Actualizar las celdas con los nuevos valores, solo las de la segunda columna
      for (let i = 0; i < rows.length; i++) {
          cells[i].textContent = rows[i];  // Actualizamos solo las celdas de la segunda columna
      }
    })
    .catch(error => {
      console.error('Error al enviar la búsqueda:', error);
    });
}