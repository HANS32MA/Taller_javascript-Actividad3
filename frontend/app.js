function consulta_general() {
  const url = "http://127.0.0.1:5000/";

  fetch(url)
    .then(response => response.json())
    .then(data => visualizar(data))
    .catch(error => console.error("Error fetching data:", error));

  const visualizar = (data) => {
    console.log("Fetched data:", data);

    let b = "";
    for (let i = 0; i < data.baul.length; i++) {
      console.log(i, data.baul[i].Plataforma);
      console.log(i, data.baul[i].usuario);
      console.log(i, data.baul[i].clave);

      b += `<tr>
        <td>${data.baul[i].id_baul}</td>
        <td>${data.baul[i].Plataforma}</td>
        <td>${data.baul[i].usuario}</td>
        <td>${data.baul[i].clave}</td>
        <td><button type="button" class="btn btn-info" onclick="location.href = 'edit.html?variable1=${data.baul[i].id_baul}'"><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTCdKFuUTRiYFn_8XLn0FR_jht8CHzSXr5U_w&s" height="30" width="30"></button>
        <button type="button" class="btn btn-warning" onclick="eliminar(${data.baul[i].id_baul})"><img src="https://w7.pngwing.com/pngs/999/436/png-transparent-delete-icon.png" height="30" width="30"></button></td>
      </tr>`;
    }

    document.getElementById('data').innerHTML = b;
  };
}

function eliminar(id) {
  const url = "http://127.0.0.1:5000/eliminar/" + id;

  fetch(url, {
    method: 'DELETE',
  })
    .then(response => response.json())
    .then(res => visualizar(res))
    .catch(error => console.error("Error deleting:", error));

  const visualizar = (res) => {
    swal("Mensaje", "Registro " + res.mensaje + " exitosamente", "success")
      .then(() => {
        swal(window.location.reload());
      });
  };
}

function registrar() {
  const url = "http://127.0.0.1:5000/registro/";
  const plat = document.getElementById("plataforma").value;
  const usua = document.getElementById("usuario").value;
  const clav = document.getElementById("clave").value;

  const data = {
    "plataforma": plat,
    "usuario": usua,
    "clave": clav
  };

  console.log("Data to send:", data);

  fetch(url, {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then(res => res.json())
    .catch(error => console.error("Error registering:", error))
    .then(response => visualizar(response));

  const visualizar = (response) => {
    console.log("Registration response:", response);

    if (response.mensaje === "Error") {
      swal("Mensaje", "Error en el registro", "error");
    } else {
      swal("Mensaje", "Registro agregado exitosamente", "success");
    }
  };
}

function consulta_individual(id) {
  const url = `http://127.0.0.1:5000/consulta_individual/${id}`;

  fetch(url)
    .then(response => response.json())
    .then(data => visualizar(data))
    .catch(error => console.error("Error fetching individual data:", error));

  const visualizar = (data) => {
    console.log("Fetched individual data:", data);

    document.getElementById("plataforma").value = data.baul.Plataforma;
    document.getElementById("usuario").value = data.baul.usuario;
    document.getElementById("clave").value = data.baul.clave;
  };
}

function modificar(id) {
  const url = `http://127.0.0.1:5000/actualizar/${id}`;
  const plat = document.getElementById("plataforma").value;
  const usua = document.getElementById("usuario").value;
  const clav = document.getElementById("clave").value;

  const data = {
    "plataforma": plat,
    "usuario": usua,
    "clave": clav
  };

  console.log("Data to update:", data);

  fetch(url, {
    method: "PUT",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then(res => res.json())
    .catch(error => console.error("Error updating:", error))
    .then(response => visualizar(response));

  const visualizar = (response) => {
    console.log("Update response:", response);

    if (response.mensaje === "Error") {
      swal("Mensaje", "Error en el registro", "error");
    } else {
      swal("Mensaje", "Registro actualizado exitosamente", "success");
    }
  };
}