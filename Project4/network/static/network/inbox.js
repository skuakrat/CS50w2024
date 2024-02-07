document.addEventListener('DOMContentLoaded', function() {

    let thisuserid = document.querySelector('#thisuser');
    if (thisuserid) {
        const thisuser = document.querySelector('#thisuser').innerHTML;
        document.querySelector('#thisuser').addEventListener('click', () => {profile(thisuser); load_post(thisuser); });
        document.querySelector('#follow').addEventListener('click', () => load_post('follow'));
        document.querySelector('#submit').addEventListener('click', submit);
    }

    load_post('all', 1)
    page('all', 1)
  
});

//Pagination
function goto(type, page_number) {
    load_post(type, page_number)
    page(type, page_number)
}



function page(type, page_number) {

    fetch(`/page/${type}/${page_number}`)
            .then(response => response.text()) // Parse the response as text
            .then(html => {
                // Create a temporary container element
                const tempDiv = document.createElement('div');
                // Set the HTML content of the container with the fetched HTML
                tempDiv.innerHTML = html;
                // Extract the content you want to append from the container
                const content = tempDiv.querySelector('.content-selector');
                // Append the extracted content to the target div
                document.getElementById('paging').innerHTML = html;
            })
            .catch(error => console.error('Error fetching webpage:', error));

 /*

    document.querySelector('#pagination').innerHTML = `
    <div class="pagination">
    <span class="step-links">
        {% if page_obj.has_previous %}
            <a href="?page=1">&laquo; first</a>
            <a href="?page={{ page_obj.previous_page_number }}">previous</a>
        {% endif %}

        <span class="current">
            Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}.
        </span>

        {% if page_obj.has_next %}
            <a href="?page={{ page_obj.next_page_number }}">next</a>
            <a href="?page={{ page_obj.paginator.num_pages }}">last &raquo;</a>
        {% endif %}
    </span>
</div>`


   
    fetch(`/page/${type}/${page_number}`)
    .then(response => response.json())
    .then(posts => {
        posts.forEach(post => {
            const div = document.createElement('div');
            div.innerHTML = 
                `<div class="card p-3 m-1">
                    <h5 class="card-title" id="user-${post.id}">${post.user}</h5>
                    <p class="card-text" id="body-${post.id}">${post.body}</p>
                    <p class="card-subtitle mb-2 text-muted" id="heart-${post.id}"><i class="fa-regular fa-heart" id="like-${post.id}"></i><i class="fa-solid fa-heart" style="color:red" id="unlike-${post.id}"></i> <span id="num-${post.id}">${post.likes}</span></p>
                    <p class="card-text">
                    <small class="text-muted">
                        Posted on ${post.timestamp}; post-id: ${post.id}
                        <span id="closebutton-${post.id}" class="link">(close)</span>
                        <span id="editbutton-${post.id}" class="link">(edit)</span>
                    </small>
                    </p>
                </div>`;
        })
    })
    */

}



// Load all posts
function load_post(type, page_number) {
    event.preventDefault()  

    let page = page_number;

    let thisuserid = document.querySelector('#thisuser');

    if (thisuserid) {
        if (type === "all") {
            document.querySelector('#title').innerHTML = `All posts`;
            document.querySelector('#profile-view').style.display = 'none';
            document.querySelector('#compose-view').style.display = 'block';
            document.querySelector('#posts-view').style.display = 'block';
            document.querySelector('#posts-view').innerHTML = '';
        } else if (type === "follow"){
            document.querySelector('#title').innerHTML = `Followings`;
            document.querySelector('#profile-view').style.display = 'none';
            document.querySelector('#compose-view').style.display = 'none';
            document.querySelector('#posts-view').style.display = 'block';
            document.querySelector('#posts-view').innerHTML = '';
        } else {
            document.querySelector('#title').innerHTML = `Profile`;
            document.querySelector('#profile-view').style.display = 'block';
            document.querySelector('#compose-view').style.display = 'none';
            document.querySelector('#posts-view').style.display = 'block';
            document.querySelector('#posts-view').innerHTML = '';
        }
    } else {
        if (type === "all") {
            document.querySelector('#title').innerHTML = `All posts`;
            document.querySelector('#posts-view').style.display = 'block';
            document.querySelector('#posts-view').innerHTML = '';
        } else if (type === "follow"){
            document.querySelector('#title').innerHTML = `Followings`;
            document.querySelector('#posts-view').style.display = 'block';
            document.querySelector('#posts-view').innerHTML = '';
        } else {
            document.querySelector('#title').innerHTML = `Profile`;
            document.querySelector('#posts-view').style.display = 'block';
            document.querySelector('#posts-view').innerHTML = '';
        }
        
    }



  
    fetch(`/posts/${type}/${page}`)
    .then(response => response.json())
    .then(posts => {
        posts.forEach(post => {
            const div = document.createElement('div');
            div.innerHTML = 
                `<div class="card p-3 m-1">
                    <h5 class="card-title" id="user-${post.id}">${post.user}</h5>
                    <p class="card-text" id="body-${post.id}">${post.body}</p>
                    <p class="card-subtitle mb-2 text-muted" id="heart-${post.id}"><i class="fa-regular fa-heart" id="like-${post.id}"></i><i class="fa-solid fa-heart" style="color:red" id="unlike-${post.id}"></i> <span id="num-${post.id}">${post.likes}</span></p>
                    <p class="card-text">
                    <small class="text-muted">
                        Posted on ${post.timestamp}; post-id: ${post.id}
                        <span id="closebutton-${post.id}" class="link">(close)</span>
                        <span id="editbutton-${post.id}" class="link">(edit)</span>
                    </small>
                    </p>
                </div>`;
            //Default view, hide these.
            div.querySelector(`#like-${post.id}`).style.display = 'none';
            div.querySelector(`#unlike-${post.id}`).style.display = 'none';
            div.querySelector(`#num-${post.id}`).style.display = 'none';
            div.querySelector(`#editbutton-${post.id}`).style.display = 'none';
            div.querySelector(`#closebutton-${post.id}`).style.display = 'none';



            // Go to user profile page
            div.querySelector(`#user-${post.id}`).addEventListener('click', function() {
                load_post(`${post.user}`);
                profile(`${post.user}`);
            });


            // If logged in.
            if (thisuserid) {
                const thisuser = document.querySelector('#thisuser').innerHTML;
                div.querySelector(`#num-${post.id}`).style.display = 'inline';



                // Edit button
                
                let editbutton = div.querySelector(`#editbutton-${post.id}`);
                let closebutton = div.querySelector(`#closebutton-${post.id}`);

                if (editbutton) {
                    
                    if(thisuser === post.user) {
                        editbutton.style.display = 'inline';
                        editbutton.addEventListener('click', function () {
                            editbutton.style.display = 'none';
                            closebutton.style.display = 'inline';
                            let body = div.querySelector(`#body-${post.id}`);
                            body.innerHTML = '';
                            const form = document.createElement('form');
                            form.innerHTML = `
                            <textarea class="form-control" id="text-${post.id}">${post.body}</textarea>
                            <input id="post-button-${post.id}" type="submit" class="btn btn-primary"/>`
                            
                            body.append(form)
                            document.querySelector(`#post-button-${post.id}`).addEventListener('click', () => edit(post.id))
                        })
                    } else {
                        editbutton.style.display = 'none';
                    }
                }


                if (closebutton) {

                    closebutton.addEventListener('click', function () {
                        editbutton.style.display = 'inline';
                        closebutton.style.display = 'none';
                        let body = div.querySelector(`#body-${post.id}`);
                        body.innerHTML = `${post.body}`;
                    })

                }

                

                
                // Unlike function
                div.querySelector(`#unlike-${post.id}`).addEventListener('click', function () {
                    let post_num = parseInt(div.querySelector(`#num-${post.id}`).innerHTML, 10);
                    div.querySelector(`#like-${post.id}`).style.display = 'inline';
                    div.querySelector(`#unlike-${post.id}`).style.display = 'none';
                    div.querySelector(`#num-${post.id}`).innerHTML = `${post_num - 1}`;
                     
                    unlike(post.id)
                })

                // like function
                div.querySelector(`#like-${post.id}`).addEventListener('click', function () {
                    let post_num = parseInt(div.querySelector(`#num-${post.id}`).innerHTML, 10);
                    div.querySelector(`#like-${post.id}`).style.display = 'none';
                    div.querySelector(`#unlike-${post.id}`).style.display = 'inline';
                    div.querySelector(`#num-${post.id}`).innerHTML = `${post_num + 1}`;
                    post_num = post_num;
                    like(post.id)
                })

                if (post.likers.includes(String(thisuser))) {
                    // If thisuser is not in post.likers
                    div.querySelector(`#like-${post.id}`).style.display = 'none';
                    div.querySelector(`#unlike-${post.id}`).style.display = 'inline';
 
                } else {
                    // If thisuser is in post.likers
                    div.querySelector(`#unlike-${post.id}`).style.display = 'none';
                    div.querySelector(`#like-${post.id}`).style.display = 'inline';

                }
                
            }
            
            document.querySelector('#posts-view').append(div);
        });
  
    })
    .catch(error => {
        console.log('Error:', error);
    });
  
}


// edit
function edit(post_id) {

    event.preventDefault() 
    
    const body = document.querySelector(`#text-${post_id}`).value;

    fetch(`edit/${post_id}`, {
        method: 'POST',
        body: JSON.stringify({
            body: body,
            post_id: post_id,
        })
    })
    .then(response => response.json())
    .then(result => {        
        if (result.error) {  
            console.log(result);
            return false;
        } else {
            console.log(result);
            let editbutton = document.querySelector(`#editbutton-${post_id}`);
            let closebutton = document.querySelector(`#closebutton-${post_id}`);
            editbutton.style.display = 'inline';
            closebutton.style.display = 'none';
            let body = document.querySelector(`#body-${post_id}`);
            body.innerHTML = `${document.querySelector(`#text-${post_id}`).value}`;
        }
    })
    
}

function like(post_id) {

    fetch(`like/${post_id}`, {
        method: 'GET'
    
    })
    .then(response => response.json())
    .then(result => {        
        if (result.error) {  
            console.log(result);
        } else {
            console.log(result);
            const heartContainer = document.querySelector(`#heart-${post_id}`);
        }
    })
}


function unlike(post_id) {

    fetch(`unlike/${post_id}`, {
        method: 'GET'
    
    })
    .then(response => response.json())
    .then(result => {        
        if (result.error) {  
            console.log(result);
        } else {
            console.log(result);
            const heartContainer = document.querySelector(`#heart-${post_id}`);
        }
    })
}




// compose new post
function submit(event) {

    event.preventDefault() 
    
    const body = document.querySelector('#compose-body').value;

    fetch('/posts', {
        method: 'POST',
        body: JSON.stringify({
            body: body,
        })
    })
    .then(response => response.json())
    .then(result => {        
        if (result.error) {  
            console.log(result);
            document.querySelector('#alert').innerHTML = '';
            document.querySelector('#alert').style.display = 'block';
            const alert = document.createElement('div');
            alert.innerHTML = result.error;
            alert.className = "alert alert-danger";
            document.querySelector('#alert').append(alert);
            return false;
        } else {
            console.log(result);
            location.reload();
        }
    })
    
}


function profile(type) {
    
    fetch(`/${type}`)
    .then(response => response.json())
    .then(profile => {
        document.querySelector('#profile').innerHTML = `${profile.profile}`;
        document.querySelector('#followers_no').innerHTML = `${profile.followers_no}`;
        document.querySelector('#followers_list').innerHTML = `${profile.followers_list}`;
        document.querySelector('#followings_no').innerHTML = `${profile.followings_no}`;
        document.querySelector('#followings_list').innerHTML = `${profile.followings_list}`;
        const thisuser = String(document.querySelector('#thisuser').innerHTML)

            if (profile.followers_list.includes(thisuser) & profile.profile !== thisuser) {
                document.querySelector('#followed').innerHTML = `Unfollow`;
                document.querySelector('#followed').addEventListener('click', () => unfollow(profile.profile))
            } else if (!profile.followers_list.includes(thisuser) & profile.profile !== thisuser) {
                document.querySelector('#followed').innerHTML = `Follow`;
                document.querySelector('#followed').addEventListener('click', () => follow(profile.profile))
            } else {
                document.querySelector('#followed').innerHTML = '';
            }
    })

}



function follow(username) {

    fetch(`follow/${username}`, {
        method: 'GET'
    
    })
    .then(response => response.json())
    .then(result => {        
        if (result.error) {  
            console.log(result);
        } else {
            console.log(result);
            profile(`${username}`);
        }
    })
}

function unfollow(username) {

    fetch(`unfollow/${username}`, {
        method: 'GET'
    
    })
    .then(response => response.json())
    .then(result => {        
        if (result.error) {  
            console.log(result);
        } else {
            console.log(result);
            profile(`${username}`);
        }
    })
}

