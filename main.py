from fastapi import FastAPI, HTTPException
import numpy as np
import plotly.graph_objects as go
import os


app = FastAPI(
    title="Student Analytics API",
    description="Student Analytics using FastAPI, NumPy and Plotly",
    version="1.0.0"
)


# =========================================================
# STUDENT DATA
# =========================================================

students = [
    {
        "student_id": 1,
        "name": "Rahul",
        "python": 85,
        "mathematics": 78,
        "data_science": 88
    },
    {
        "student_id": 2,
        "name": "Priya",
        "python": 92,
        "mathematics": 89,
        "data_science": 94
    },
    {
        "student_id": 3,
        "name": "Amit",
        "python": 76,
        "mathematics": 81,
        "data_science": 79
    },
    {
        "student_id": 4,
        "name": "Sneha",
        "python": 88,
        "mathematics": 95,
        "data_science": 91
    },
    {
        "student_id": 5,
        "name": "Rohan",
        "python": 67,
        "mathematics": 72,
        "data_science": 70
    },
    {
        "student_id": 6,
        "name": "Neha",
        "python": 95,
        "mathematics": 91,
        "data_science": 96
    },
    {
        "student_id": 7,
        "name": "Karan",
        "python": 72,
        "mathematics": 68,
        "data_science": 75
    },
    {
        "student_id": 8,
        "name": "Anjali",
        "python": 89,
        "mathematics": 86,
        "data_science": 90
    },
    {
        "student_id": 9,
        "name": "Vikas",
        "python": 81,
        "mathematics": 77,
        "data_science": 84
    },
    {
        "student_id": 10,
        "name": "Pooja",
        "python": 94,
        "mathematics": 93,
        "data_science": 92
    },
    {
        "student_id": 11,
        "name": "Suresh",
        "python": 63,
        "mathematics": 69,
        "data_science": 65
    },
    {
        "student_id": 12,
        "name": "Meena",
        "python": 87,
        "mathematics": 84,
        "data_science": 89
    },
    {
        "student_id": 13,
        "name": "Arjun",
        "python": 79,
        "mathematics": 75,
        "data_science": 82
    },
    {
        "student_id": 14,
        "name": "Kavya",
        "python": 91,
        "mathematics": 90,
        "data_science": 93
    },
    {
        "student_id": 15,
        "name": "Nikhil",
        "python": 70,
        "mathematics": 73,
        "data_science": 71
    },
    {
        "student_id": 16,
        "name": "Ayesha",
        "python": 96,
        "mathematics": 94,
        "data_science": 97
    },
    {
        "student_id": 17,
        "name": "Vivek",
        "python": 74,
        "mathematics": 80,
        "data_science": 77
    },
    {
        "student_id": 18,
        "name": "Isha",
        "python": 86,
        "mathematics": 88,
        "data_science": 85
    },
    {
        "student_id": 19,
        "name": "Manish",
        "python": 69,
        "mathematics": 64,
        "data_science": 68
    },
    {
        "student_id": 20,
        "name": "Riya",
        "python": 90,
        "mathematics": 87,
        "data_science": 91
    }
]


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def get_numpy_arrays():
    """
    Convert student marks into NumPy arrays.
    """

    python_marks = np.array(
        [student["python"] for student in students]
    )

    mathematics_marks = np.array(
        [student["mathematics"] for student in students]
    )

    data_science_marks = np.array(
        [student["data_science"] for student in students]
    )

    return python_marks, mathematics_marks, data_science_marks


def calculate_average(student):
    """
    Calculate average marks of one student.
    """

    marks = np.array([
        student["python"],
        student["mathematics"],
        student["data_science"]
    ])

    return round(float(np.mean(marks)), 2)


# =========================================================
# 1. GET ALL STUDENTS
# =========================================================

@app.get("/students")
def get_students():

    return {
        "count": len(students),
        "students": students
    }


# =========================================================
# 2. GET STUDENT BY ID
# =========================================================

@app.get("/student/{student_id}")
def get_student(student_id: int):

    for student in students:

        if student["student_id"] == student_id:

            result = student.copy()

            result["overall_average"] = calculate_average(student)

            return result

    raise HTTPException(
        status_code=404,
        detail=f"Student with ID {student_id} not found"
    )


# =========================================================
# 3. PYTHON AVERAGE
# =========================================================

@app.get("/average/python")
def python_average():

    python_marks, _, _ = get_numpy_arrays()

    average = np.mean(python_marks)

    return {
        "subject": "Python",
        "average": round(float(average), 2)
    }


# =========================================================
# 4. MATHEMATICS AVERAGE
# =========================================================

@app.get("/average/mathematics")
def mathematics_average():

    _, mathematics_marks, _ = get_numpy_arrays()

    average = np.mean(mathematics_marks)

    return {
        "subject": "Mathematics",
        "average": round(float(average), 2)
    }


# =========================================================
# 5. DATA SCIENCE AVERAGE
# =========================================================

@app.get("/average/data-science")
def data_science_average():

    _, _, data_science_marks = get_numpy_arrays()

    average = np.mean(data_science_marks)

    return {
        "subject": "Data Science",
        "average": round(float(average), 2)
    }


# =========================================================
# 6. TOP STUDENT
# =========================================================

@app.get("/topper")
def get_topper():

    student_averages = []

    for student in students:

        average = calculate_average(student)

        student_averages.append(average)

    highest_index = np.argmax(student_averages)

    topper = students[highest_index].copy()

    topper["overall_average"] = student_averages[highest_index]

    return {
        "message": "Top student",
        "student": topper
    }


# =========================================================
# 7. PASSED STUDENTS
# =========================================================

@app.get("/passed")
def get_passed_students():

    passed_students = []

    for student in students:

        marks = np.array([
            student["python"],
            student["mathematics"],
            student["data_science"]
        ])

        # Passing criteria:
        # Minimum 40 marks in every subject
        # AND overall average >= 50

        if np.all(marks >= 40) and np.mean(marks) >= 50:

            result = student.copy()

            result["overall_average"] = round(
                float(np.mean(marks)), 2
            )

            passed_students.append(result)

    return {
        "passing_criteria": "Minimum 40 in every subject and overall average >= 50",
        "count": len(passed_students),
        "students": passed_students
    }


# =========================================================
# 8. FAILED STUDENTS
# =========================================================

@app.get("/failed")
def get_failed_students():

    failed_students = []

    for student in students:

        marks = np.array([
            student["python"],
            student["mathematics"],
            student["data_science"]
        ])

        if not (np.all(marks >= 40) and np.mean(marks) >= 50):

            result = student.copy()

            result["overall_average"] = round(
                float(np.mean(marks)), 2
            )

            failed_students.append(result)

    return {
        "count": len(failed_students),
        "students": failed_students
    }


# =========================================================
# 9. STATISTICS
# =========================================================

@app.get("/statistics")
def get_statistics():

    python_marks, mathematics_marks, data_science_marks = \
        get_numpy_arrays()

    all_marks = np.concatenate([
        python_marks,
        mathematics_marks,
        data_science_marks
    ])

    statistics = {

        "subject_averages": {
            "python": round(float(np.mean(python_marks)), 2),
            "mathematics": round(float(np.mean(mathematics_marks)), 2),
            "data_science": round(float(np.mean(data_science_marks)), 2)
        },

        "highest_marks": {
            "python": int(np.max(python_marks)),
            "mathematics": int(np.max(mathematics_marks)),
            "data_science": int(np.max(data_science_marks))
        },

        "lowest_marks": {
            "python": int(np.min(python_marks)),
            "mathematics": int(np.min(mathematics_marks)),
            "data_science": int(np.min(data_science_marks))
        },

        "overall_average": round(
            float(np.mean(all_marks)), 2
        )
    }

    return statistics


# =========================================================
# 10. PLOTLY - SUBJECT AVERAGE BAR CHART
# =========================================================

@app.get("/visualization/average-marks")
def average_marks_visualization():

    python_marks, mathematics_marks, data_science_marks = \
        get_numpy_arrays()

    subjects = [
        "Python",
        "Mathematics",
        "Data Science"
    ]

    averages = [
        np.mean(python_marks),
        np.mean(mathematics_marks),
        np.mean(data_science_marks)
    ]

    fig = go.Figure(
        data=[
            go.Bar(
                x=subjects,
                y=averages,
                text=[round(float(x), 2) for x in averages],
                textposition="auto"
            )
        ]
    )

    fig.update_layout(
        title="Average Marks Across Subjects",
        xaxis_title="Subjects",
        yaxis_title="Average Marks",
        yaxis=dict(range=[0, 100])
    )

    os.makedirs("visualizations", exist_ok=True)

    file_path = "visualizations/average_marks.html"

    fig.write_html(file_path)

    return {
        "message": "Plotly bar chart created successfully",
        "file": file_path,
        "subjects": subjects,
        "averages": [
            round(float(x), 2)
            for x in averages
        ]
    }


# =========================================================
# 11. PLOTLY - TOP FIVE STUDENTS
# =========================================================

@app.get("/visualization/top-five")
def top_five_visualization():

    student_data = []

    for student in students:

        average = calculate_average(student)

        student_data.append({
            "name": student["name"],
            "average": average
        })

    # Sort by average in descending order

    student_data.sort(
        key=lambda x: x["average"],
        reverse=True
    )

    top_five = student_data[:5]

    names = [
        student["name"]
        for student in top_five
    ]

    averages = [
        student["average"]
        for student in top_five
    ]

    fig = go.Figure(
        data=[
            go.Bar(
                x=names,
                y=averages,
                text=averages,
                textposition="auto"
            )
        ]
    )

    fig.update_layout(
        title="Top Five Students",
        xaxis_title="Students",
        yaxis_title="Overall Average",
        yaxis=dict(range=[0, 100])
    )

    os.makedirs("visualizations", exist_ok=True)

    file_path = "visualizations/top_five_students.html"

    fig.write_html(file_path)

    return {
        "message": "Top five visualization created successfully",
        "top_five": top_five,
        "file": file_path
    }


# =========================================================
# ROOT API
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Welcome to Student Analytics API",
        "total_students": len(students),
        "documentation": "/docs"
    }