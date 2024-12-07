import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time
from datetime import datetime
import os
from pprint import pp
import json
import mimetypes
import sys


def convert_to_html(text_list, strict=False):
    if not isinstance(text_list, list):
        text_list = [text_list]

    # Define a mapping for escape sequences to their HTML representations
    escape_mapping = {
        "\\": "&bsol;",  # Backslash
        "'": "&apos;",  # Single quote
        '"': "&quot;",  # Double quote
        "\n": "<br>",  # Newline
        "\r": "",  # Carriage return (not represented in HTML)
        "\t": "&nbsp;&nbsp;&nbsp;&nbsp;",  # Tab (4 spaces)
        "\b": "",  # Backspace (not typically represented)
        "\f": "",  # Form feed (not typically represented)
        "\v": "",  # Vertical tab (not typically represented)
        "\a": "",  # Bell/alert sound (not typically represented)
        "\0": "",  # Null character (not typically represented)
    }
    # Convert text by replacing escape sequences with their HTML equivalents
    html_content = ""
    for text in text_list:
        for escape_seq, html_rep in escape_mapping.items():
            text = text.replace(escape_seq, html_rep)
        html_content += text.replace("\n", "<br>")  # Add line breaks for newlines
    if strict:
        # html_content = "<html><body>\n" + html_content + "\n</body></html>"
                # Include mobile-friendly CSS for responsive tables
        css_style = """
        <style>
            .table-container {
                overflow-x: auto;
                -webkit-overflow-scrolling: touch; /* Enable smooth scrolling on iOS */
                margin-bottom: 20px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                padding: 8px;
                border: 1px solid #ddd;
                text-align: left;
            }
        </style>
        """

        # Wrap the HTML content in the responsive container div
        html_content = f"""
        <html>
            <head>{css_style}</head>
            <body>
                <div class="table-container">
                    {html_content}
                </div>
            </body>
        </html>
        """
    return html_content


def get_name(email_str, by="@"):
    if "num" in by:
        for i, char in enumerate(email_str):
            if char.isdigit():
                break
        else:
            return email_str
        return email_str[:i]

    # Handle the case where '@' is the criteria
    elif "@" in by:
        name = email_str.split("@")[0]
        name = get_name(name, by="num")
        name = " ".join([part.capitalize() for part in name.split(".")])
        return name


def extract_kv(
    dir_data=None,
    idx=0,
):  # select the index
    if dir_data is None:
        if "dar" in sys.platform:
            dir_data = "/Users/macjianfeng/Dropbox/github/python/py2ls/confidential_data/gmail_login.json"
        else:
            if "win" in sys.platform:
                dir_data = (
                    "Z:\\Jianfeng\\Apps\\settings\\confidential_data\\gmail_login.json"
                )
            elif "lin" in sys.platform:
                dir_data = "/Users/macjianfeng/Dropbox/github/python/py2ls/confidential_data/gmail_login.json"
    with open(dir_data, "r") as file:
        email_login = json.load(file)
    for i, (user, pd) in enumerate(email_login.items()):
        if i == idx:
            return user, pd


def email_to(**kwargs):
    return email(**kwargs)


def email(**kwargs):
    """
    usage:
    email_to(who=["example@gmail.com"],
              subject="test",
              what="this is the body",
              attachments=["/Users/test.pdf"],
              cc=["cc1@example.com"],
              bcc=["bcc@example.com"],
              html_template="template.html")
    Send an email with optional attachments.

    :param who: Recipient email address (string or list)
    :param subject: Email subject
    :param what: Email body (can be HTML or plain text)
    :param attachments: List of file paths to attach
    :param cc: List of CC email addresses
    :param bcc: List of BCC email addresses, "blind carbon copy"接受者之间互相看不到
    :param html_template: Path to an HTML file for the email body
    """
    who, what, subject, signature = None, None, None, None
    attachments = False
    pause_sec = False  # default 10 seconds pause
    bcc, cc = [], []
    signature_styles = extract_kv(idx=1)[1]  # signature list
    signature = signature_styles[0]  # default signature,None
    read_receipt = False
    verbose = True
    if not kwargs:
        print(
            f'\nUsage:\nemail_to(who="example@gmail.com",\n         subject="test",\n         what="this is the body",\n         attachments="/Users/test.pdf"\n         )'
        )
        return None
    # params config
    for k, v in kwargs.items():
        if any([i in k.lower() for i in ["who", "whe", "to", "@"]]):  # 'who' or "where"
            if isinstance(v, list):
                who = v
            else:
                who = [v]
    for k, v in kwargs.items():
        if any(
            [i in k.lower() for i in ["sub", "hea", "top"]]
        ):  # 'subject', 'header','topic'
            subject = v
        if any(
            [i in k.lower() for i in ["wha", "con", "bod"]]
        ):  # 'what','content','body'
            what = v
        if any([i in k.lower() for i in ["att", "fil"]]):
            attachments = v  # optional
        if any([i in k.lower() for i in ["paus", "tim", "delay"]]):
            pause_sec = v  # optional
        if any(["sig" in k.lower()]):  # 'attachments', 'file'
            signature = v  # optional
            if not isinstance(v, str):
                signature = signature_styles[v]
        if any([i in k.lower() for i in ["verb", "show"]]):  # 'verbose', 'show'
            verbose = v  # verbose
        if any(["cc" in k.lower() and "bcc" not in k.lower(), "ward" in k.lower()]):
            if isinstance(v, list):
                cc = v
            else:
                cc = [v]
        if any([i in k.lower() for i in ["bcc", "blind", "secret"]]):
            if isinstance(v, list):
                bcc = v
            else:
                bcc = [v]
        if any(["temp" in k.lower(), "html" in k.lower()]):
            # Load HTML template if specified
            if isinstance(v, str) and v.endswith("html"):
                with open(kwargs["html_template"], "r") as f:
                    what = f.read()
    # Create email message
    message = MIMEMultipart()
    message["From"] = extract_kv()[0]
    print(who)
    message["To"] = ", ".join(who)

    if len(who) == 1:
        who = ", ".join(who)

    message["Subject"] = subject
    # Add CC addresses if provided
    if cc:
        message["Cc"] = ", ".join(cc)  # Join CC addresses as a comma-separated string

    # the eamil's body
    if what is None:
        what = ""
    if isinstance(what, list):
        what = convert_to_html(what)
    if 'class="' in str(what):
        # Combine HTML content correctly
        html_content = "<html><body>\n"
        html_content += f"{what}"
        html_content += f"<br><br>{convert_to_html([signature])}"
        html_content += "\n</body></html>"
        message.attach(MIMEText(html_content, "html"))
    elif 'class="' in str(attachments):
        # Combine HTML content correctly
        html_content = "<html><body>\n"
        html_content += f"{convert_to_html(what)}<br>{attachments}"
        html_content += f"<br><br>{convert_to_html([signature])}"
        html_content += "\n</body></html>"
        message.attach(MIMEText(html_content, "html"))
    else:
        # add signature
        if signature:
            what += f"\n\n{signature}\n"
        message.attach(MIMEText(what, "plain"))

    # attach files
    if attachments and not 'class="dataframe"' in str(attachments):
        if isinstance(attachments, str):
            attachments = [attachments]
        for file in attachments:
            # 有时候一些不常用的文件类型, 无法自动识别
            mime_type, _ = mimetypes.guess_type(file)
            if mime_type is None:
                if file.endswith(".xlsx"):
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                else:
                    mime_type = "application/octet-stream"

            main_type, sub_type = mime_type.split("/", 1)
            # part = MIMEBase("application", "octet-stream") # 旧的版本
            part = MIMEBase(main_type, sub_type)
            try:
                with open(file, "rb") as attachment:
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                filename = os.path.basename(file)
                part.add_header(
                    "Content-Disposition", f'attachment; filename="{filename}"'
                )
                message.attach(part)
            except FileNotFoundError:
                print(f"File not found: {file}")
            except Exception as e:
                print(f"Error attaching file {file}: {e}")
    if pause_sec:
        time.sleep(pause_sec)

    # Send the email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(extract_kv()[0], extract_kv()[1])
            if any(bcc):
                recipient_list = who + cc + bcc  # Include all recipients
                server.sendmail(extract_kv()[0], recipient_list, message.as_string())
            else:
                server.sendmail(extract_kv()[0], who, message.as_string())

        if verbose:
            if attachments:
                print(
                    f'\nEmail successfully sent to:\nto:"{who}"\nsubject:{subject}\nattached:'
                )
                pp(attachments)
            else:
                print(f'\nEmail successfully sent to:\nto:"{who}"\nsubject:{subject}')
    except Exception as e:
        print(f"Failed to send email: {e}")


def email_to_every(who, subject, what, when, attachments=None):
    """
    Check the time and send an email when the time matches the when.

    :param who: Recipient email address
    :param subject: Email subject
    :param what: Email what
    :param when: Time to send the email in HH:MM format
    :param attachments: List of file paths to attach
    """
    current_time = datetime.now().strftime("%H:%M")
    if current_time == when:
        email_to(
            who=who,
            subject=subject,
            what=what,
            attachments=attachments,
        )


# Example usage
def example_job():
    # Example email details
    reminder_subject = "Reminder: Important Meeting Tomorrow"
    reminder_what = (
        "Don't forget about the meeting tomorrow at 10 AM in the conference room."
    )
    who = "Jianfeng.Liu0413@gmail.com"
    when = "14:30"  # Send time in 24-hour format

    # Optional attachments
    attachments = ["path/to/attachment1.pdf", "path/to/attachment2.jpg"]

    # Schedule the email
    email_to_every(who, reminder_subject, reminder_what, when, attachments)


if __name__ == "__main__":
    pass
    # # Schedule the job to run every minute
    # schedule.every(1).minutes.do(example_job)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    # # example2:
    # email_to(
    #     who="Jianfeng.Liu@medizin.uni-tuebingen.de",
    #     subj="test",
    #     wha="this is the body",
    #     signat="\n\n Best, Jianfeng\n",
    #     att="/Users/macjianfeng/Dropbox/Downloads/_*_doc-xlsx/20240822-preprints_full_20190101_20201031-2.xlsx",
    # )

    # # example3:
    # email_to(
    #     who="Jianfeng.Liu@medizin.uni-tuebingen.de",
    #     subj="test",
    #     wha="this is the test",
    #     signat=2,
    #     # att="/Users/macjianfeng/Dropbox/Downloads/_*_doc-xlsx/20240822-preprints_full_20190101_20201031-2.xlsx",
    # )

    # # example_4
    # print(extract_kv(idx=0))
    # print(extract_kv(idx=0)[0])
    # print(extract_kv(idx=1))
