# 67011594 Chuthathip Termchaikul

class AppointmentScheduler:
    def __init__(self):
        self.appointment_list = []
        self.member_list = []

    def add_member(self, member):
        self.member_list.append(member)

    def add_attendance(self, topic, member):
        for appointment in self.appointment_list:
            if appointment.topic == topic:
                appointment.add_attn(member)

    def add_appointment(self, appointment):
        self.appointment_list.append(appointment)

    def edit_appointment(self, title=None, location=None, date=None, to=None):
        for appointment in self.appointment_list:
            appointment.edit_appointment(title, location, date, to)

    def delete_appointment(self, title=None, location=None, date=None):
        for appointment in self.appointment_list:
            if title != None:
                if appointment.topic == title:
                    self.appointment_list.remove(appointment)
            elif location != None:
                if appointment.location == location:
                    self.appointment_list.remove(appointment)
            elif date != None:
                if appointment.date == date:
                    self.appointment_list.remove(appointment)

    def view_appointments(self):
        for appointment in self.appointment_list:
            print(appointment.record())
            
    def show_person_in_appointment(self, member):
        for appointment in self.appointment_list:
            if appointment.attn == None:
                continue
            for attendance in appointment.attn:
                if attendance.name == member.name:
                    print(appointment.record())
    
    def send_notifications(self, topic, message):
        for appointment in self.appointment_list:
            if appointment.topic == topic:
                if appointment.type == "Activity":
                    for member in app.member_list:
                        member.notification(message)
                else:
                    for attendance in appointment.attn:
                        attendance.notification(message)

class Appointment:
    def __init__(self, topic, location, date, attn, type=None):
        self.topic = topic
        self.location = location
        self.date = date
        self.attn = attn
        self.type = type

    def add_attn(self, member):
        self.attn.append(member)

    def attendance(self):
        member = None
        for attendance in self.attn:
            if member == None:
                member = attendance.name
            else:
                member += f",{attendance.name}"
        return member
    
    def record(self):
        if self.type != "One-time AP":
            record = f"{self.type}, Topic : {self.topic} Location : {self.location} on {self.date} "
        else:
            record = f"Topic : {self.topic} Location : {self.location} on {self.date} "
        if self.type != "Activity":
            record += f"Attn: {self.attendance()}"
        return record

    def edit_appointment(self, title=None, location=None, date=None, to=None):
        if title != None:
            if self.topic == title:
                self.topic = to
        elif location != None:
            if self.location == location:
                self.location = to
        elif date != None:
            if self.date == date:
                self.date = to

class One_time_appointment(Appointment):
    def __init__(self, topic, location, date, attn):
        super().__init__(topic, location, date, attn, type="One-time AP")

class Weekly_appointment(Appointment):
    def __init__(self, topic, location, date, attn):
        super().__init__(topic, location, date, attn, type="Weekly AP")

class Activity(Appointment):
    def __init__(self, topic, location, date, attn=None):
        super().__init__(topic, location, date, attn, type="Activity")

class Member:
    def __init__(self, name, email, telephone_number, noti_type):
        self.name = name
        self.email = email
        self.telephone_number = telephone_number
        self.noti_type = noti_type
        if noti_type == "email":
            self.noti = self.email
        elif noti_type == "SMS":
            self.noti = self.telephone_number

    def notification(self, message):
        print(f"Sending {self.noti_type} notification to: {self.noti} with message : {message}")


app = AppointmentScheduler()

# Add Member
john = Member("John Doe", "john.doe@example.com", None, "email")
jane = Member("Jane Smith", "jane.smith@example.com", None, "email")
robert = Member("Robert Johnson", "robert.johnson@example.com", "08-1234-5678", "SMS")
michael = Member("Michael Brown", "michael.brown@example.com", None, "email")
emily = Member("Emily Davis", "emily.davis@example.com", "08-3456-7890", "SMS")
app.add_member(john)
app.add_member(jane)
app.add_member(robert)
app.add_member(michael)
app.add_member(emily)

# # Test Case 1 : Add Appointment, add activity information, and add appointment information.
# 1 : title="Team Meeting #1", location="Room A" , date="2024-03-15", Jane Smith, Robert Johnson,  Emily Davis
# 2 : title="Team Meeting #2", location="Room B" , date="2024-03-17", Jane Smith, Robert Johnson และ Emily Davis
# 3 : title="Weekly Meeting", location="Room C" , day_of_week="Wednesday"
# Activity
# 4 : title="Company Party", location="Conference Room", date="2024-03-17"
# 5 : title="Company Visit", location="Conference Room", date="2024-03-17"

# Output Expect
# Topic : Team Meeting #1 Location : Room A on 2024-03-15 Attn: Jane Smith,John Doe,Emily Davis
# Topic : Team Meeting #2 Location : Room B on 2024-03-17 Attn: Jane Smith,John Doe,Emily Davis
# Weekly AP, Topic : Weekly Meeting Location : Room C on Wednesday Attn: John Doe,Robert Johnson,Emily Davis
# Activity, Topic : Company Party Location : Conference Room on 2024-03-17
# Activity, Topic : Company Visit Location : Conference Room on 2024-03-17

print("# # Test Case 1 : Add Appointment, add activity information, and add appointment information. ")
app.add_appointment(One_time_appointment("Team Meeting #1", "Room A", "2024-03-15", [jane, robert, emily]))
app.add_appointment(One_time_appointment("Team Meeting #2", "Room B", "2024-03-17", [jane, robert, emily]))
app.add_appointment(Weekly_appointment("Weekly Meeting", "Room C", "Wednesday", [john, robert, emily]))
app.add_appointment(Activity("Company Party", "Conference Room", "2024-03-17"))
app.add_appointment(Activity("Company Visit", "Conference Room", "2024-03-17"))
app.view_appointments()            # Show all Appointments
print()

# # Test Case 2 : Edit Appointment 
# Change the name of One-Time Appointment #1 from “Team Meeting #1” to “Team B Meeting #1”
# Output Expect
# Topic : Team B Meeting #1 Location : Room A on 2024-03-15 Attn: Jane Smith,John Doe,Emily Davis
# Topic : Team Meeting #2 Location : Room C on 2024-03-17 Attn: Jane Smith,John Doe,Emily Davis
# Weekly AP, Topic : Weekly Meeting Location : Room C on Wednesday Attn: John Doe,Robert Johnson,Emily Davis
# Activity, Topic : Company Party Location : Conference Room on 2024-03-17
# Activity, Topic : Company Visit Location : Conference Room on 2024-03-17
print("Test Case 2 : Edit Appointment")
app.edit_appointment(title="Team Meeting #1",to="Team B Meeting #1")
app.edit_appointment(location="Room B",to="Room C")
app.view_appointments()            # Show all Appointments
print()


# # Test Case 3 : Delete Appointment using topic “Team Meeting #2” 
# Output Expect
# Topic : Team B Meeting #1 Location : Room A on 2024-03-15 Attn: Jane Smith,John Doe,Emily Davis
# Weekly AP, Topic : Weekly Meeting Location : Room C on Wednesday Attn: John Doe,Robert Johnson,Emily Davis
# Activity, Topic : Company Party Location : Conference Room on 2024-03-17
# Activity, Topic : Company Visit Location : Conference Room on 2024-03-17
print("Test Case 3 : Delete Appointment using topic “Team Meeting #2”")
app.delete_appointment(title="Team Meeting #2")
app.view_appointments()            # Show all Appointments
print()

# # Test Case 4 : Add Attendance who receives appointments for one-time appointments and weekly appointments as follows.
# - One-Time Appointment #1 (“Team B Meeting #1”) Add John Doe
# - Weekly Appointments “Weekly Meeting” added Jane Smith.

# Output Expect
# Topic : Team B Meeting #1 Location : Room A on 2024-03-15 Attn: Jane Smith,John Doe,Emily Davis,John Doe
# Weekly AP, Topic : Weekly Meeting Location : Room C on Wednesday Attn: John Doe,Robert Johnson,Emily Davis,Jane Smith
# Activity, Topic : Company Party Location : Conference Room on 2024-03-17
# Activity, Topic : Company Visit Location : Conference Room on 2024-03-17
print("Test Case 4 : Add Attendance who receives appointments for one-time appointments and weekly appointments")
app.add_attendance("Team B Meeting #1", john)
app.add_attendance("Weekly Meeting", jane)
app.view_appointments()            # Show all Appointments
print()

# # Test Case 5 : Search Attendance Search for individual appointments using the name “Robert Johnson”. 
# Output Expect
# Topic : Team B Meeting #1 Location : Room A on 2024-03-15 Attn: Jane Smith,John Doe,Emily Davis,John Doe
# Weekly AP, Topic : Weekly Meeting Location : Room C on Wednesday Attn: John Doe,Robert Johnson,Emily Davis,Jane Smith
print("Test Case 5 : Search Attendance Search for individual appointments using the name Robert Johnson")
app.show_person_in_appointment(john)
print()

# # Test Case 6 : Notify by using the appointment “Team B Meeting #1”
# Output Expect
# Sending email notification to: jane.smith@example.com with message : invite for meeting
# Sending SMS notification to: 08-1234-5678 with message : invite for meeting
# Sending SMS notification to: 08-3456-7890 with message : invite for meeting
# Sending email notification to: john.doe@example.com with message : invite for meeting
print("Test Case 6 : Notify by using the appointment “Team B Meeting #1")
app.send_notifications("Team B Meeting #1","invite for meeting")


