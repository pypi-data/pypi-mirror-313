Examples
========

Advanced Usage
------------

Sending with Attachments
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from shoutbox import ShoutboxClient, Email, Attachment
   
   with ShoutboxClient() as client:
       with open('document.pdf', 'rb') as f:
           attachment = Attachment(
               filename='document.pdf',
               content=f.read()
           )
       
       email = Email(
           to="recipient@example.com",
           subject="Document",
           html="<h1>Please find attached document</h1>",
           from_email="sender@yourdomain.com",
           attachments=[attachment]
       )
       
       response = client.send(email)
