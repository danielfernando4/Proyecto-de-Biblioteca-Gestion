function sendUpdatedData() {
    const table = document.getElementById('data-table');
    const rows = table.querySelectorAll('tr');
    const updatedData = [];

    // Recopilar los datos de las celdas editables
    rows.forEach((row) => {
        const cells = row.querySelectorAll('td');
        if (cells.length === 2) {
            updatedData.push(cells[1].innerText.trim());
        }
    });

    // Enviar los datos actualizados al servidor mediante fetch con método PUT
    fetch('/actualizar', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ updatedData }),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log('Datos enviados:', data);
            alert('Datos actualizados correctamente.');
        })
        .catch((error) => {
            console.error('Error al enviar datos:', error);
        });
}

function sendSearchQuery() {
    const searchInput = document.getElementById('search-input').value.trim();

    // Enviar la búsqueda al servidor mediante fetch
    fetch('/buscar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: searchInput }),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log('Resultados de búsqueda:', data);
            // Aquí puedes manejar la respuesta del servidor
        })
        .catch((error) => {
            console.error('Error al realizar la búsqueda:', error);
        });
}
