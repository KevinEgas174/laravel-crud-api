import flet as ft
import requests

def main(page: ft.Page):
    page.title = "API CRUD Laravel y Flet"

    # Crear una tabla de usuarios con columnas y filas vacías inicialmente
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Primer Nombre")),
            ft.DataColumn(ft.Text("Segundo Nombre")),
            ft.DataColumn(ft.Text("Primer Apellido")),
            ft.DataColumn(ft.Text("Segundo Apellido")),
            ft.DataColumn(ft.Text("Cedula")),
            ft.DataColumn(ft.Text("Rango")),
            ft.DataColumn(ft.Text("Email")),
            ft.DataColumn(ft.Text("Celular")),
            ft.DataColumn(ft.Text("Ciudad")),
            ft.DataColumn(ft.Text("Acciones"))
        ],
        rows=[]
    )

    # Función para obtener usuarios desde la API
    def get_usuarios():
        url = "http://127.0.0.1:8000/api/usuarios"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    # Función para agregar un nuevo usuario
    def add_usuario(e):
        nuevo_usuario = {
            "Primer_Nombre": primer_nombre.value,
            "Segundo_Nombre": segundo_nombre.value,
            "Primer_Apellido": primer_apellido.value,
            "Segundo_Apellido": segundo_apellido.value,
            "Cedula": cedula.value,
            "Rango": rango.value,
            "Email": email.value,
            "Celular": celular.value,
            "Ciudad": ciudad.value
        }

        try:
            response = requests.post("http://127.0.0.1:8000/api/usuarios", json=nuevo_usuario)
            response.raise_for_status()
            page.snack_bar = ft.SnackBar(ft.Text("Usuario creado con éxito!"))
            page.snack_bar.open = True
            update_table()
            dialog.open = False
        except requests.exceptions.HTTPError as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al crear usuario: {response.text}"))
            page.snack_bar.open = True
        finally:
            page.update()

    # Función para eliminar un usuario
    def delete_usuario(usuario_id):
        try:
            response = requests.delete(f"http://127.0.0.1:8000/api/usuarios/{usuario_id}")
            response.raise_for_status()
            page.snack_bar = ft.SnackBar(ft.Text("Usuario eliminado con éxito!"))
            page.snack_bar.open = True
            update_table()
        except requests.exceptions.HTTPError as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar usuario: {response.text}"))
            page.snack_bar.open = True
        finally:
            page.update()

    # Función para actualizar un campo específico de un usuario
    def update_usuario_field(usuario_id, campo, valor):
        try:
            response = requests.patch(f"http://127.0.0.1:8000/api/usuarios/{usuario_id}", json={campo: valor})
            response.raise_for_status()
            page.snack_bar = ft.SnackBar(ft.Text("Campo actualizado con éxito!"))
            page.snack_bar.open = True
            update_table()
            dialog_open = False
        except requests.exceptions.HTTPError as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al actualizar campo: {response.text}"))
            page.snack_bar.open = True
        finally:
            page.update()

    # Función para refrescar la tabla de usuarios
    def update_table(e=None):
        table.rows.clear()
        try:
            usuarios_data = get_usuarios()
            if "usuarios" in usuarios_data:
                for usuario in usuarios_data["usuarios"]:
                    edit_button = ft.IconButton(ft.icons.EDIT, on_click=lambda e, u=usuario: show_update_form(u['id'], u))
                    delete_button = ft.IconButton(ft.icons.DELETE, on_click=lambda e, u=usuario: delete_usuario(u['id']))
                    table.rows.append(
                        ft.DataRow(
                            [
                                ft.DataCell(ft.Text(usuario["Primer_Nombre"])),
                                ft.DataCell(ft.Text(usuario["Segundo_Nombre"])),
                                ft.DataCell(ft.Text(usuario["Primer_Apellido"])),
                                ft.DataCell(ft.Text(usuario["Segundo_Apellido"])),
                                ft.DataCell(ft.Text(usuario["Cedula"])),
                                ft.DataCell(ft.Text(usuario["Rango"])),
                                ft.DataCell(ft.Text(usuario["Email"])),
                                ft.DataCell(ft.Text(usuario["Celular"])),
                                ft.DataCell(ft.Text(usuario["Ciudad"])),
                                ft.DataCell(ft.Row([edit_button, delete_button]))
                            ]
                        )
                    )
            else:
                print("No se encontraron usuarios en la respuesta.")
        except requests.exceptions.HTTPError as err:
            print(f"Error al obtener usuarios: {err}")

        page.update()

    # Mostrar formulario para agregar/actualizar usuario en una ventana emergente
    def show_update_form(usuario_id=None, usuario=None):
        if usuario:
            primer_nombre.value = usuario["Primer_Nombre"]
            segundo_nombre.value = usuario["Segundo_Nombre"]
            primer_apellido.value = usuario["Primer_Apellido"]
            segundo_apellido.value = usuario["Segundo_Apellido"]
            cedula.value = usuario["Cedula"]
            rango.value = usuario["Rango"]
            email.value = usuario["Email"]
            celular.value = usuario["Celular"]
            ciudad.value = usuario["Ciudad"]
            submit_button.text = "Actualizar Usuario"
            submit_button.on_click = lambda e: update_usuario_field(usuario_id, field_selector.value, field_value.value)
            # Mostrar campos de actualización solo para edición
            field_selector.visible = True
            field_value.visible = True
        else:
            primer_nombre.value = ""
            segundo_nombre.value = ""
            primer_apellido.value = ""
            segundo_apellido.value = ""
            cedula.value = ""
            rango.value = ""
            email.value = ""
            celular.value = ""
            ciudad.value = ""
            submit_button.text = "Crear Usuario"
            submit_button.on_click = add_usuario
            # Ocultar campos de actualización al agregar
            field_selector.visible = False
            field_value.visible = False

        dialog.open = True
        page.update()

    # Función para cerrar el formulario
    def close_dialog(e):
        dialog.open = False
        page.update()

    # Crear campos del formulario con un ancho más amplio y alineación ajustada
    primer_nombre = ft.TextField(label="Primer Nombre", width=400)
    segundo_nombre = ft.TextField(label="Segundo Nombre", width=400)
    primer_apellido = ft.TextField(label="Primer Apellido", width=400)
    segundo_apellido = ft.TextField(label="Segundo Apellido", width=400)
    cedula = ft.TextField(label="Cédula", width=400)
    rango = ft.Dropdown(
        label="Rango",
        options=[
            ft.dropdown.Option("Gerente"),
            ft.dropdown.Option("Empleado")
        ],
        width=400
    )
    email = ft.TextField(label="Email", width=400)
    celular = ft.TextField(label="Celular", width=400)
    ciudad = ft.TextField(label="Ciudad", width=400)

    field_selector = ft.Dropdown(
        label="Campo a Actualizar",
        options=[
            ft.dropdown.Option("Primer_Nombre"),
            ft.dropdown.Option("Segundo_Nombre"),
            ft.dropdown.Option("Primer_Apellido"),
            ft.dropdown.Option("Segundo_Apellido"),
            ft.dropdown.Option("Cedula"),
            ft.dropdown.Option("Rango"),
            ft.dropdown.Option("Email"),
            ft.dropdown.Option("Celular"),
            ft.dropdown.Option("Ciudad")
        ],
        width=400
    )

    field_value = ft.TextField(label="Nuevo Valor", width=400)
    submit_button = ft.ElevatedButton("Crear Usuario", on_click=add_usuario, width=400)

    # Botón de cierre (X)
    close_button = ft.IconButton(ft.icons.CLOSE, on_click=close_dialog)

    # Crear el diálogo para mostrar el formulario con botón de cerrar
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row([ft.Text("Formulario de Usuario", size=20, weight=ft.FontWeight.BOLD), close_button], alignment=ft.MainAxisAlignment.CENTER),
        content=ft.Column([
            primer_nombre, segundo_nombre, primer_apellido, segundo_apellido,
            cedula, rango, email, celular, ciudad,
            field_selector,
            field_value,
            submit_button
        ], scroll=ft.ScrollMode.AUTO, width=450, alignment=ft.MainAxisAlignment.START)  # Ancho ajustado del formulario
    )

    # Añadir el diálogo al overlay de la página
    page.overlay.append(dialog)

    # Botón para agregar un nuevo usuario
    add_button = ft.ElevatedButton("Agregar Usuario", on_click=lambda e: show_update_form())

    # Botón para cargar usuarios
    update_button = ft.ElevatedButton("Cargar Usuarios", on_click=update_table)

    # Contenedor principal con desplazamiento horizontal y vertical
    content = ft.Column(
        [
            ft.Text("Lista de Usuarios", size=24, weight=ft.FontWeight.BOLD),
            add_button,
            update_button,
            ft.Column([table], scroll=ft.ScrollMode.AUTO, expand=True)  # Ajuste para agregar barra de desplazamiento horizontal y vertical
        ],
        scroll=ft.ScrollMode.AUTO  # Permite el desplazamiento vertical en la página
    )

    # Agregar contenido a la página
    page.add(content)

    # Cargar usuarios al iniciar la página
    page.on_load = update_table

ft.app(target=main)
