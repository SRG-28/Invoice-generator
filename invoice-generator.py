import tkinter as tk
from tkinter import messagebox
import os

def obtener_siguiente_numero_factura():
    facturas = [f for f in os.listdir() if f.startswith("factura_")]
    
    if facturas:
        numeros_facturas = [int(f.split('_')[1].split('.')[0]) for f in facturas]
        return max(numeros_facturas) + 1
    else:
        return 1

def validar_login(entry_usuario, entry_contraseña, ventana_login):
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()

    usuarios = {}
    with open('usuarios.txt', 'r') as file:
        for line in file:
            user, passwd = line.strip().split(',')
            usuarios[user] = passwd  

    if usuario in usuarios and usuarios[usuario] == contraseña:
        messagebox.showinfo("Login exitoso", "¡Bienvenido!")
        ventana_login.destroy()
        ventana_facturacion()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

def calcular_vuelto(entry_monto, entry_dinero, label_vuelto):
    try:
        monto_pagar = float(entry_monto.get())
        dinero_dado = float(entry_dinero.get())
        
        if dinero_dado < monto_pagar:
            messagebox.showerror("Error", "El cliente no ha dado suficiente dinero.")
            label_vuelto.config(text="Vuelto: ---")  
            return None  
        else:
            vuelto = dinero_dado - monto_pagar
            label_vuelto.config(text=f"Vuelto: {vuelto:.2f}")  
            return vuelto
    except ValueError:
        messagebox.showerror("Error", "Valores inválidos. Ingrese solo números.")
        label_vuelto.config(text="Vuelto: ---")  
        return None

def generar_factura(entry_nombre, entry_productos, entry_monto, entry_dinero, label_vuelto):
    nombre = entry_nombre.get()
    productos = entry_productos.get()
    monto_pagar = entry_monto.get()
    dinero_dado = entry_dinero.get()

    vuelto = calcular_vuelto(entry_monto, entry_dinero, label_vuelto)
    
    if vuelto is None:
        return 

    if nombre and productos and monto_pagar and dinero_dado:
        numero_factura = obtener_siguiente_numero_factura()
        factura = (f"Factura #{numero_factura}\n"
                   f"Nombre: {nombre}\nProductos: {productos}\n"
                   f"Monto a Pagar: {monto_pagar}\nDinero Recibido: {dinero_dado}\n"
                   f"Vuelto: {vuelto:.2f}\n\n")

        with open(f"factura_{numero_factura}.txt", 'w') as file:
            file.write(factura)

        messagebox.showinfo("Factura generada", "La factura ha sido generada correctamente.")

        entry_nombre.delete(0, tk.END)
        entry_productos.delete(0, tk.END)
        entry_monto.delete(0, tk.END)
        entry_dinero.delete(0, tk.END)
        label_vuelto.config(text="Vuelto: ---")  

    else:
        messagebox.showerror("Error", "Por favor complete todos los campos.")

def ver_facturas():
    facturas = [f for f in os.listdir() if f.startswith("factura_")]

    if facturas:
        messagebox.showinfo("Facturas generadas", "\n".join(facturas))
    else:
        messagebox.showinfo("Facturas generadas", "No hay facturas generadas.")

def ver_factura_especifica(entry_factura):
    factura_a_ver = entry_factura.get()
    if os.path.exists(factura_a_ver):
        with open(factura_a_ver, 'r') as file:
            contenido = file.read()
            messagebox.showinfo("Factura", contenido)
    else:
        messagebox.showerror("Error", "Factura no encontrada.")

def ventana_facturacion():
    ventana = tk.Tk()
    ventana.title("Sistema de Facturación")
    ventana.geometry("450x500")
    ventana.config(bg="Light Blue")

    tk.Label(ventana, text="Nombre del Cliente", bg="Light Blue").pack()
    entry_nombre = tk.Entry(ventana)
    entry_nombre.pack()

    tk.Label(ventana, text="Productos", bg="Light Blue").pack()
    entry_productos = tk.Entry(ventana)
    entry_productos.pack()

    tk.Label(ventana, text="Monto a Pagar", bg="Light Blue").pack()
    entry_monto = tk.Entry(ventana)
    entry_monto.pack()

    tk.Label(ventana, text="Dinero Recibido", bg="Light Blue").pack()
    entry_dinero = tk.Entry(ventana)
    entry_dinero.pack()

    label_vuelto = tk.Label(ventana, text="Vuelto: ---", bg="Light Blue")
    label_vuelto.pack()

    tk.Button(ventana, text="Calcular Vuelto", command=lambda: calcular_vuelto(entry_monto, entry_dinero, label_vuelto)).pack()
    tk.Button(ventana, text="Generar Factura", command=lambda: generar_factura(entry_nombre, entry_productos, entry_monto, entry_dinero, label_vuelto)).pack()

    tk.Label(ventana, text="Ver Factura (Ingrese nombre del archivo)", bg="Light Blue").pack()
    entry_factura = tk.Entry(ventana)
    entry_factura.pack()

    tk.Button(ventana, text="Ver Facturas Generadas", command=ver_facturas).pack()
    tk.Button(ventana, text="Ver Factura Específica", command=lambda: ver_factura_especifica(entry_factura)).pack()

    ventana.mainloop()

ventana_login = tk.Tk()
ventana_login.title("Login")
ventana_login.geometry("450x500")
ventana_login.config(bg="Light Blue")

tk.Label(ventana_login, text="Usuario", bg="Light Blue").pack()
entry_usuario = tk.Entry(ventana_login)
entry_usuario.pack()

tk.Label(ventana_login, text="Contraseña", bg="Light Blue").pack()
entry_contraseña = tk.Entry(ventana_login, show="*")
entry_contraseña.pack()

tk.Button(ventana_login, text="Ingresar", command=lambda: validar_login(entry_usuario, entry_contraseña, ventana_login)).pack()

ventana_login.mainloop()
