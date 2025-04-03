import sys
import sqlite3
import tkinter as tk
from tkinter import messagebox


class ClinicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("سیستم مدیریت مطب")
        self.root.geometry("400x350")

        self.init_db()
        self.create_widgets()
        self.load_appointments()

    def init_db(self):
        self.conn = sqlite3.connect("clinic.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                patient_name TEXT,
                                doctor_name TEXT,
                                date TEXT,
                                time TEXT)''')
        self.conn.commit()

    def create_widgets(self):
        tk.Label(self.root, text="نام بیمار:").pack()
        self.txt_patient = tk.Entry(self.root)
        self.txt_patient.pack()

        tk.Label(self.root, text="نام پزشک:").pack()
        self.txt_doctor = tk.Entry(self.root)
        self.txt_doctor.pack()

        tk.Label(self.root, text="تاریخ:").pack()
        self.txt_date = tk.Entry(self.root)
        self.txt_date.pack()

        tk.Label(self.root, text="ساعت:").pack()
        self.txt_time = tk.Entry(self.root)
        self.txt_time.pack()

        self.btn_add = tk.Button(self.root, text="افزودن نوبت", command=self.add_appointment)
        self.btn_add.pack()

        self.list_appointments = tk.Listbox(self.root, width=50)
        self.list_appointments.pack()

    def load_appointments(self):
        self.list_appointments.delete(0, tk.END)
        self.cursor.execute("SELECT patient_name, doctor_name, date, time FROM appointments")
        for row in self.cursor.fetchall():
            self.list_appointments.insert(tk.END, f"{row[0]} - {row[1]} - {row[2]} {row[3]}")

    def add_appointment(self):
        patient = self.txt_patient.get()
        doctor = self.txt_doctor.get()
        date = self.txt_date.get()
        time = self.txt_time.get()
        if patient and doctor:
            self.cursor.execute("INSERT INTO appointments (patient_name, doctor_name, date, time) VALUES (?, ?, ?, ?)",
                                (patient, doctor, date, time))
            self.conn.commit()
            self.load_appointments()
            messagebox.showinfo("موفقیت", "نوبت با موفقیت اضافه شد!")
        else:
            messagebox.showwarning("خطا", "لطفا نام بیمار و پزشک را وارد کنید.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ClinicApp(root)
    root.mainloop()
