# Bank statement generation (Zywa-23)

<img src="https://github.com/Emad-Eldin-G/Transactions-details/blob/main/logo.png" width="250">

## Tech Stack
------------------------------------  
### Django
> Web Framework
  
I used the Django web framework as it's built for the Python programming language, which offers really good versatility and ease of use. Django also has many out-of-the-box features that aid development and ensure code quality and integrity, some of those features include: Django REST framework, Django Models ORM, Django mail API, Django auth api.  


### DocXtpl
> Statement creation library

DocXtpl is a Python library that allowed me to create a template for the bank statement as a docx file. It also allows to create placeholder text and cells in the docx template that could be replaced by data from the Python program. As shown for example, the following line renders the data (value) to the placeholder (key) in the template:
```python
template.render({'email': email, 'total': total, 'fromDate': date1, 'toDate': date2, 'invoice_list': transactionsList})
```
I chose the DocXtpl as its templating style is very similar to the Django Template Language, which I have previous experience with.  
Here is how the template looks before data rendering:  
<br>
<img src="https://github.com/Emad-Eldin-G/Transactions-details/blob/main/template.png" width=550>  


### Docx2pdf
> PDF creation/conversion library

Docx2Pdf is a very widely used docx to pdf conversion library, it allowed me to maintain all the template data in the docx and create a perfect pdf document to send in the email. It only has one problem which is that it requires msWord to be installed, meaning that it can only run on Windows and macOS servers currently. However, it is sufficient for the problem at hand.


### Gmail SMTP server + Python Email message app  
This is the combination I used to create and send the bank statement as an email. It is not very secure but it works well for this project. I would personally use a third-party email service like MailChimp to send emails, but configuring it and setting it up with an email domain could not be done before the deadline.
