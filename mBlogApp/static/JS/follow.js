const followButton = document.querySelector('.follow-btn');

followButton.addEventListener('click', () => {
    let value = followButton.getAttribute('data-clicked')
    if (value == 'false')
        followButton.setAttribute('data-clicked', 'true');
    else
        followButton.setAttribute('data-clicked', 'false');
});