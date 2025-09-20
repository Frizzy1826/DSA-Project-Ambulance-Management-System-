import tkinter as tk
from tkinter import messagebox

# Queue for patients
patient_queue = []
patient_records = []

ambulances = [
    ["Ambulance1", 7, 60],
    ["Ambulance2", 3, 50],
    ["Ambulance3", 10, 70]
]

class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value
                return
        self.table[index].append([key, value])

    def search(self, key):
        index = self.hash_function(key)
        for pair in self.table[index]:
            if pair[0].lower() == key.lower():
                return pair[1]
        return None

hospital_db = HashTable()
hospital_db.insert("Andheri", "Cooper Hospital")
hospital_db.insert("Bandra", "Lilavati Hospital")
hospital_db.insert("Borivali", "Karuna Hospital")
hospital_db.insert("Dadar", "Hinduja Hospital")
hospital_db.insert("Goregaon", "SRV Hospital")
hospital_db.insert("Thane", "Jupiter Hospital")

def sort_ambulances():
    amb_list = ambulances[:]
    n = len(amb_list)
    for i in range(n):
        for j in range(0, n - i - 1):
            if amb_list[j][1] > amb_list[j + 1][1]:  # Compare distance
                amb_list[j], amb_list[j + 1] = amb_list[j + 1], amb_list[j]
    return amb_list

def add_request():
    name = entry_name.get()
    loc = entry_location.get()
    priority = entry_priority.get()
    if name and loc and priority:
        patient_queue.append((name, loc, priority))
        patient_records.append((name, loc, priority))
        messagebox.showinfo("Request Added", f"✅ Request added for {name} at {loc}")
        entry_name.delete(0, tk.END)
        entry_location.delete(0, tk.END)
        entry_priority.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please fill all fields!")

def assign_ambulance():
    if not patient_queue or not ambulances:
        messagebox.showerror("Error", "❌ No requests or ambulances available")
        return
    
    critical_request = None
    for req in patient_queue:
        if req[2].lower() == "critical":
            critical_request = req
            break

    if critical_request:
        patient_queue.remove(critical_request)
        patient, location, priority = critical_request
    else:
        patient, location, priority = patient_queue.pop(0)

    sorted_amb = sort_ambulances()
    amb = sorted_amb[0]
    ambulances.remove(amb)

    name, distance, speed = amb
    eta = round(distance / speed * 60, 2)
    hospital = hospital_db.search(location) or "Nearest Government Hospital"

    messagebox.showinfo("Ambulance Assigned",
                        f"🚑 {name} assigned to {patient}\n"
                        f"📍 Location: {location} ({priority})\n"
                        f"📏 Distance: {distance} km | ⚡ Speed: {speed} km/h\n"
                        f"⏳ ETA: {eta} mins\n"
                        f"🏥 Hospital: {hospital}")

def search_hospital():
    area = entry_search_hospital.get()
    if area:
        hospital = hospital_db.search(area)
        if hospital:
            messagebox.showinfo("Hospital Found", f"🏥 Nearest hospital in {area}:\n{hospital}")
        else:
            messagebox.showwarning("Not Found", "❌ No hospital found in this area.")
    else:
        messagebox.showwarning("Input Error", "Please enter an area to search!")

def search_patient():
    name = entry_search_patient.get()
    if name:
        found = [rec for rec in patient_records if rec[0].lower() == name.lower()]
        if found:
            info = "\n".join([f"Name: {r[0]}, Location: {r[1]}, Priority: {r[2]}" for r in found])
            messagebox.showinfo("Patient Found", f"🔎 Patient Records:\n{info}")
        else:
            messagebox.showwarning("Not Found", "❌ No patient found in records.")
    else:
        messagebox.showwarning("Input Error", "Please enter a patient name to search!")

root = tk.Tk()
root.title("Ambulance Management System")
root.geometry("420x550")

tk.Label(root, text="Patient Name:").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Location:").pack()
entry_location = tk.Entry(root)
entry_location.pack()

tk.Label(root, text="Priority (Critical/Normal):").pack()
entry_priority = tk.Entry(root)
entry_priority.pack()

tk.Button(root, text="Add Request", command=add_request).pack(pady=5)
tk.Button(root, text="Assign Ambulance", command=assign_ambulance).pack(pady=5)

# Hospital Search
tk.Label(root, text="\n🔎 Search Hospital by Area:").pack()
entry_search_hospital = tk.Entry(root)
entry_search_hospital.pack()
tk.Button(root, text="Search Hospital", command=search_hospital).pack(pady=5)

tk.Label(root, text="\n🔎 Search Patient by Name:").pack()
entry_search_patient = tk.Entry(root)
entry_search_patient.pack()
tk.Button(root, text="Search Patient", command=search_patient).pack(pady=5)

root.mainloop()
