from requests.auth import HTTPBasicAuth
import requests
import json
from pypdf import PdfReader, PdfWriter
import pandas as pd
import mimetypes
import time
from selenium.webdriver.common.by import By
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def click_button(xpath, driver, timeout=None):
    """
    Clicks a button on a webpage using Selenium WebDriver.

    Args:
        xpath (str): The XPath of the button to click.
        driver (selenium.webdriver): The Selenium WebDriver instance.
        timeout (float, optional): The time (in seconds) to attempt clicking before timing out. Defaults to None.

    Returns:
        None
    """
    start_time = time.time()
    while True:
        try:
            button = driver.find_element(By.XPATH, xpath)
            button.click()
            break
        except Exception as e:
            if timeout is not None:
                if (time.time() - start_time) > timeout:
                    print(f'Error clicking button: {e}')
                    break


def send_text(text, xpath, driver, timeout=None):
    """
    Sends text to a specified input field on a webpage using Selenium WebDriver.

    Args:
        text (str): The text to send to the input field.
        xpath (str): The XPath of the input field.
        driver (selenium.webdriver): The Selenium WebDriver instance.
        timeout (float, optional): The time (in seconds) to attempt sending text before timing out. Defaults to None.

    Returns:
        None
    """
    start_time = time.time()
    while True:
        try:
            box = driver.find_element(By.XPATH, xpath)
            box.send_keys(text)
            break
        except Exception as e:
            if timeout is not None:
                if (time.time() - start_time) > timeout:
                    print(f'Error sending text: {e}')
                    break

def switch_to_iframe(xpath, driver, timeout=None):
    """
    Switches the WebDriver context to a specified iframe.

    Args:
        xpath (str): The XPath of the iframe to switch to.
        driver (selenium.webdriver): The Selenium WebDriver instance.
        timeout (float, optional): The time (in seconds) to attempt switching before timing out. Defaults to None.

    Returns:
        None
    """
    start_time = time.time()
    while True:
        try:
            iframe = driver.find_element(By.XPATH, xpath)
            driver.switch_to.frame(iframe)
            break
        except Exception as e:
            if timeout is not None:
                if (time.time() - start_time) > timeout:
                    print(f'Error clicking button: {e}')
                    break

def switch_to_default_frame(driver):
    """
    Switches the WebDriver context back to the default content frame.

    Args:
        driver (selenium.webdriver): The Selenium WebDriver instance.

    Returns:
        None
    """
    driver.switch_to.default_content()

def refresh_quickbooks_access_token(QUICKBOOKS_TOKENS, QUICKBOOKS_CLIENT_ID, QUICKBOOKS_CLIENT_SECRET):

    """
    Refreshes the QuickBooks Online OAuth2 access token.

    Args:
        QUICKBOOKS_TOKENS (dict): A dictionary containing the 'accessToken' and 'refreshToken'.
        QUICKBOOKS_CLIENT_ID (str): The QuickBooks client ID.
        QUICKBOOKS_CLIENT_SECRET (str): The QuickBooks client secret.

    Returns:
        dict: The updated QuickBooks tokens.
    """

    # QuickBooks Online OAuth2 token endpoint
    token_url = 'https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer'

    # Prepare the request payload
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': QUICKBOOKS_TOKENS['refreshToken'],
    }

    # Make the request to get a new access token
    response = requests.post(
        token_url,
        data=payload,
        auth=HTTPBasicAuth(QUICKBOOKS_CLIENT_ID, QUICKBOOKS_CLIENT_SECRET),
        headers={'Accept': 'application/json'},
    )

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        new_tokens = response.json()
        QUICKBOOKS_TOKENS['accessToken'] = new_tokens.get('access_token')
        QUICKBOOKS_TOKENS['refreshToken'] = new_tokens.get('refresh_token')
        print('TOKENS REFRESHED SUCCESSFULLY')
        # print(json.dumps(new_tokens,indent=2))
    else:
        # Handle errors
        print(f"FAILED TO REFRESH TOKENS: {response.status_code}")
        #print(response.json())
    return QUICKBOOKS_TOKENS


def get_pdf(filepath):
    """
    Extracts form fields from a PDF and returns them as a Pandas DataFrame.

    Args:
        filepath (str): The path to the PDF file.

    Returns:
        pandas.DataFrame: A DataFrame containing field names, types, and values.
    """
    reader = PdfReader(filepath)

    fields = reader.get_fields()

    field_names = []
    field_types = []
    field_values = []

    for field_name, field in fields.items():
        field_type = field.get('/FT', '')
        field_value = field.get('/V', '')

        field_names.append(field_name)
        field_types.append(field_type)
        field_values.append(field_value)

    df = pd.DataFrame(columns=['name', 'type', 'value'])
    df['name'] = field_names
    df['type'] = field_types
    df['value'] = field_values
    return df

def create_pdf(templatepath, topath, update_dict):
    """
    Creates a new PDF by updating fields in a template PDF.

    Args:
        templatepath (str): The path to the template PDF.
        topath (str): The path to save the updated PDF.
        update_dict (dict): A dictionary of field names and values to update.

    Returns:
        None
    """
    # Open the PDF
    reader = PdfReader(templatepath)
    writer = PdfWriter()
    writer.append(reader)

    # Write data to each page in the PDF file
    pagenum = 0
    while True:
        try:
            writer.update_page_form_field_values(writer.pages[pagenum], update_dict)
            pagenum = pagenum + 1
        except Exception: # An exception is raised when the pagenum exceeds the number of pages in the PDF document. When that happens, we are done adding data to the PDF file so we break out of this while loop.
            break

    # Save the updated PDF
    with open(topath, "wb") as pdf_output:
        writer.write(pdf_output)

# Add attachment to a GMAIL email

def add_attachment(path_to_file, message):
    """
    Adds an attachment to an email message.

    Args:
        path_to_file (str): The path to the file to attach.
        message (email.message.EmailMessage): The email message object.

    Returns:
        email.message.EmailMessage: The updated email message object with the attachment.
    """

    if '/' in path_to_file:
        filename = path_to_file.split('/')[-1]
    if '\\' in path_to_file:
        filename = path_to_file.split('\\')[-1]

    mime_type, _ = mimetypes.guess_type(path_to_file)
    mime_type, mime_subtype = mime_type.split('/')
    with open(path_to_file, 'rb') as file:
        message.add_attachment(file.read(), maintype=mime_type, subtype=mime_subtype, filename=filename)
    return message

def single_input(prompt: str, mask: bool = False, width: int = 300, height: int = 150):
    """
    Displays a Tkinter input dialog box and retrieves a user input.

    Args:
        prompt (str): The prompt text displayed in the dialog.
        mask (bool, optional): Whether to mask the input (e.g., for passwords). Defaults to False.
        width (int, optional): Minimum width of the dialog. Defaults to 300.
        height (int, optional): Minimum height of the dialog. Defaults to 150.

    Returns:
        str: The user input as a string.
    """
    root = tk.Tk()
    root.attributes('-topmost', True)  # Keep the window on top
    root.title("Input")

    # Variable to store the entered value
    var = tk.StringVar()

    # Define colors and styles
    footer_bg = root.cget("bg")  # Match footer background to system default background
    body_bg = "white"  # Input box and prompt area
    input_border_color = "#d9d9d9"  # Light gray border color for the input box

    # Create the main content area
    body_frame = tk.Frame(root, bg=body_bg)
    body_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Create a label for the prompt
    prompt_label = tk.Label(body_frame, text=prompt, bg=body_bg, wraplength=width - 20, font=("Helvetica", 12))
    prompt_label.pack(pady=10)

    # Create a frame for the input box
    input_row_frame = tk.Frame(body_frame, bg=body_bg)
    input_row_frame.pack(fill=tk.X, pady=10)

    # Create a frame around the entry box to give it a border
    entry_frame = tk.Frame(input_row_frame, bg=input_border_color, padx=1, pady=1)
    entry_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

    # Create the entry box
    entry = tk.Entry(entry_frame, textvariable=var, font=("Helvetica", 12), show='*' if mask else '')
    entry.pack(fill=tk.X)

    # Create the footer area
    footer_frame = tk.Frame(root, bg=footer_bg)
    footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

    # Save and close
    def save_close():
        root.destroy()

    # Bind Enter key to the save_close function
    entry.bind('<Return>', lambda event: save_close())

    # Create a confirm button in the footer, aligned to the right
    confirm_button = ttk.Button(footer_frame, text='Confirm', command=save_close)
    confirm_button.pack(side=tk.RIGHT, padx=10, pady=10)

    # Focus the entry field
    def set_focus():
        entry.focus_force()  # Force focus on the entry widget
        root.attributes('-topmost', False)  # Reset topmost after setting focus

    root.update_idletasks()  # Ensures all widget sizes are calculated
    content_width = max(root.winfo_reqwidth(), width)
    content_height = max(root.winfo_reqheight(), height)
    root.geometry(f"{content_width}x{content_height}")

    # Center the window on the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - content_width) // 2
    y = (screen_height - content_height) // 2
    root.geometry(f"+{x}+{y}")

    # Set focus after ensuring the window is drawn
    root.after(50, set_focus)

    root.mainloop()

    return var.get()

def input_form(prompt: str=None, inputs: list=None, masks: list=None, width: int = 0, height: int = 0):
    
    """
    Create a dynamic tkinter-based input form with customizable input fields and optional masking for secure input.

    Args:
        prompt (str, optional): Text to display at the top of the form. Defaults to None.
        inputs (list): A list of strings representing the labels for each input field. 
            This argument is required.
        masks (list, optional): A list of booleans indicating whether each input field 
            should be masked (e.g., for password input). Defaults to None.
            If provided, the length of `masks` must match the length of `inputs`.
        width (int, optional): The minimum width of the form in pixels. 
            Automatically calculated if not provided. Defaults to 0.
        height (int, optional): The minimum height of the form in pixels. 
            Automatically calculated if not provided. Defaults to 0.

    Raises:
        Exception: If the `inputs` argument is not provided.
        Exception: If the lengths of `inputs` and `masks` (if provided) do not match.

    Returns:
        dict: A dictionary where the keys are the input labels and the values 
            are the user-entered responses as strings.

    Example:
        To collect a username and password:
        
        ```python
        inputs = ["Username", "Password"]
        masks = [False, True]
        user_data = input_form(prompt="Please enter your login details:", inputs=inputs, masks=masks)
        print(user_data)  # {'Username': 'entered_username', 'Password': 'entered_password'}
        ```

    Notes:
        - The form dynamically adjusts its size based on the number of input fields.
        - A confirm button allows users to submit their input and close the form.
        - Pressing the Enter key in the last input field also submits the form.

    """

    if inputs is None:
        raise Exception("inputs must be declared.")
    if masks is not None and inputs is not None:
        if len(masks) != len(inputs):
            raise Exception("The length of masks does not match the length of inputs.")

    root = tk.Tk()
    root.attributes('-topmost', True)
    root.focus_force()
    
    # Calculate required dimensions
    #label_width = max(len(input_config.get('label', 'Input')) for input_config in inputs) * 8  # Approximate width per char
    label_width = max(len(x) for x in inputs) * 8  # Approximate width per char
    input_field_height = 30  # Approximate height per input field
    padding = 20  # Padding for the frame and labels
    footer_height = 50  # Space for the footer
    prompt_height = 60  # Space for the prompt label

    # Calculate dynamic width and height
    required_width = max(width, label_width + 220)  # Add space for labels and input fields
    required_height = max(height, prompt_height + footer_height + len(inputs) * input_field_height + padding + 40)
    
    # Center the window on the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_offset = (screen_width - required_width) // 2
    y_offset = (screen_height - required_height) // 2

    root.geometry(f'{required_width}x{required_height}+{x_offset}+{y_offset}')
    root.minsize(required_width, required_height)
    root.title('Input Form')

    # Dictionary to store entered values
    values = {}

    # Define colors and styles
    footer_bg = root.cget("bg")  # Match footer background to system default background
    body_bg = "white"  # Input box and prompt area
    input_border_color = footer_bg  # Light gray border color for the input box

    # Create the main content area
    body_frame = tk.Frame(root, bg=body_bg)
    body_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Create a label for the prompt
    if prompt is not None:
        tk.Label(body_frame, text=prompt, bg=body_bg, wraplength=required_width - 20, font=("Helvetica", 12)).pack(pady=10)

    # Create a frame to contain the input fields
    input_fields_frame = tk.Frame(body_frame, bg=body_bg)
    input_fields_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    # Dynamically add input fields
    last_entry = None
    first_entry = None
    for i,label_text in enumerate(inputs):
        try:
            is_masked = masks[i]
        except Exception:
            is_masked = False

        # Create a frame for each input field
        input_frame = tk.Frame(input_fields_frame, bg=body_bg)
        input_frame.pack(fill=tk.X, pady=5)

        # Add the label
        tk.Label(
            input_frame,
            text=label_text + ":",
            bg=body_bg,
            font=("Helvetica", 12),
            anchor='e',
            width=15
        ).pack(side=tk.LEFT, padx=5)

        # Create a frame around the entry box to give it a border
        entry_frame = tk.Frame(input_frame, bg=input_border_color, padx=0, pady=3)
        entry_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Create the entry field with uniform size
        entry = tk.Entry(entry_frame, show='*' if is_masked else '', font=("Helvetica", 12))
        entry.pack(fill=tk.X, padx=5)

        # Store the variable in the dictionary with the label as the key
        values[label_text] = entry
        last_entry = entry  # Keep track of the last entry field

        # Track the first entry field to set focus later
        if first_entry is None:
            first_entry = entry

    # Create the footer area
    footer_frame = tk.Frame(root, bg=footer_bg, height=footer_height)
    footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

    # Save and close
    user_input_values = {}

    def save_close():
        nonlocal user_input_values
        # Retrieve all input values before destroying the root window
        user_input_values = {key: entry.get() for key, entry in values.items()}
        root.destroy()

    # Add padding to ensure button visibility
    footer_frame.grid_propagate(False)

    # Create a confirm button and align it to the right
    confirm_button = ttk.Button(footer_frame, text='Confirm', command=save_close)
    confirm_button.pack(side=tk.RIGHT, padx=20, pady=10)

    # Bind Enter key to the last input field to trigger save_close
    if last_entry:
        last_entry.bind('<Return>', lambda event: save_close())

    # Ensure the first entry field gets focus
    root.after(100, lambda: first_entry.focus_set())

    root.mainloop()
    
    # Return the collected values
    return user_input_values

def show_message(title: str, message: str, width: int = 0, height: int = 0):
    """
    Display a customizable message window using Tkinter.

    This function creates a pop-up window with a specified title and message. 
    The window is centered on the screen and automatically adjusts its size 
    based on the message content, ensuring readability. The user can optionally 
    specify minimum width and height dimensions for the window.

    Args:
        title (str): The title of the message window.
        message (str): The message to display in the window. 
                       Text will wrap to fit the width of the window.
        width (int, optional): The minimum width of the window in pixels. 
                               Defaults to 0, allowing the size to be 
                               determined by the content.
        height (int, optional): The minimum height of the window in pixels. 
                                Defaults to 0, allowing the size to be 
                                determined by the content.

    Returns:
        None
    """

    # Initialize Tkinter root window
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.title(title)

    # Create a temporary label to measure the required size
    temp_label = tk.Label(text=message, font=('Helvetica', 12), wraplength=width - 20)
    temp_label.update_idletasks()  # Update geometry calculations

    # Get the required width and height
    required_width = temp_label.winfo_reqwidth() + 20
    required_height = temp_label.winfo_reqheight() + 80  # Add space for padding and buttons
    temp_label.destroy()

    # Ensure the dimensions respect the minimum size constraints
    final_width = max(width, required_width)
    final_height = max(height, required_height)

    # Center the window on the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - final_width) // 2
    y = (screen_height - final_height) // 2

    root.geometry(f'{final_width}x{final_height}+{x}+{y}')
    root.minsize(width, height)

    # Create the message frame to fill horizontally and vertically
    message_frame = tk.Frame(root, bg='white')  # White background for the message area
    message_frame.pack(fill='both', expand=True)

    # Message label
    message_label = tk.Label(
        message_frame, text=message, bg='white', wraplength=final_width - 20, font=('Helvetica', 12)
    )
    message_label.place(relx=0.5, rely=0.5, anchor='center')  # Center the label

    # Footer frame for the button
    footer_frame = tk.Frame(root, bg=root.cget("bg"))  # Footer matches the title bar
    footer_frame.pack(fill='x', side='bottom')

    # OK Button using ttk for native styling
    def close_window():
        root.destroy()

    ok_button = ttk.Button(
        footer_frame, text="OK", command=close_window
    )
    ok_button.pack(pady=10, side='right', padx=10)

    # Bind the Enter key to close the window
    root.bind('<Return>', lambda event: close_window())

    # Ensure the window gains focus
    root.focus_force()
    
    root.mainloop()

def select_file(title: str, filetypes: list=None):
    """
    Opens a file dialog for the user to select a file.

    Args:
        title (str): The title for the file selection dialog.
        filetypes (list): A list of file type filters (e.g., [("Text files", "*.txt")]).

    Returns:
        str: The path of the selected file or an empty string if no file is selected.
    """

    show_message("Select File", title, width=4, height=5)

    root = tk.Tk()
    root.withdraw()  # Hide the root window
    root.attributes('-topmost', True)  # Ensure the dialog appears on top

    # Open file dialog with the specified title and file types
    if filetypes is not None:
        selected_file = filedialog.askopenfilename(title=title, filetypes=filetypes)
    else:
        selected_file = filedialog.askopenfilename(title=title)
    # Destroy the root window after use
    root.destroy()

    return selected_file