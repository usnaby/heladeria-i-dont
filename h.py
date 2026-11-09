import sqlite3
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk


class HeladeriaApp:

  def __init__(self, root):
    self.root = root
    self.root.title("🍦 Heladería Dulce Frío - Control de Inventario y Ventas")
    self.root.geometry("1000x700")
    self.root.configure(bg="#fff4f7")

    self.rol_actual = None
    self.carrito = []

    self.init_db()
    self.insert_initial_data()
    self.create_login_screen()

  def init_db(self):
    self.conn = sqlite3.connect("heladeria.db")
    self.cursor = self.conn.cursor()

    # Tabla de productos
    self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL,
                precio REAL NOT NULL,
                cantidad INTEGER NOT NULL
            )
        """)

    # Tabla de ventas
    self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                total REAL NOT NULL
            )
        """)

    # Tabla de detalle de ventas
    self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS detalle_ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venta_id INTEGER,
                producto_nombre TEXT,
                cantidad INTEGER,
                precio_unitario REAL,
                subtotal REAL,
                FOREIGN KEY (venta_id) REFERENCES ventas (id)
            )
        """)
    self.conn.commit()

  def insert_initial_data(self):
    self.cursor.execute("SELECT COUNT(*) FROM productos")
    if self.cursor.fetchone()[0] == 0:
      productos_iniciales = [
          ("Helado de Vainilla", "Helados", 25.0, 50),
          ("Helado de Chocolate", "Helados", 28.0, 40),
          ("Paleta de Fresa", "Paletas", 15.0, 30),
          ("Paleta de Limón", "Paletas", 12.0, 45),
          ("Agua de Horchata", "Bebidas", 20.0, 25),
          ("Chispas de Chocolate", "Toppings", 5.0, 100),
      ]
      self.cursor.executemany(
          "INSERT INTO productos (nombre, categoria, precio, cantidad) VALUES"
          " (?, ?, ?, ?)",
          productos_iniciales,
      )
      self.conn.commit()

  def clear_window(self):
    for widget in self.root.winfo_children():
      widget.destroy()

  def create_login_screen(self):
    self.clear_window()

    frame = tk.Frame(
        self.root, bg="white", padx=30, pady=30, bd=1, relief="solid"
    )
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        frame,
        text="🍦 Heladería Dulce Frío",
        font=("Arial", 18, "bold"),
        bg="white",
        fg="#e85d8e",
    ).pack(pady=10)
    tk.Label(
        frame, text="Iniciar Sesión", font=("Arial", 14), bg="white"
    ).pack(pady=5)

    tk.Label(frame, text="Usuario:", bg="white", anchor="w").pack(
        fill="x", pady=(10, 0)
    )
    self.combo_user = ttk.Combobox(
        frame, values=["administrador", "vendedor"], state="readonly"
    )
    self.combo_user.set("administrador")
    self.combo_user.pack(fill="x", pady=5)

    tk.Label(frame, text="Contraseña:", bg="white", anchor="w").pack(
        fill="x", pady=(10, 0)
    )
    self.entry_pass = tk.Entry(frame, show="*")
    self.entry_pass.pack(fill="x", pady=5)

    tk.Button(
        frame,
        text="Entrar",
        bg="#e85d8e",
        fg="white",
        font=("Arial", 10, "bold"),
        command=self.login,
    ).pack(fill="x", pady=15)

    tk.Label(
        frame,
        text="Admin: Admin123 | Vendedor: Venta123",
        font=("Arial", 8),
        bg="white",
        fg="#777",
    ).pack()

  def login(self):
    usuario = self.combo_user.get()
    clave = self.entry_pass.get()

    credenciales = {"administrador": "Admin123", "vendedor": "Venta123"}

    if credenciales.get(usuario) == clave:
      self.rol_actual = usuario
      self.create_main_screen()
    else:
      messagebox.showerror("Error", "Usuario o contraseña incorrectos")

  def create_main_screen(self):
    self.clear_window()

    header = tk.Frame(self.root, bg="#e85d8e", pady=10)
    header.pack(fill="x")
    tk.Label(
        header,
        text=(
            "🍦 Heladería Dulce Frío — Sesión:"
            f" {self.rol_actual.capitalize()}"
        ),
        font=("Arial", 14, "bold"),
        bg="#e85d8e",
        fg="white",
    ).pack(side="left", padx=20)
    tk.Button(
        header,
        text="Cerrar Sesión",
        bg="#777",
        fg="white",
        command=self.create_login_screen,
    ).pack(side="right", padx=20)

    notebook = ttk.Notebook(self.root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    self.tab_inventario = tk.Frame(notebook, bg="#fff4f7")
    notebook.add(self.tab_inventario, text="📦 Inventario")

    self.tab_ventas = tk.Frame(notebook, bg="#fff4f7")
    notebook.add(self.tab_ventas, text="🛒 Punto de Venta / Ticket")

    self.tab_reportes = tk.Frame(notebook, bg="#fff4f7")
    notebook.add(self.tab_reportes, text="📊 Ventas del Día")

    self.setup_tab_inventario()
    self.setup_tab_ventas()
    self.setup_tab_reportes()

  def setup_tab_inventario(self):
    if self.rol_actual == "administrador":
      frame_form = tk.LabelFrame(
          self.tab_inventario,
          text="Gestión de Producto",
          bg="white",
          padx=10,
          pady=10,
      )
      frame_form.pack(fill="x", padx=10, pady=5)

      tk.Label(frame_form, text="Nombre:", bg="white").grid(
          row=0, column=0, sticky="w"
      )
      self.ent_nombre = tk.Entry(frame_form)
      self.ent_nombre.grid(row=0, column=1, padx=5, pady=5)

      tk.Label(frame_form, text="Categoría:", bg="white").grid(
          row=0, column=2, sticky="w"
      )
      self.cmb_cat = ttk.Combobox(
          frame_form,
          values=["Helados", "Paletas", "Bebidas", "Toppings", "Otros"],
          state="readonly",
      )
      self.cmb_cat.set("Helados")
      self.cmb_cat.grid(row=0, column=3, padx=5, pady=5)

      tk.Label(frame_form, text="Precio ($):", bg="white").grid(
          row=1, column=0, sticky="w"
      )
      self.ent_precio = tk.Entry(frame_form)
      self.ent_precio.grid(row=1, column=1, padx=5, pady=5)

      tk.Label(frame_form, text="Stock:", bg="white").grid(
          row=1, column=2, sticky="w"
      )
      self.ent_cantidad = tk.Entry(frame_form)
      self.ent_cantidad.grid(row=1, column=3, padx=5, pady=5)

      tk.Button(
          frame_form,
          text="➕ Agregar / Actualizar",
          bg="#e85d8e",
          fg="white",
          command=self.guardar_producto,
      ).grid(row=2, column=0, columnspan=2, pady=10, sticky="we")
      tk.Button(
          frame_form,
          text="🗑️ Eliminar Seleccionado",
          bg="#dc3545",
          fg="white",
          command=self.eliminar_producto,
      ).grid(row=2, column=2, columnspan=2, pady=10, sticky="we")

    frame_tabla = tk.Frame(self.tab_inventario, bg="white")
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)

    self.tree_inv = ttk.Treeview(
        frame_tabla,
        columns=("ID", "Nombre", "Categoría", "Precio", "Stock"),
        show="headings",
    )
    for col in ("ID", "Nombre", "Categoría", "Precio", "Stock"):
      self.tree_inv.heading(col, text=col)
      self.tree_inv.column(col, width=100)

    self.tree_inv.pack(fill="both", expand=True)
    self.tree_inv.bind("<<TreeviewSelect>>", self.seleccionar_producto_inv)

    self.cargar_inventario()

  def cargar_inventario(self):
    for item in self.tree_inv.get_children():
      self.tree_inv.delete(item)
    self.cursor.execute("SELECT * FROM productos")
    for row in self.cursor.fetchall():
      self.tree_inv.insert("", "end", values=row)

  def guardar_producto(self):
    nombre = self.ent_nombre.get().strip()
    cat = self.cmb_cat.get()
    try:
      precio = float(self.ent_precio.get())
      cant = int(self.ent_cantidad.get())
    except ValueError:
      messagebox.showerror(
          "Error", "Precio y stock deben ser numéricos válidos."
      )
      return

    if not nombre or precio <= 0 or cant < 0:
      messagebox.showerror("Error", "Ingresa datos válidos.")
      return

    self.cursor.execute("SELECT id FROM productos WHERE nombre = ?", (nombre,))
    existe = self.cursor.fetchone()

    if existe:
      self.cursor.execute(
          "UPDATE productos SET categoria=?, precio=?, cantidad=? WHERE id=?",
          (cat, precio, cant, existe[0]),
      )
      messagebox.showinfo(
          "Éxito", f"¡Alerta! Producto '{nombre}' modificado correctamente."
      )
    else:
      self.cursor.execute(
          "INSERT INTO productos (nombre, categoria, precio, cantidad) VALUES"
          " (?, ?, ?, ?)",
          (nombre, cat, precio, cant),
      )
      messagebox.showinfo(
          "Éxito", f"¡Alerta! Nuevo producto '{nombre}' agregado exitosamente."
      )

    self.conn.commit()
    self.cargar_inventario()
    self.cargar_productos_venta()

  def seleccionar_producto_inv(self, event):
    selected = self.tree_inv.selection()
    if selected and self.rol_actual == "administrador":
      item = self.tree_inv.item(selected[0])["values"]
      self.ent_nombre.delete(0, tk.END)
      self.ent_nombre.insert(0, item[1])
      self.cmb_cat.set(item[2])
      self.ent_precio.delete(0, tk.END)
      self.ent_precio.insert(0, item[3])
      self.ent_cantidad.delete(0, tk.END)
      self.ent_cantidad.insert(0, item[4])

  def eliminar_producto(self):
    selected = self.tree_inv.selection()
    if not selected:
      messagebox.showwarning(
          "Atención", "Selecciona un producto para eliminar."
      )
      return
    item = self.tree_inv.item(selected[0])["values"]
    if messagebox.askyesno(
        "Confirmar", f"¿Seguro que deseas eliminar '{item[1]}'?"
    ):
      self.cursor.execute("DELETE FROM productos WHERE id=?", (item[0],))
      self.conn.commit()
      self.cargar_inventario()
      self.cargar_productos_venta()
      messagebox.showinfo("Éxito", "Producto eliminado correctamente.")

  def setup_tab_ventas(self):
    frame_left = tk.Frame(self.tab_ventas, bg="white", padx=10, pady=10)
    frame_left.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    tk.Label(
        frame_left,
        text="Seleccionar Producto:",
        bg="white",
        font=("Arial", 10, "bold"),
    ).pack(anchor="w")
    self.cmb_prod_venta = ttk.Combobox(frame_left, state="readonly")
    self.cmb_prod_venta.pack(fill="x", pady=5)

    tk.Label(frame_left, text="Cantidad:", bg="white").pack(anchor="w")
    self.spn_cant_venta = tk.Spinbox(frame_left, from_=1, to=100)
    self.spn_cant_venta.pack(fill="x", pady=5)

    tk.Button(
        frame_left,
        text="🛒 Agregar al Carrito",
        bg="#3578c8",
        fg="white",
        command=self.agregar_carrito,
    ).pack(fill="x", pady=10)

    self.tree_cart = ttk.Treeview(
        frame_left,
        columns=("Producto", "Cant", "Precio U.", "Subtotal"),
        show="headings",
    )
    for col in ("Producto", "Cant", "Precio U.", "Subtotal"):
      self.tree_cart.heading(col, text=col)
      self.tree_cart.column(col, width=80)
    self.tree_cart.pack(fill="both", expand=True, pady=5)

    self.lbl_total = tk.Label(
        frame_left,
        text="Total: $0.00",
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#e85d8e",
    )
    self.lbl_total.pack(pady=5)

    tk.Button(
        frame_left,
        text="✅ Procesar Venta y Generar Ticket",
        bg="#176534",
        fg="white",
        font=("Arial", 10, "bold"),
        command=self.procesar_venta,
    ).pack(fill="x", pady=5)

    frame_right = tk.Frame(self.tab_ventas, bg="white", padx=10, pady=10)
    frame_right.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    tk.Label(
        frame_right,
        text="📄 Ticket de Compra",
        bg="white",
        font=("Arial", 12, "bold"),
    ).pack()
    self.txt_ticket = tk.Text(frame_right, width=40, font=("Courier", 9))
    self.txt_ticket.pack(fill="both", expand=True, pady=5)

    self.cargar_productos_venta()

  def cargar_productos_venta(self):
    self.cursor.execute(
        "SELECT id, nombre, precio, cantidad FROM productos WHERE cantidad > 0"
    )
    self.prods_dict = {
        f"{row[1]} (${row[2]}) - Stock: {row[3]}": row
        for row in self.cursor.fetchall()
    }
    self.cmb_prod_venta["values"] = list(self.prods_dict.keys())
    if self.prods_dict:
      self.cmb_prod_venta.current(0)

  def agregar_carrito(self):
    key = self.cmb_prod_venta.get()
    if not key or key not in self.prods_dict:
      return

    prod = self.prods_dict[key]
    cant = int(self.spn_cant_venta.get())

    if cant > prod[3]:
      messagebox.showerror(
          "Error", f"Stock insuficiente. Solo quedan {prod[3]} unidades."
      )
      return

    subtotal = prod[2] * cant
    self.carrito.append({
        "id": prod[0],
        "nombre": prod[1],
        "cantidad": cant,
        "precio": prod[2],
        "subtotal": subtotal,
    })

    self.tree_cart.insert(
        "",
        "end",
        values=(prod[1], cant, f"${prod[2]:.2f}", f"${subtotal:.2f}"),
    )
    self.actualizar_total_carrito()

  def actualizar_total_carrito(self):
    total = sum(item["subtotal"] for item in self.carrito)
    self.lbl_total.config(text=f"Total: ${total:.2f}")

  def procesar_venta(self):
    if not self.carrito:
      messagebox.showwarning("Atención", "El carrito está vacío.")
      return

    total = sum(item["subtotal"] for item in self.carrito)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    self.cursor.execute(
        "INSERT INTO ventas (fecha, total) VALUES (?, ?)", (fecha, total)
    )
    venta_id = self.cursor.lastrowid

    for item in self.carrito:
      self.cursor.execute(
          "INSERT INTO detalle_ventas (venta_id, producto_nombre, cantidad,"
          " precio_unitario, subtotal) VALUES (?, ?, ?, ?, ?)",
          (
              venta_id,
              item["nombre"],
              item["cantidad"],
              item["precio"],
              item["subtotal"],
          ),
      )
      self.cursor.execute(
          "UPDATE productos SET cantidad = cantidad - ? WHERE id = ?",
          (item["cantidad"], item["id"]),
      )

    self.conn.commit()
    self.generar_ticket(venta_id, fecha, total)

    self.carrito.clear()
    for i in self.tree_cart.get_children():
      self.tree_cart.delete(i)
    self.actualizar_total_carrito()
    self.cargar_inventario()
    self.cargar_productos_venta()
    messagebox.showinfo(
        "Venta Exitosa",
        "La venta ha sido registrada y el inventario actualizado"
        " automáticamente.",
    )

  def generar_ticket(self, venta_id, fecha, total):
    self.txt_ticket.delete("1.0", tk.END)
    ticket = "================================\n"
    ticket += "   🍦 HELADERÍA DULCE FRÍO 🍦   \n"
    ticket += "================================\n"
    ticket += f"Ticket ID: #{venta_id}\n"
    ticket += f"Fecha: {fecha}\n"
    ticket += f"Atendido por: {self.rol_actual.capitalize()}\n"
    ticket += "--------------------------------\n"
    ticket += f"{'Cant.  Producto':<20} {'Total':>10}\n"
    ticket += "--------------------------------\n"

    for item in self.carrito:
      nombre = item["nombre"][:14]
      ticket += (
          f"{item['cantidad']}x {nombre:<14} ${item['subtotal']:>8.2f}\n"
      )

    ticket += "--------------------------------\n"
    ticket += f"TOTAL: ${total:.2f} MXN\n"
    ticket += "================================\n"
    ticket += "   ¡Gracias por su compra! 🍦   \n"
    ticket += "================================\n"

    self.txt_ticket.insert(tk.END, ticket)

  def setup_tab_reportes(self):
    btn_refrescar = tk.Button(
        self.tab_reportes,
        text="🔄 Actualizar Reporte del Día",
        bg="#e85d8e",
        fg="white",
        command=self.cargar_reporte_dia,
    )
    btn_refrescar.pack(pady=10)

    self.lbl_resumen_ventas = tk.Label(
        self.tab_reportes, text="", font=("Arial", 11, "bold"), bg="#fff4f7"
    )
    self.lbl_resumen_ventas.pack(pady=5)

    self.tree_rep = ttk.Treeview(
        self.tab_reportes,
        columns=("ID Venta", "Fecha/Hora", "Total"),
        show="headings",
    )
    for col in ("ID Venta", "Fecha/Hora", "Total"):
      self.tree_rep.heading(col, text=col)
      self.tree_rep.column(col, width=150)
    self.tree_rep.pack(fill="both", expand=True, padx=10, pady=10)

    self.cargar_reporte_dia()

  def cargar_reporte_dia(self):
    for item in self.tree_rep.get_children():
      self.tree_rep.delete(item)

    hoy = datetime.now().strftime("%Y-%m-%d")
    self.cursor.execute(
        "SELECT id, fecha, total FROM ventas WHERE fecha LIKE ?", (f"{hoy}%",)
    )
    ventas_hoy = self.cursor.fetchall()

    total_dinero = 0
    for v in ventas_hoy:
      self.tree_rep.insert("", "end", values=(v[0], v[1], f"${v[2]:.2f}"))
      total_dinero += v[2]

    self.lbl_resumen_ventas.config(
        text=(
            f"Total Ventas Realizadas Hoy ({hoy}): {len(ventas_hoy)} | Ingresos"
            f" del Día: ${total_dinero:.2f} MXN"
        )
    )


if __name__ == "__main__":
  root = tk.Tk()
  app = HeladeriaApp(root)
  root.mainloop()