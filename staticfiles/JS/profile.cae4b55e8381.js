const followButton = document.querySelector('.follow-btn');

followButton.addEventListener('click', () => {
    let value = followButton.getAttribute('data-clicked')
    if (value == 'false')
        followButton.setAttribute('data-clicked', 'true');
    else
        followButton.setAttribute('data-clicked', 'false');
});

const isUser = document.querySelector('.left-panel').getAttribute('data-owner');
const profilePhotoDiv = document.querySelector('.profile-photo');

const uploadPhotoModal = document.querySelector('.upload-photo-modal');
const closeButton1 = uploadPhotoModal.querySelector('.modal-close');

if (isUser == 'true') {
    profilePhotoDiv.addEventListener('click', () => {
        uploadPhotoModal.classList.add('is-visible');
        uploadPhotoModal.style.animation = 'modalFadeIn 500ms forwards';
        const modalClose = () => {
            uploadPhotoModal.classList.remove('is-visible');
            modal.removeEventListener('animationend', modalClose);
        };

        closeButton1.addEventListener('click', () => {
            uploadPhotoModal.style.animation = 'modalFadeOut 500ms forwards';
            modal.addEventListener('animationend', modalClose);
        });
    });
}

const uploadPhotoIcon = document.querySelector('.upload-photo-icon')
const uploadButton = document.querySelector('.upload-button');
uploadPhotoIcon.addEventListener('click', () => {
    uploadButton.click()
});
