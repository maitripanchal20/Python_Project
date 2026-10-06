import tkinter as tk
from tkinter import messagebox
import backend


# =====================================================
# STUDENT STUDY PLANNER - FRONTEND
# =====================================================

BG = "#F3F9FD"
WHITE = "#FFFFFF"
PRIMARY = "#176B87"
DARK = "#0E4F68"
BLUE = "#5AA9D6"
TEXT = "#183B4E"
MUTED = "#718895"
BORDER = "#DCEAF2"
GREEN = "#2E9B68"
GREEN_BG = "#E9F7F0"
ORANGE = "#E99A3D"
ORANGE_BG = "#FFF3E2"
RED = "#D95D5D"
RED_BG = "#FDECEC"

FONT = "Segoe UI"


# =====================================================
# UPDATE DASHBOARD
# =====================================================

def update_dashboard():

    total, completed, pending, percentage = backend.get_counts()

    total_value.config(text=str(total))

    completed_value.config(
        text=str(completed)
    )

    pending_value.config(
        text=str(pending)
    )

    progress_value.config(
        text=str(round(percentage, 1)) + "%"
    )

    update_progress_bar()

    if total == 0:

        progress_message.config(
            text="Start by adding your first study task."
        )

    elif percentage == 100:

        progress_message.config(
            text="Excellent! All tasks are completed."
        )

    elif percentage >= 50:

        progress_message.config(
            text="Great progress! Keep going."
        )

    else:

        progress_message.config(
            text="Stay focused and keep studying."
        )


# =====================================================
# ADD TASK
# =====================================================

def add_task():

    subject = subject_entry.get().strip()

    time = time_entry.get().strip()

    duration = duration_entry.get().strip()


    # Check empty fields
    if subject == "" or time == "" or duration == "":

        messagebox.showwarning(
            "Missing Information",
            "Please fill Subject, Time and Duration."
        )

        return


    # Send task to backend
    # Backend checks time conflict
    success, message = backend.add_task(
        subject,
        time,
        duration
    )


    # If conflict / invalid input
    if not success:

        messagebox.showwarning(
            "Time Conflict",
            message
        )

        return


    # Clear fields
    subject_entry.delete(
        0,
        tk.END
    )

    time_entry.delete(
        0,
        tk.END
    )

    duration_entry.delete(
        0,
        tk.END
    )


    # Update dashboard
    update_dashboard()


    messagebox.showinfo(
        "Task Added",
        "Your study task was added successfully!"
    )


# =====================================================
# TASK WINDOW
# =====================================================

def open_task_window():

    task_window = tk.Toplevel(root)

    task_window.title(
        "My Study Tasks"
    )


    # =================================================
    # FULL MAXIMIZED WINDOW
    # =================================================

    task_window.state("zoomed")

    task_window.configure(
        bg=BG
    )


    # =================================================
    # HEADER
    # =================================================

    header = tk.Frame(
        task_window,
        bg=PRIMARY,
        height=120
    )

    header.pack(
        fill="x",
        side="top"
    )

    header.pack_propagate(False)


    tk.Label(
        header,
        text="My Study Tasks",
        font=(FONT, 30, "bold"),
        bg=PRIMARY,
        fg=WHITE
    ).pack(
        anchor="w",
        padx=50,
        pady=(25, 0)
    )


    tk.Label(
        header,
        text="Manage your daily study schedule",
        font=(FONT, 12),
        bg=PRIMARY,
        fg="#D9EEF7"
    ).pack(
        anchor="w",
        padx=52
    )


    # =================================================
    # BOTTOM AREA
    # =================================================

    bottom = tk.Frame(
        task_window,
        bg=BG,
        height=75
    )

    bottom.pack(
        fill="x",
        side="bottom"
    )

    bottom.pack_propagate(False)


    # =================================================
    # SCROLLABLE AREA
    # =================================================

    outer = tk.Frame(
        task_window,
        bg=BG
    )

    outer.pack(
        fill="both",
        expand=True,
        padx=35,
        pady=25
    )


    # =================================================
    # CANVAS
    # =================================================

    canvas = tk.Canvas(
        outer,
        bg=BG,
        highlightthickness=0
    )


    # =================================================
    # SCROLLBAR
    # =================================================

    scrollbar = tk.Scrollbar(
        outer,
        orient="vertical",
        command=canvas.yview
    )


    # =================================================
    # TASK CONTAINER
    # =================================================

    task_container = tk.Frame(
        canvas,
        bg=BG
    )


    # Create canvas window
    canvas_window = canvas.create_window(
        (0, 0),
        window=task_container,
        anchor="nw"
    )


    # Connect scrollbar
    canvas.configure(
        yscrollcommand=scrollbar.set
    )


    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )


    scrollbar.pack(
        side="right",
        fill="y"
    )


    # =================================================
    # UPDATE SCROLL REGION
    # =================================================

    def update_scroll_region(event=None):

        canvas.configure(
            scrollregion=canvas.bbox("all")
        )


    task_container.bind(
        "<Configure>",
        update_scroll_region
    )


    # =================================================
    # MAKE CONTENT SAME WIDTH AS CANVAS
    # =================================================

    def resize_canvas(event):

        canvas.itemconfig(
            canvas_window,
            width=event.width
        )


    canvas.bind(
        "<Configure>",
        resize_canvas
    )


    # =================================================
    # MOUSE WHEEL SCROLL
    # =================================================

    def mouse_scroll(event):

        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )


    # Bind mouse wheel to entire task window
    task_window.bind_all(
        "<MouseWheel>",
        mouse_scroll
    )


    # =================================================
    # REMOVE MOUSE SCROLL WHEN WINDOW CLOSES
    # =================================================

    def close_task_window():

        task_window.unbind_all(
            "<MouseWheel>"
        )

        task_window.destroy()


    # =================================================
    # DISPLAY TASKS
    # =================================================

    def refresh_tasks():

        # Remove previous cards
        for widget in task_container.winfo_children():

            widget.destroy()


        # Get sorted tasks
        task_list = backend.get_tasks()


        # =================================================
        # NO TASKS
        # =================================================

        if len(task_list) == 0:

            empty = tk.Frame(
                task_container,
                bg=WHITE,
                highlightbackground=BORDER,
                highlightthickness=1
            )


            empty.pack(
                fill="x",
                padx=10,
                pady=10
            )


            tk.Label(
                empty,
                text="No Study Tasks",
                font=(FONT, 22, "bold"),
                bg=WHITE,
                fg=TEXT
            ).pack(
                pady=(70, 5)
            )


            tk.Label(
                empty,
                text="Add a task from the main dashboard.",
                font=(FONT, 12),
                bg=WHITE,
                fg=MUTED
            ).pack(
                pady=(0, 70)
            )


            return


        # =================================================
        # DISPLAY TASKS
        # =================================================

        for index, task in enumerate(task_list):

            create_task_card(
                index,
                task
            )


    # =================================================
    # TASK CARD
    # =================================================

    def create_task_card(index, task):

        card = tk.Frame(
            task_container,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )


        card.pack(
            fill="x",
            padx=10,
            pady=7
        )


        # =================================================
        # TASK NUMBER
        # =================================================

        tk.Label(
            card,
            text=str(index + 1),
            font=(FONT, 13, "bold"),
            bg="#EAF6FF",
            fg=PRIMARY,
            width=4,
            height=2
        ).pack(
            side="left",
            padx=(18, 12),
            pady=18
        )


        # =================================================
        # DETAILS
        # =================================================

        details = tk.Frame(
            card,
            bg=WHITE
        )


        details.pack(
            side="left",
            fill="both",
            expand=True,
            pady=18
        )


        tk.Label(
            details,
            text=task["subject"],
            font=(FONT, 17, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(
            anchor="w"
        )


        tk.Label(
            details,
            text="Time: "
                 + task["time"]
                 + "    •    Duration: "
                 + task["duration"],
            font=(FONT, 11),
            bg=WHITE,
            fg=MUTED
        ).pack(
            anchor="w",
            pady=(5, 0)
        )


        # =================================================
        # STATUS
        # =================================================

        if task["status"] == "Completed":

            status_bg = GREEN_BG

            status_fg = GREEN

            status_text = "✓ Completed"

            button_text = "↩  Mark Uncompleted"

            button_bg = GREEN_BG

            button_fg = GREEN

        else:

            status_bg = ORANGE_BG

            status_fg = ORANGE

            status_text = "● Pending"

            button_text = "✓  Mark Completed"

            button_bg = "#EAF6FF"

            button_fg = PRIMARY


        tk.Label(
            card,
            text=status_text,
            font=(FONT, 10, "bold"),
            bg=status_bg,
            fg=status_fg,
            padx=15,
            pady=8
        ).pack(
            side="left",
            padx=10
        )


        # =================================================
        # BUTTON AREA
        # =================================================

        buttons = tk.Frame(
            card,
            bg=WHITE
        )


        buttons.pack(
            side="right",
            padx=(5, 20),
            pady=18
        )


        # =================================================
        # COMPLETE / UNCOMPLETE
        # =================================================

        def change_task_status(i=index):

            backend.change_status(i)

            update_dashboard()

            refresh_tasks()


        tk.Button(
            buttons,
            text=button_text,
            command=change_task_status,
            font=(FONT, 10, "bold"),
            bg=button_bg,
            fg=button_fg,
            activebackground=button_bg,
            activeforeground=button_fg,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=14,
            pady=8
        ).pack(
            pady=(0, 7)
        )


        # =================================================
        # DELETE
        # =================================================

        def delete_task_item(i=index):

            answer = messagebox.askyesno(
                "Delete Task",
                "Are you sure you want to delete this task?",
                parent=task_window
            )


            if answer:

                backend.delete_task(i)

                update_dashboard()

                refresh_tasks()


        tk.Button(
            buttons,
            text="Delete",
            command=delete_task_item,
            font=(FONT, 10),
            bg=RED_BG,
            fg=RED,
            activebackground=RED_BG,
            activeforeground=RED,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=30,
            pady=6
        ).pack()


    # =================================================
    # CLOSE BUTTON
    # =================================================

    tk.Button(
        bottom,
        text="Close",
        command=close_task_window,
        font=(FONT, 11, "bold"),
        bg=DARK,
        fg=WHITE,
        activebackground=PRIMARY,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=45,
        pady=10
    ).pack(
        pady=15
    )


    # =================================================
    # LOAD TASKS
    # =================================================

    refresh_tasks()


# =====================================================
# MAIN WINDOW
# =====================================================

root = tk.Tk()

root.title(
    "Student Study Planner"
)

root.geometry(
    "1100x720"
)

root.minsize(
    900,
    650
)

root.configure(
    bg=BG
)


# =====================================================
# SIDEBAR
# =====================================================

sidebar = tk.Frame(
    root,
    bg=DARK,
    width=235
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)


tk.Label(
    sidebar,
    text="STUDY\nPLANNER",
    font=(FONT, 24, "bold"),
    bg=DARK,
    fg=WHITE,
    justify="left"
).pack(
    anchor="w",
    padx=28,
    pady=(45, 8)
)


tk.Label(
    sidebar,
    text="Organize • Focus • Achieve",
    font=(FONT, 9),
    bg=DARK,
    fg="#BFDDE9"
).pack(
    anchor="w",
    padx=30
)


# =====================================================
# DIVIDER
# =====================================================

tk.Frame(
    sidebar,
    bg="#286A83",
    height=1
).pack(
    fill="x",
    padx=25,
    pady=35
)


tk.Label(
    sidebar,
    text="MENU",
    font=(FONT, 9, "bold"),
    bg=DARK,
    fg="#8FC8DF"
).pack(
    anchor="w",
    padx=30,
    pady=(0, 12)
)


# =====================================================
# DASHBOARD BUTTON
# =====================================================

tk.Button(
    sidebar,
    text="  ▣   Dashboard",
    font=(FONT, 11, "bold"),
    bg=PRIMARY,
    fg=WHITE,
    activebackground=PRIMARY,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    anchor="w",
    padx=20,
    pady=12
).pack(
    fill="x",
    padx=15
)


# =====================================================
# TASKS BUTTON
# =====================================================

tk.Button(
    sidebar,
    text="  ☑   My Tasks",
    command=open_task_window,
    font=(FONT, 11),
    bg=DARK,
    fg="#D8ECF4",
    activebackground=PRIMARY,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    anchor="w",
    padx=20,
    pady=12,
    cursor="hand2"
).pack(
    fill="x",
    padx=15,
    pady=4
)


# =====================================================
# BOTTOM MESSAGE
# =====================================================

tk.Label(
    sidebar,
    text="Stay consistent.\nSmall steps every day.",
    font=(FONT, 10, "italic"),
    bg=DARK,
    fg="#9EC8D8",
    justify="left"
).pack(
    side="bottom",
    anchor="w",
    padx=30,
    pady=35
)


# =====================================================
# MAIN CONTENT AREA - SCROLLABLE
# =====================================================

dashboard_area = tk.Frame(
    root,
    bg=BG
)

dashboard_area.pack(
    side="left",
    fill="both",
    expand=True
)


# =====================================================
# DASHBOARD CANVAS
# =====================================================

dashboard_canvas = tk.Canvas(
    dashboard_area,
    bg=BG,
    highlightthickness=0
)


dashboard_scrollbar = tk.Scrollbar(
    dashboard_area,
    orient="vertical",
    command=dashboard_canvas.yview
)


content = tk.Frame(
    dashboard_canvas,
    bg=BG
)


content_window = dashboard_canvas.create_window(
    (0, 0),
    window=content,
    anchor="nw"
)


dashboard_canvas.configure(
    yscrollcommand=dashboard_scrollbar.set
)


dashboard_canvas.pack(
    side="left",
    fill="both",
    expand=True
)


dashboard_scrollbar.pack(
    side="right",
    fill="y"
)


# =====================================================
# DASHBOARD SCROLL REGION
# =====================================================

def update_dashboard_scroll(event=None):

    dashboard_canvas.configure(
        scrollregion=dashboard_canvas.bbox("all")
    )


content.bind(
    "<Configure>",
    update_dashboard_scroll
)


def resize_dashboard(event):

    dashboard_canvas.itemconfig(
        content_window,
        width=event.width
    )


dashboard_canvas.bind(
    "<Configure>",
    resize_dashboard
)


# =====================================================
# DASHBOARD MOUSE WHEEL
# =====================================================

def dashboard_scroll(event):

    dashboard_canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


dashboard_canvas.bind(
    "<MouseWheel>",
    dashboard_scroll
)


# =====================================================
# HEADER
# =====================================================

header = tk.Frame(
    content,
    bg=BG
)


header.pack(
    fill="x",
    padx=35,
    pady=(30, 15)
)


tk.Label(
    header,
    text="Good day! 👋",
    font=(FONT, 12),
    bg=BG,
    fg=MUTED
).pack(
    anchor="w"
)


tk.Label(
    header,
    text="Your Study Dashboard",
    font=(FONT, 28, "bold"),
    bg=BG,
    fg=TEXT
).pack(
    anchor="w",
    pady=(2, 0)
)


tk.Label(
    header,
    text="Plan your sessions and keep track of your progress.",
    font=(FONT, 11),
    bg=BG,
    fg=MUTED
).pack(
    anchor="w",
    pady=(3, 0)
)


# =====================================================
# STAT CARDS
# =====================================================

stats = tk.Frame(
    content,
    bg=BG
)


stats.pack(
    fill="x",
    padx=35,
    pady=10
)


def create_stat_card(
    parent,
    title,
    value,
    color
):

    card = tk.Frame(
        parent,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )


    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 10)
    )


    tk.Frame(
        card,
        bg=color,
        width=5
    ).pack(
        side="left",
        fill="y"
    )


    inner = tk.Frame(
        card,
        bg=WHITE
    )


    inner.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=12
    )


    tk.Label(
        inner,
        text=title,
        font=(FONT, 10),
        bg=WHITE,
        fg=MUTED
    ).pack(
        anchor="w"
    )


    value_label = tk.Label(
        inner,
        text=value,
        font=(FONT, 24, "bold"),
        bg=WHITE,
        fg=TEXT
    )


    value_label.pack(
        anchor="w",
        pady=(3, 0)
    )


    return value_label


total_value = create_stat_card(
    stats,
    "TOTAL TASKS",
    "0",
    PRIMARY
)


completed_value = create_stat_card(
    stats,
    "COMPLETED",
    "0",
    GREEN
)


pending_value = create_stat_card(
    stats,
    "PENDING",
    "0",
    ORANGE
)


progress_value = create_stat_card(
    stats,
    "PROGRESS",
    "0%",
    BLUE
)


# =====================================================
# BODY
# =====================================================

body = tk.Frame(
    content,
    bg=BG
)


body.pack(
    fill="x",
    padx=35,
    pady=15
)


# =====================================================
# ADD TASK CARD
# =====================================================

add_card = tk.Frame(
    body,
    bg=WHITE,
    highlightbackground=BORDER,
    highlightthickness=1
)


add_card.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 8)
)


tk.Label(
    add_card,
    text="Add Study Task",
    font=(FONT, 18, "bold"),
    bg=WHITE,
    fg=TEXT
).pack(
    anchor="w",
    padx=25,
    pady=(25, 3)
)


tk.Label(
    add_card,
    text="Create a new session for your timetable.",
    font=(FONT, 10),
    bg=WHITE,
    fg=MUTED
).pack(
    anchor="w",
    padx=25,
    pady=(0, 20)
)


def create_label(text):

    tk.Label(
        add_card,
        text=text,
        font=(FONT, 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=25,
        pady=(7, 5)
    )


def create_entry():

    entry = tk.Entry(
        add_card,
        font=(FONT, 11),
        bg="#F8FBFD",
        fg=TEXT,
        insertbackground=TEXT,
        relief="flat",
        highlightbackground=BORDER,
        highlightcolor=BLUE,
        highlightthickness=1
    )


    entry.pack(
        fill="x",
        padx=25,
        ipady=9
    )


    return entry


create_label("Subject")

subject_entry = create_entry()


create_label("Study Time")

time_entry = create_entry()


create_label("Duration")

duration_entry = create_entry()


# =====================================================
# ADD STUDY TASK BUTTON
# =====================================================

tk.Button(
    add_card,
    text="+  Add Study Task",
    command=add_task,
    font=(FONT, 11, "bold"),
    bg=PRIMARY,
    fg=WHITE,
    activebackground=DARK,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    cursor="hand2",
    pady=11
).pack(
    fill="x",
    padx=25,
    pady=(22, 8)
)


# =====================================================
# VIEW ALL TASKS
# =====================================================

tk.Button(
    add_card,
    text="View All Tasks  →",
    command=open_task_window,
    font=(FONT, 10, "bold"),
    bg="#EAF6FF",
    fg=PRIMARY,
    activebackground="#DDEFF8",
    activeforeground=DARK,
    relief="flat",
    bd=0,
    cursor="hand2",
    pady=10
).pack(
    fill="x",
    padx=25,
    pady=(0, 20)
)


# =====================================================
# PROGRESS CARD
# =====================================================

progress_card = tk.Frame(
    body,
    bg=WHITE,
    highlightbackground=BORDER,
    highlightthickness=1
)


progress_card.pack(
    side="right",
    fill="both",
    expand=True,
    padx=(8, 0)
)


tk.Label(
    progress_card,
    text="Today's Progress",
    font=(FONT, 18, "bold"),
    bg=WHITE,
    fg=TEXT
).pack(
    anchor="w",
    padx=25,
    pady=(25, 3)
)


tk.Label(
    progress_card,
    text="Your completed study sessions.",
    font=(FONT, 10),
    bg=WHITE,
    fg=MUTED
).pack(
    anchor="w",
    padx=25,
    pady=(0, 28)
)


# =====================================================
# PROGRESS BAR
# =====================================================

progress_background = tk.Frame(
    progress_card,
    bg="#EAF1F5",
    height=18
)


progress_background.pack(
    fill="x",
    padx=25
)


progress_background.pack_propagate(False)


progress_fill = tk.Frame(
    progress_background,
    bg=BLUE
)


progress_fill.place(
    x=0,
    y=0,
    relheight=1,
    relwidth=0
)


def update_progress_bar():

    total, completed, pending, percentage = backend.get_counts()

    progress_fill.place(
        relwidth=percentage / 100
    )


progress_message = tk.Label(
    progress_card,
    text="Start by adding your first study task.",
    font=(FONT, 10),
    bg=WHITE,
    fg=MUTED,
    wraplength=300,
    justify="left"
)


progress_message.pack(
    anchor="w",
    padx=25,
    pady=(18, 20)
)


# =====================================================
# TIP BOX
# =====================================================

tip_box = tk.Frame(
    progress_card,
    bg="#F7FBFD"
)


tip_box.pack(
    fill="x",
    padx=25,
    pady=5
)


tk.Label(
    tip_box,
    text="TIP",
    font=(FONT, 10, "bold"),
    bg="#F7FBFD",
    fg=PRIMARY
).pack(
    anchor="w",
    padx=15,
    pady=(12, 4)
)


tk.Label(
    tip_box,
    text="Complete your planned sessions one by one. "
         "You can also uncomplete a task if it was marked by accident.",
    font=(FONT, 10),
    bg="#F7FBFD",
    fg=MUTED,
    wraplength=310,
    justify="left"
).pack(
    anchor="w",
    padx=15,
    pady=(0, 15)
)


# =====================================================
# START APPLICATION
# =====================================================

backend.load_data()

backend.sort_tasks()

update_dashboard()

root.mainloop()