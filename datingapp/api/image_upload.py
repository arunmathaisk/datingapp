import os
import frappe
from werkzeug.wrappers import Request, Response
from werkzeug.utils import secure_filename
from pathlib import Path

ALLOWED_EXTENSIONS = {"png", "jpeg", "jpg"}
MAX_FILE_SIZE_MB = 10  # Maximum allowed file size in megabytes

def is_allowed_extension(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@frappe.whitelist()
def upload(picture_number):
    # Convert picture_number to an integer
    try:
        picture_number = int(picture_number)
    except ValueError:
        frappe.throw("Invalid picture number. Please provide a valid integer.")

    # Check if the provided picture_number is not in the allowed range
    if picture_number not in {1, 2, 3, 4, 5}:
        frappe.throw("Invalid picture number. Please provide a number between 1 and 5.")

    # Get the uploaded file from the request
    uploaded_file = frappe.request.files.get("file")

    # Check if a file was provided
    if not uploaded_file:
        frappe.throw("Please provide a file")

    # Check if the file size is above the limit (in bytes)
    if uploaded_file.content_length > MAX_FILE_SIZE_MB * 1024 * 1024:
        frappe.throw("File size exceeds the maximum allowed size of {}MB".format(MAX_FILE_SIZE_MB))

    # Get the file name and save path
    file_name = secure_filename(uploaded_file.filename)
    save_path = os.path.join(frappe.get_site_path("private/files"), file_name)

    # Check if the file already exists
    if os.path.exists(save_path):
        frappe.throw("File already exists")

    # Check if the file has an allowed extension
    if not is_allowed_extension(file_name):
        frappe.throw("Invalid file extension. Allowed extensions are: {}".format(", ".join(ALLOWED_EXTENSIONS)))

    try:
        # Save the uploaded file
        uploaded_file.save(save_path)
    except Exception as e:
        frappe.throw("Failed to Upload the File")

    reply_dict = {"type": "success", "info": "File Successfully Uploaded"}
    return reply_dict
