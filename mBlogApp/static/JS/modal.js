const createPostButton = document.querySelector(".create__post");
const modal = document.querySelector(".create-post-modal");
const closeButton = modal.querySelector(".modal-close");

createPostButton.addEventListener("click", (_) => {
    modal.classList.add("is-visible");
    modal.style.animation = 'modalFadeIn 500ms forwards';
    
    const modalClose = _ => {
        modal.classList.remove("is-visible");
        modal.removeEventListener('animationend', modalClose);
    }

    closeButton.addEventListener("click", (_) => {
        modal.style.animation = 'modalFadeOut 500ms forwards';
        modal.addEventListener('animationend', modalClose);
    });
});
