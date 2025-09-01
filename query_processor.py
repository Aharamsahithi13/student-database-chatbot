import mysql.connector
from mysql.connector import pooling
import time
import re
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create a connection pool
connection_pool = pooling.MySQLConnectionPool(
    pool_name="my_pool",
    pool_size=5,
    host="127.0.0.1",
    user="root",
    password="your_mysql_password",
    database="chatbotdb",
    autocommit=True,
    connection_timeout=10,
    buffered=True
)

class DBConnection:
    """Context manager for database connections"""
    def __enter__(self):
        self.conn = connection_pool.get_connection()
        logger.debug("Got connection from pool")
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
            logger.debug("Released connection back to pool")

def get_table_columns():
    columns = []
    try:
        with DBConnection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SHOW COLUMNS FROM student_data")
                result = cursor.fetchall()
                columns = [column[0] for column in result]
                logger.debug(f"Table columns found: {columns}")
    except Exception as e:
        logger.error(f"Error getting table structure: {e}")
        columns = []
    return columns

def process_query(user_input):
    user_input = user_input.lower().strip()
    query_timestamp = time.strftime('%H:%M:%S')
    logger.debug(f"[{query_timestamp}] Processing query: '{user_input}'")

    response = "Sorry, I didn't understand your question. Please try asking another question."

    try:
        columns = get_table_columns()
        logger.debug(f"Available columns: {columns}")

        if not isinstance(columns, list):
            columns = []

        with DBConnection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                # Student ID lookup
                if ("student id" in user_input or "id" in user_input) and any(char.isdigit() for char in user_input):
                    logger.debug("Processing student ID query")
                    student_id_match = re.search(r'\d+', user_input)
                    if student_id_match:
                        student_id = student_id_match.group()
                        cursor.execute("SELECT student_name FROM student_data WHERE student_id = %s", (student_id,))
                        result = cursor.fetchone()
                        if result:
                            response = f"The name of the student with student ID {student_id} is {result['student_name']}."
                        else:
                            response = f"No student found with student ID {student_id}."

                # Total count queries for field of study
                elif any(keyword in user_input for keyword in ["total", "how many", "count"]):
                    logger.debug("Processing count query for field of study")
                    if any(field in user_input for field in ["mechanical engineering", "mechanical"]):
                        cursor.execute("SELECT COUNT(*) AS count FROM student_data WHERE LOWER(field_of_study) LIKE LOWER('%Mechanical%')")
                        result = cursor.fetchone()
                        response = f"The total number of students in Mechanical Engineering is {result['count']}."
                    elif any(field in user_input for field in ["electrical engineering", "electrical"]):
                        cursor.execute("SELECT COUNT(*) AS count FROM student_data WHERE LOWER(field_of_study) LIKE LOWER('%Electrical%')")
                        result = cursor.fetchone()
                        response = f"The total number of students in Electrical Engineering is {result['count']}."
                    elif any(field in user_input for field in ["computer engineering", "computer"]):
                        cursor.execute("SELECT COUNT(*) AS count FROM student_data WHERE LOWER(field_of_study) LIKE LOWER('%Computer%')")
                        result = cursor.fetchone()
                        response = f"The total number of students in Computer Engineering is {result['count']}."
                    elif any(field in user_input for field in ["civil engineering", "civil"]):
                        cursor.execute("SELECT COUNT(*) AS count FROM student_data WHERE LOWER(field_of_study) LIKE LOWER('%Civil%')")
                        result = cursor.fetchone()
                        response = f"The total number of students in Civil Engineering is {result['count']}."
                    elif any(field in user_input for field in ["chemical engineering", "chemical"]):
                        cursor.execute("SELECT COUNT(*) AS count FROM student_data WHERE LOWER(field_of_study) LIKE LOWER('%Chemical%')")
                        result = cursor.fetchone()
                        response = f"The total number of students in Chemical Engineering is {result['count']}."
                    else:
                        cursor.execute("SELECT COUNT(*) AS count FROM student_data")
                        result = cursor.fetchone()
                        response = f"The total number of students is {result['count']}."

                # Total count queries for specialization
                elif any(keyword in user_input for keyword in ["specialization", "specialisation"]):
                    logger.debug("Processing count query for specialization")
                    if any(field in user_input for field in ["web development", "web"]):
                        cursor.execute("SELECT COUNT(*) AS count FROM student_data WHERE LOWER(specialization) LIKE LOWER('%Web Development%')")
                        result = cursor.fetchone()
                        response = f"The total number of students in Web Development is {result['count']}."
                    elif any(field in user_input for field in ["data science", "data"]):
                        cursor.execute("SELECT COUNT(*) AS count FROM student_data WHERE LOWER(specialization) LIKE LOWER('%Data Science%')")
                        result = cursor.fetchone()
                        response = f"The total number of students in Data Science is {result['count']}."
                    elif any(field in user_input for field in ["artificial intelligence", "ai"]):
                        cursor.execute("SELECT COUNT(*) AS count FROM student_data WHERE LOWER(specialization) LIKE LOWER('%Artificial Intelligence%')")
                        result = cursor.fetchone()
                        response = f"The total number of students in Artificial Intelligence is {result['count']}."
                    elif any(field in user_input for field in ["network security", "network"]):
                        cursor.execute("SELECT COUNT(*) AS count FROM student_data WHERE LOWER(specialization) LIKE LOWER('%Network Security%')")
                        result = cursor.fetchone()
                        response = f"The total number of students in Network Security is {result['count']}."
                    elif any(field in user_input for field in ["machine learning", "ml"]):
                        cursor.execute("SELECT COUNT(*) AS count FROM student_data WHERE LOWER(specialization) LIKE LOWER('%Machine Learning%')")
                        result = cursor.fetchone()
                        response = f"The total number of students in Machine Learning is {result['count']}."

                # Average queries
                elif any(keyword in user_input for keyword in ["average", "avg", "mean"]):
                    logger.debug("Processing average query")
                    if any(fee in user_input for fee in ["fees", "fee"]):
                        cursor.execute("SELECT AVG(fees) AS avg_fees FROM student_data WHERE fees IS NOT NULL")
                        result = cursor.fetchone()
                        if result and result['avg_fees'] is not None:
                            response = f"The average fees is ${result['avg_fees']:.2f}."
                        else:
                            response = "Could not calculate the average fees."

                # Minimum queries
                elif any(keyword in user_input for keyword in ["minimum", "min", "lowest", "smallest"]):
                    logger.debug("Processing minimum query")
                    if any(fee in user_input for fee in ["fees", "fee"]):
                        cursor.execute("SELECT MIN(fees) AS min_fees, student_name FROM student_data WHERE fees = (SELECT MIN(fees) FROM student_data WHERE fees IS NOT NULL) LIMIT 1")
                        result = cursor.fetchone()
                        if result:
                            response = f"The minimum fees is ${result['min_fees']:.2f}, paid by student {result['student_name']}."
                        else:
                            response = "Could not find minimum fees information."

                # Maximum queries
                elif any(keyword in user_input for keyword in ["maximum", "max", "highest", "largest"]):
                    logger.debug("Processing maximum query")
                    if any(fee in user_input for fee in ["fees", "fee"]):
                        cursor.execute("SELECT MAX(fees) AS max_fees, student_name FROM student_data WHERE fees = (SELECT MAX(fees) FROM student_data WHERE fees IS NOT NULL) LIMIT 1")
                        result = cursor.fetchone()
                        if result:
                            response = f"The maximum fees is ${result['max_fees']:.2f}, paid by student {result['student_name']}."
                        else:
                            response = "Could not find maximum fees information."

                # Show table/list queries
                elif any(keyword in user_input for keyword in ["show", "list", "display", "all students"]):
                    logger.debug("Processing list query")
                    available_cols = ['student_name', 'field_of_study', 'specialization', 'fees']
                    col_list = ', '.join(available_cols)

                    # Default query: show all students
                    query = f"SELECT {col_list} FROM student_data ORDER BY student_name LIMIT 10"

                    if any(field in user_input for field in ["mechanical engineering", "mechanical"]):
                        query = f"SELECT {col_list} FROM student_data WHERE LOWER(field_of_study) LIKE LOWER('%Mechanical%') ORDER BY student_name LIMIT 5"
                    elif any(field in user_input for field in ["electrical engineering", "electrical"]):
                        query = f"SELECT {col_list} FROM student_data WHERE LOWER(field_of_study) LIKE LOWER('%Electrical%') ORDER BY student_name LIMIT 5"
                    elif any(field in user_input for field in ["computer engineering", "computer"]):
                        query = f"SELECT {col_list} FROM student_data WHERE LOWER(field_of_study) LIKE LOWER('%Computer%') ORDER BY student_name LIMIT 5"
                    elif any(field in user_input for field in ["civil engineering", "civil"]):
                        query = f"SELECT {col_list} FROM student_data WHERE LOWER(field_of_study) LIKE LOWER('%Civil%') ORDER BY student_name LIMIT 5"
                    elif any(field in user_input for field in ["chemical engineering", "chemical"]):
                        query = f"SELECT {col_list} FROM student_data WHERE LOWER(field_of_study) LIKE LOWER('%Chemical%') ORDER BY student_name LIMIT 5"
                    elif any(field in user_input for field in ["web development", "web"]):
                        query = f"SELECT {col_list} FROM student_data WHERE LOWER(specialization) LIKE LOWER('%Web Development%') ORDER BY student_name LIMIT 5"
                    elif any(field in user_input for field in ["data science", "data"]):
                        query = f"SELECT {col_list} FROM student_data WHERE LOWER(specialization) LIKE LOWER('%Data Science%') ORDER BY student_name LIMIT 5"
                    elif any(field in user_input for field in ["artificial intelligence", "ai"]):
                        query = f"SELECT {col_list} FROM student_data WHERE LOWER(specialization) LIKE LOWER('%Artificial Intelligence%') ORDER BY student_name LIMIT 5"
                    elif any(field in user_input for field in ["network security", "network"]):
                        query = f"SELECT {col_list} FROM student_data WHERE LOWER(specialization) LIKE LOWER('%Network Security%') ORDER BY student_name LIMIT 5"
                    elif any(field in user_input for field in ["machine learning", "ml"]):
                        query = f"SELECT {col_list} FROM student_data WHERE LOWER(specialization) LIKE LOWER('%Machine Learning%') ORDER BY student_name LIMIT 5"

                    cursor.execute(query)
                    results = cursor.fetchall()

                    if results:
                        response = {
                            "type": "table",
                            "headers": available_cols,
                            "rows": results
                        }
                    else:
                        response = "No students found matching your criteria."

                # Debug query to show available columns
                elif any(keyword in user_input for keyword in ["columns", "structure"]):
                    logger.debug("Processing columns query")
                    response = f"Available columns in student_data table: {', '.join(columns)}"
                    if columns:
                        cols_to_show = columns[:5] if len(columns) > 5 else columns
                        sample_query = f"SELECT {', '.join(cols_to_show)} FROM student_data LIMIT 2"
                        cursor.execute(sample_query)
                        sample_data = cursor.fetchall()
                        response += f"\n\nSample data:\n{sample_data}"

                logger.debug(f"Final response: {response}")
    except mysql.connector.Error as err:
        logger.error(f"Database Error: {err}")
        response = f"Database error: {str(err)}"
    except Exception as e:
        logger.error(f"Application Error: {e}")
        response = f"An unexpected error occurred: {str(e)}"

    return response
