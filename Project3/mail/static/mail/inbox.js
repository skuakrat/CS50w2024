document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#submit').addEventListener('click', submit);


  // By default, load the inbox
  load_mailbox('inbox');

  //compose submit
function submit() {
  
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
    })
  })
  load_mailbox('sent');
}

});




function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      emails.forEach(email => {
        const div = document.createElement('div');
        div.style.cursor = "pointer";
        div.innerHTML = `<div class="row">
        <div class="col">
          <b>${email.sender}</b>
        </div>
        <div class="col-6">
          ${email.subject}
        </div>
        <div class="col">
          ${email.timestamp}
        </div>
      </div>`;

        if (email.read === true) {
          div.className = 'py-3 container border border-dark';
          div.style.backgroundColor = '#e9ecef';
        } else {
          div.className = 'py-3 container border border-dark ';
        }

        div.addEventListener('click', function() {
          fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
               read: true
            })
          })
          console.log('This element has been clicked!')
          load_mail(email.id)
        });
        
        
        document.querySelector('#emails-view').append(div);
      });

  })
  .catch(error => {
      console.log('Error:', error);
  });

}

function load_mail(id) {
  // Show the mailbox and hide other views

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').innerHTML = '';
  const userEmail = document.querySelector('#userEmail').innerHTML;

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      const div = document.createElement('div');
      div.innerHTML = 
        `
        <div class="py-1 container ">
        <b>From:</b> ${email.sender}
        </div>
        <div class="py-1 container ">
        <b>To:</b> ${email.recipients}
        </div>
        <div class="py-1 container ">
        <b>Subject:</b> ${email.subject}
        </div>
        <div class="py-1 container ">
        <b>Time:</b> ${email.timestamp}
        </div>
        <hr>
        <div class="pt-1 container ">
        <b>Message:</b>
        </div>
        <div class="py-3 container ">
        ${email.body}
        </div>
        `;
      document.querySelector('#email-view').append(div);

      // archive button, excluse sent emails
      if (email.sender !== userEmail) {
        console.log(`${email.sender}`, `${userEmail}`);
        const div1 = document.createElement('div')
        div1.className = "ml-1 btn btn-sm btn-outline-primary";
        if (email.archived === true) {
          div1.innerHTML = "Unarchive";
          document.querySelector('#email-view').append(div1);
          div1.addEventListener('click', function() {
            fetch(`/emails/${email.id}`, {
              method: 'PUT',
              body: JSON.stringify({
                 archived: false
              })
            })
            console.log('Archived clicked!')
            location.reload();
          });


        } else {
          div1.innerHTML = "Archive";
          document.querySelector('#email-view').append(div1);
          div1.addEventListener('click', function() {
            fetch(`/emails/${email.id}`, {
              method: 'PUT',
              body: JSON.stringify({
                 archived: true
              })
            })
            console.log('Unarchived clicked!')
            location.reload();
          });
        }
        
      }



      // reply button
      const div2 = document.createElement('div')
      div2.className = "ml-1 btn btn-sm btn-outline-primary";
      div2.innerHTML = "Reply";
      document.querySelector('#email-view').append(div2);
  })
}
