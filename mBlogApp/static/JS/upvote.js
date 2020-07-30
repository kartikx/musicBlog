/**
 * TODO
 * Implement Toggle Button functionality, so that User isn't allowed to upvote twice.
 * Also implement class changes when toggle Upvote Button.
 * Implement Feed Generation using API, so that Upvote immediately appears.
 */

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie("csrftoken");

const posts = document.querySelectorAll('.feed-post');
const current_user_id = document.querySelector('.feed').getAttribute('data-user-id');



posts.forEach((post) => {
    post.querySelector('.post-upvote').addEventListener('click', () => {
        upvotePost(post);
    })
});

async function getPostsLikedByUser(user_id) {

}

async function getAllPosts() {
    const url = 'http://127.0.0.1:8000/api/posts-list';

    // For get you don't need to pass in any parameters.
    const response = await fetch(url);
    const data = await response.json();
    return data;
    // console.log(`Upvote clicked on ${post.getAttribute('data-post-id')}`);
}

async function upvotePost(post) {
    const postId = post.getAttribute('data-post-id');
    const upvoteButton = post.querySelector('.upvote-btn');
    const upvoteStatus = upvoteButton.getAttribute('data-clicked');
    const upvoteCount = post.querySelector('.upvotes-count');

    let url = `http://127.0.0.1:8000/api/post-details/${postId}`;

    let response = await fetch(url);
    let data = await response.json();
    let upvotes = await data.upvotes;

    if (upvoteStatus == 'false')
    {
        upvotes++;
        upvoteButton.setAttribute('data-clicked', 'true');
        url = `http://127.0.0.1:8000/api/post-details/${postId}/true`;
    } else {
        upvotes--;
        upvoteButton.setAttribute('data-clicked', 'false');
        url = `http://127.0.0.1:8000/api/post-details/${postId}/false`;
    }

    upvoteCount.textContent = upvotes;

    response = await fetch(url, {
        method: "PUT",
        headers: {
            "Content-type": "application/json",
            "X-CSRFToken": csrftoken
        },
        // body: JSON.stringify(data),
    });
}
