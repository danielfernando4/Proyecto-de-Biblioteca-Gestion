function eliminarLibro(id) {
    if (confirm("¿Estás seguro de eliminar este libro?")) {
        fetch(`/eliminar_libro/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Libro eliminado');
                location.reload(); // Recargar la página para reflejar el cambio
            } else {
                alert('Error al eliminar el libro');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Hubo un problema con la solicitud');
        });
    }
}