import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import random
import smtplib
from email.mime.text import MIMEText
import subprocess  # To call external scripts

# Database setup
conn = sqlite3.connect('user_data.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              username TEXT NOT NULL,
              email TEXT NOT NULL,
              name TEXT NOT NULL,
              phone TEXT NOT NULL,
              password TEXT NOT NULL)''')
conn.commit()

# OTP storage
generated_otp = None
user_email = None
otp_verified = False  # Flag to track OTP verification

# Function to send OTP
def send_otp(email):
    global generated_otp
    global user_email
    generated_otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
    user_email = email  # Store email for use in OTP verification
    try:
        sender_email = "whymeha.12@gmail.com"  # Your email
        sender_password = "your_password"  # Your app password
        subject = "Your OTP Code"
        body = f"Your OTP code is {generated_otp}"

        # Create MIMEText object
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = email

        # Connect to Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()

        messagebox.showinfo("Success", f"OTP sent to {email}")
    except Exception as e:              
        messagebox.showerror("Error", f"Failed to send OTP: {str(e)}")

# Function to toggle password visibility
def toggle_password_visibility(entry_widget, show_password_var):
    if show_password_var.get():
        entry_widget.config(show="")
    else:
        entry_widget.config(show="*")

# Function to open the login page
def open_login_page():
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("400x300")
    login_window.configure(bg="sky blue")

    # Username Entry
    label_username = tk.Label(login_window, text="Username", font=("Helvetica", 12), bg="sky blue")
    label_username.place(x=100, y=100)
    entry_username = tk.Entry(login_window)
    entry_username.place(x=180, y=100, width=160)

    # Password Entry
    label_password = tk.Label(login_window, text="Password", font=("Helvetica", 12), bg="sky blue")
    label_password.place(x=100, y=140)
    entry_password = tk.Entry(login_window, show="*")
    entry_password.place(x=180, y=140, width=160)

    # Show Password Checkbox
    show_password_var = tk.BooleanVar()
    check_show_password = tk.Checkbutton(login_window, text="Show Password", variable=show_password_var, bg="sky blue",
                                         command=lambda: toggle_password_visibility(entry_password, show_password_var))
    check_show_password.place(x=180, y=170)

    # Login Button
    login_button = tk.Button(login_window, text="Login", font=("Helvetica", 12, "bold"),
                             command=lambda: handle_login(entry_username.get(), entry_password.get()))
    login_button.place(x=160, y=200)

# Function to open the signup page
def open_signup_page():
    signup_window = tk.Toplevel(root)
    signup_window.title("Signup")
    signup_window.geometry("700x500")
    signup_window.configure(bg="sky blue")

    # Widgets for Signup
    label_username = tk.Label(signup_window, text="Username", font=("Helvetica", 12), bg="sky blue")
    label_username.place(x=50, y=100)
    entry_username_signup = tk.Entry(signup_window)
    entry_username_signup.place(x=150, y=100, width=160)

    label_email = tk.Label(signup_window, text="Email", font=("Helvetica", 12), bg="sky blue")
    label_email.place(x=50, y=130)
    entry_email_signup = tk.Entry(signup_window)
    entry_email_signup.place(x=150, y=130, width=160)

    label_name = tk.Label(signup_window, text="Name", font=("Helvetica", 12), bg="sky blue")
    label_name.place(x=50, y=160)
    entry_name_signup = tk.Entry(signup_window)
    entry_name_signup.place(x=150, y=160, width=160)

    label_phone = tk.Label(signup_window, text="Phone", font=("Helvetica", 12), bg="sky blue")
    label_phone.place(x=50, y=190)
    entry_phone_signup = tk.Entry(signup_window)
    entry_phone_signup.place(x=150, y=190, width=160)

    label_password = tk.Label(signup_window, text="Password", font=("Helvetica", 12), bg="sky blue")
    label_password.place(x=50, y=220)
    entry_password_signup = tk.Entry(signup_window, show="*")
    entry_password_signup.place(x=150, y=220, width=160)

    label_confirm_password = tk.Label(signup_window, text="Confirm Pass", font=("Helvetica", 12), bg="sky blue")
    label_confirm_password.place(x=50, y=270)
    entry_confirm_password_signup = tk.Entry(signup_window, show="*")
    entry_confirm_password_signup.place(x=150, y=270, width=160)

    # Show Password Checkbutton
    show_password_var = tk.BooleanVar()
    check_show_password = tk.Checkbutton(signup_window, text="Show Password", variable=show_password_var, bg="sky blue",
                                         command=lambda: toggle_password_visibility(entry_password_signup, show_password_var))
    check_show_password.place(x=320, y=218)

    # Show Confirm Password Checkbutton
    show_confirm_password_var = tk.BooleanVar()
    check_show_confirm_password = tk.Checkbutton(signup_window, text="Show Confirm Password", variable=show_confirm_password_var, bg="sky blue",
                                                 command=lambda: toggle_password_visibility(entry_confirm_password_signup, show_confirm_password_var))
    check_show_confirm_password.place(x=320, y=268)

    # Signup button
    signup_button = tk.Button(signup_window, text="Signup", font=("Helvetica", 12, "bold"),
                              command=lambda: handle_signup(entry_username_signup, entry_email_signup, 
                                                            entry_name_signup, entry_phone_signup, 
                                                            entry_password_signup, entry_confirm_password_signup))
    signup_button.place(x=150, y=350)

# Function to handle signup
def handle_signup(username_entry, email_entry, name_entry, phone_entry, password_entry, confirm_password_entry):
    username = username_entry.get()
    email = email_entry.get()
    name = name_entry.get()
    phone = phone_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    if username and email and name and phone and password:
        if password == confirm_password:
            # Insert user data
            c.execute("INSERT INTO users (username, email, name, phone, password) VALUES (?, ?, ?, ?, ?)", 
                      (username, email, name, phone, password))
            conn.commit()
            messagebox.showinfo("Success", "Signup Successful! Please verify the OTP sent to your email.")
            send_otp(email)  # Send OTP to the user's email for verification
            show_otp_window()  # Show OTP entry window
        else:
            messagebox.showerror("Error", "Passwords do not match")
    else:
        messagebox.showerror("Error", "Please fill all fields")

# Function to show OTP window
def show_otp_window():
    otp_window = tk.Toplevel(root)
    otp_window.title("Enter OTP")
    otp_window.geometry("300x200")
    otp_window.configure(bg="sky blue")

    label_otp = tk.Label(otp_window, text="Enter OTP", font=("Helvetica", 12), bg="sky blue")
    label_otp.pack(pady=10)
    entry_otp = tk.Entry(otp_window)
    entry_otp.pack(pady=5)

    submit_button = tk.Button(otp_window, text="Submit", font=("Helvetica", 12, "bold"),
                              command=lambda: validate_otp(entry_otp.get(), otp_window))
    submit_button.pack(pady=10)

# Function to validate OTP after signup or login
def validate_otp(entered_otp, otp_window):
    global otp_verified
    if entered_otp == generated_otp:
        otp_verified = True
        messagebox.showinfo("Success", "OTP Verified! You can now access the billing system.")
        otp_window.destroy()
        if otp_verified:  # Ensure OTP was verified
            open_billing_system()  # Open the billing system
    else:
        messagebox.showerror("Error", "Invalid OTP")

# Function to open the billing system
def open_billing_system():
    # Call the billing system script (you can change the command according to your setup)
    subprocess.Popen(["python", "Billing_system.py"])

# Function to handle login
def handle_login(username, password):
    global user_email
    # Retrieve user info from database
    c.execute("SELECT email, password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    if result:
        user_email, db_password = result
        if password == db_password:
            send_otp(user_email)  # Send OTP to the email
            show_otp_window()  # Show OTP entry window
        else:
            messagebox.showerror("Error", "Incorrect Password")
    else:
        messagebox.showerror("Error", "Username not found")

# Main GUI Setup (First Page with Login and Signup buttons)
root = tk.Tk()
root.title("Welcome Page")
root.geometry("600x400")
root.configure(bg="sky blue")  # Set background color to sky blue

# Title for First Page
label_title = tk.Label(root, text="Welcome To Dipak Store", font=("Helvetica", 24, "bold"), bg="sky blue")
label_title.place(x=150, y=50)

# Login Button
login_button = tk.Button(root, text="Login", font=("Helvetica", 12, "bold"),
                         command=open_login_page)
login_button.place(x=250, y=220)

# Signup Button
signup_button = tk.Button(root, text="Signup", font=("Helvetica", 12, "bold"),
                          command=open_signup_page)
signup_button.place(x=250, y=280)

# Load and Display Image on Right Side
try:
    img = Image.open("C:/Users/ACER/OneDrive/Desktop/abc/image.png")  # Use full path to the image
    img = img.resize((800, 800))  # Resize image to fit on the screen
    img = ImageTk.PhotoImage(img)

    image_label = tk.Label(root, image=img, bg="sky blue")
    image_label.image = img  # Keep a reference to the image
    image_label.place(x=550, y=100)  # Place image on the right side of the window
except Exception as e:
    messagebox.showerror("Error", f"Failed to load image: {str(e)}")

root.mainloop()

# Close the database connection when the application exits
conn.close()
