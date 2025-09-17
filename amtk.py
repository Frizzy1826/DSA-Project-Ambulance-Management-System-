import tkinter as tk
from tkinter import messagebox

patient_queue = []
patient_records = []
ambulances = [["Ambulance1", 7, 60], ["Ambulance2", 3, 50], ["Ambulance3", 10, 70]]

hospital_db = {
    "Andheri": "Cooper Hospital",
    "Bandra": "Lilavati Hospital",
    "Borivali": "Karuna Hospital",
    "Dadar": "Hinduja Hospital",
    "Goregaon": "SRV Hospital",
    "Thane": "Jupiter Hospital"
}

def add_request():
    name = entry_name.get()
    loc = entry_location.get()
    priority = entry_priority.get()
    if name and loc and priority:
        patient_queue.append((name, loc, priority))
        patient_records.append((name, loc, priority))
        messagebox.showinfo("Request Added", f" Request added for {name} at {loc}")
        entry_name.delete(0, tk.END)
        entry_location.delete(0, tk.END)
        entry_priority.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please fill all fields!")

def assign_ambulance():
    if not patient_queue or not ambulances:
        messagebox.showerror("Error", " No requests or ambulances available")
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

    ambulances.sort(key=lambda x: x[1])
    amb = ambulances.pop(0)

    name, distance, speed = amb
    eta = round(distance / speed * 60, 2)
    hospital = hospital_db.get(location, "Nearest Government Hospital")

    messagebox.showinfo("Ambulance Assigned",
                        f" {name} assigned to {patient}\n"
                        f" Location: {location} ({priority})\n"
                        f" Distance: {distance} km |  Speed: {speed} km/h\n"
                        f" ETA: {eta} mins\n"
                        f" Hospital: {hospital}")

def search_hospital():
    area = entry_search_hospital.get()
    if area:
        hospital = hospital_db.get(area)
        if hospital:
            messagebox.showinfo("Hospital Found", f" Nearest hospital in {area}:\n{hospital}")
        else:
            messagebox.showwarning("Not Found", " No hospital found in this area.")
    else:
        messagebox.showwarning("Input Error", "Please enter an area to search!")

def search_patient():
    name = entry_search_patient.get()
    if name:
        found = [rec for rec in patient_records if rec[0].lower() == name.lower()]
        if found:
            info = "\n".join([f"Name: {r[0]}, Location: {r[1]}, Priority: {r[2]}" for r in found])
            messagebox.showinfo("Patient Found", f" Patient Records:\n{info}")
        else:
            messagebox.showwarning("Not Found", " No patient found in records.")
    else:
        messagebox.showwarning("Input Error", "Please enter a patient name to search!")

root = tk.Tk()
root.title("Ambulance Management System")
root.geometry("420x500")

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

tk.Label(root, text="\n Search Hospital by Area:").pack()
entry_search_hospital = tk.Entry(root)
entry_search_hospital.pack()
tk.Button(root, text="Search Hospital", command=search_hospital).pack(pady=5)

tk.Label(root, text="\n Search Patient by Name:").pack()
entry_search_patient = tk.Entry(root)
entry_search_patient.pack()
tk.Button(root, text="Search Patient", command=search_patient).pack(pady=5)

root.mainloop()

